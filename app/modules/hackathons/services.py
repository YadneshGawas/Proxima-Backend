import uuid
from app.extensions import db
from .models import Hackathon
from .exceptions import HackathonNotFoundError,HackathonCreateError,HackathonQueryError,Teamsizelimit
from sqlalchemy.exc import SQLAlchemyError
from .schemas import HackathonCreateSchema

from sqlalchemy import and_, or_
from sqlalchemy.orm import Query
from typing import Optional

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
        organizer_id: Optional[str] = None
        
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

