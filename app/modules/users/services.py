from app.extensions import db
from .models import User
from .utils import hash_password, check_password, generate_access_token
from .exceptions import UserAlreadyExistsError,UserNotFoundError,InvalidCredentialsError

class AuthService:
    @staticmethod
    def register_user(name:str,email:str,password:str)->User:

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {email} already exists.")
        
        try:
            new_user = User(
                name=name,
                email=email,
                password_hash=hash_password(password)
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception('Database error during user registration.') from e
        return {
            "message": "User registered successfully",
            "user" : {
                "id": new_user.id,
                "name": new_user.name,
                "email": new_user.email
            }
        },201
    
    @staticmethod
    def login_user(email:str,password:str)->User:
        user = User.query.filter_by(email=email).first()

        # If user is missing OR password doesn't match, reject login
        if (not user) or (not check_password(user.password_hash, password)):
            raise InvalidCredentialsError("Invalid email or password.")

        access_token = generate_access_token(user_id = str(user.id))
        return {
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }, 200
    
    @staticmethod
    def logout_user()->str:
        return {
            "message": "Logout successful"
        }, 200
    
    @staticmethod
    def get_current_user(user_id:int)->User:
        user = User.query.get(user_id)
        if not user:
            raise UserNotFoundError("User not found.")
        
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        },200
    
    @staticmethod
    def update_user(user_id:int,data)->User:
        user = User.query.get(user_id)
        if not user:
            raise UserNotFoundError("User not found.")
        
        if data.get("name"):
            user.name = data["name"]
        if data.get("email"):
            user.email = data["email"]
        if data.get("password"):
            user.password_hash = hash_password(data["password"])        
        db.session.commit()

        return {
            "message": "User updated successfully",     
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }         
        }   
        