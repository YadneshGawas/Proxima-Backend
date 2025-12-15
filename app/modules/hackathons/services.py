import uuid
from app.extensions import db
from .models import Hackathon
from .exceptions import (
    HackathonNotFoundError,HackathonCreateError,HackathonQueryError,Teamsizelimit
    )
from sqlalchemy.exc import SQLAlchemyError
from .schemas import HackathonCreateSchema,HackathonUpdateSchema,HackathonResponse

from sqlalchemy import and_, or_
from sqlalchemy.orm import Query
from typing import Optional
from app.modules.hackathons.models import HackathonInterest

class HackathonService:

    @staticmethod
    def create_hackathon(data: HackathonCreateSchema) -> Hackathon:
        if data.min_team_size > data.max_team_size:
            raise Teamsizelimit("Minimum Team size should be lower")

        hackathon = Hackathon(
            id=str(uuid.uuid4()),
            organizer_id=data.organizer_id,
            event_name=data.event_name,
            description=data.description,
            location=data.location,

            mode=data.mode,
            participation_type=data.participation_type,
            min_team_size=data.min_team_size,
            max_team_size=data.max_team_size,

            deadline=data.deadline,
            start_date=data.start_date,
            end_date=data.end_date,

            entry_fee=data.entry_fee,
            max_participants=data.max_participants,
            tags=data.tags or [],
            status=data.status,
            image_url=data.image_url,
            requirements=data.requirements or [],
            prizes=data.prizes or [],
        )

        try:
            db.session.add(hackathon)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            # Optional: log the real error for debugging
            # current_app.logger.error(f"Hackathon creation failed: {e}")
            raise HackathonCreateError("Database error while creating hackathon.")

        return hackathon
    
    @staticmethod
    def get_hackathons(
        page: int = 1,
        limit: int = 10,
        mode: Optional[str] = None,
        participation_type: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None,
        organizer_id: Optional[str] = None,
        status: Optional[str] = None
        
    ) -> tuple[list[Hackathon], int]:

        try:
            query: Query = Hackathon.query

            # Filters
            if mode:
                query = query.filter(Hackathon.mode == mode)

            if participation_type:
                query = query.filter(Hackathon.participation_type == participation_type)
            
            if organizer_id:
                print("Filtering by organizer:", organizer_id)
                query = query.filter(Hackathon.organizer_id == organizer_id)
            
            if status:
                query = query.filter(Hackathon.status == status)

            if tag:
                query = query.filter(Hackathon.tags.like(f'%"{tag}"%'))


            if search:
                search_pattern = f"%{search}%"
                query = query.filter(
                    or_(
                        Hackathon.event_name.ilike(search_pattern),
                        Hackathon.description.ilike(search_pattern),
                        Hackathon.location.ilike(search_pattern),
                    )
                )

            # Count total before pagination
            total = query.count()

            # Apply pagination + sorting
            hackathons = (
                query.order_by(Hackathon.created_at.desc())
                     .offset((page - 1) * limit)
                     .limit(limit)
                     .all()
            )

            return hackathons, total
        
        except SQLAlchemyError as e:
            # Optional debug logging:
            # current_app.logger.error(f"Failed fetching hackathons: {e}")
            raise HackathonQueryError("Database error while fetching hackathons.")


    @staticmethod
    def update_hackathon(hackathon_id: str, organizer_id: str, data: HackathonUpdateSchema):
        hackathon = Hackathon.query.get(hackathon_id)

        if not hackathon:
            raise HackathonNotFoundError("Hackathon not found.")

        # Permission check
        if hackathon.organizer_id != organizer_id:
            raise PermissionError("You cannot update someone else's hackathon.")

        # Apply updated fields
        for field, value in data.dict(exclude_unset=True).items():
            setattr(hackathon, field, value)

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise HackathonCreateError("Failed to update hackathon.")

        return hackathon

    @staticmethod
    def delete_hackathon(hackathon_id: str, organizer_id: str):
        hackathon = Hackathon.query.get(hackathon_id)

        if not hackathon:
            raise HackathonNotFoundError("Hackathon not found.")

        # Permission check
        if hackathon.organizer_id != organizer_id:
            raise PermissionError("You cannot delete someone else's hackathon.")

        try:
            db.session.delete(hackathon)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise HackathonCreateError("Failed to delete hackathon.")

        return True
    
    @staticmethod
    def get_hackathon_by_id(hackathon_id: str, user_id: str | None = None):
        hackathon = Hackathon.query.get(hackathon_id)

        if not hackathon:
            raise HackathonNotFoundError("Hackathon not found.")

        is_interested = False

        if user_id:
            is_interested = (
                HackathonInterest.query.filter_by(
                    hackathon_id=hackathon_id,
                    user_id=user_id
                ).first()
                is not None
            )

        # return both ORM + computed field
        data = HackathonResponse.from_orm(hackathon).dict()
        data["is_interested"] = is_interested

        return data


    # @staticmethod
    # def toggle_interest(hackathon_id: str, increment: bool = True):
    #     hackathon = Hackathon.query.get(hackathon_id)

    #     if not hackathon:
    #         raise HackathonNotFoundError("Hackathon not found.")

    #     if increment:
    #         hackathon.interested_count += 1
    #     else:
    #         hackathon.interested_count = max(0, hackathon.interested_count - 1)

    #     try:
    #         db.session.commit()
    #     except SQLAlchemyError:
    #         db.session.rollback()
    #         raise HackathonCreateError("Failed to update interest count.")

    #     return hackathon.interested_count

    @staticmethod
    def toggle_interest(user_id: str, hackathon_id: str):
        hackathon = Hackathon.query.get(hackathon_id)
        if not hackathon:
            raise HackathonNotFoundError("Hackathon not found.")

        interest = HackathonInterest.query.filter_by(
            user_id=user_id,
            hackathon_id=hackathon_id
        ).first()

        try:
            if interest:
                # User already interested → REMOVE interest
                db.session.delete(interest)
                hackathon.interested_count = max(0, hackathon.interested_count - 1)
                is_interested = False
            else:
                # User not interested → ADD interest
                db.session.add(
                    HackathonInterest(
                        user_id=user_id,
                        hackathon_id=hackathon_id
                    )
                )
                hackathon.interested_count += 1
                is_interested = True

            db.session.commit()
            return {
                "interested_count": hackathon.interested_count,
                "is_interested": is_interested
            }

        except SQLAlchemyError:
            db.session.rollback()
            raise HackathonCreateError("Failed to update interest.")
