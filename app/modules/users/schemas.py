from pydantic import EmailStr, BaseModel, Field

class RegisterSchema(BaseModel):
    name: str = Field(..., min_length=3, description="The user's name")
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., min_length=8, description="The user's password")

class LoginSchema(BaseModel):
    email: EmailStr = Field(..., description="The user's email address")
    password: str = Field(..., description="The user's password")

class UserResponse(BaseModel):
    id:int
    name: str
    email: EmailStr

class RegisterResponse(BaseModel):
    message: str
    user: UserResponse

class LoginResponse(BaseModel):
    message: str
    access_token: str
    user: UserResponse

class LogoutResponse(BaseModel):
    message: str




