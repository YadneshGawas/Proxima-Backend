from app.extensions import db   
from app.modules.teams.models import (HackathonTeamMember,HackathonTeam,TeamMemberRole)
from app.modules.teams.exceptions import (NotTeamOwnerException,MemberNotFoundException,MemberAlreadyExistsException,TeamNotFoundException)

class TeamService:

    @staticmethod
    def create_team(name,created_by):
        team = HackathonTeam(name=name,created_by=created_by)
        db.session.add(team)
        db.session.flush()
        
        owner = HackathonTeamMember(hackathon_team_id=team.id,member_id=created_by,role=TeamMemberRole.OWNER)
        db.session.add(owner)
        db.session.commit()
        return team
    
    @staticmethod
    def _ensure_owner(team,user_id):
        if team.created_by != user_id:
            raise NotTeamOwnerException("Only owner can perform this action")
    
    @staticmethod
    def add_member(team_id, requester_id, member_id, role):
        team = HackathonTeam.query.get(team_id)
        if not team:
            raise TeamNotFoundException("Team not found")

        TeamService._ensure_owner(team, requester_id)

        existing = HackathonTeamMember.query.filter_by(
            hackathon_team_id=team_id,
            member_id=member_id
        ).first()

        if existing:
            raise MemberAlreadyExistsException("Member already exists")

        member = HackathonTeamMember(
            hackathon_team_id=team_id,
            member_id=member_id,
            role=TeamMemberRole(role)
        )

        db.session.add(member)
        db.session.commit()
        return member
    
    @staticmethod
    def remove_member(team_id, requester_id, member_id):
        team = HackathonTeam.query.get(team_id)
        if not team:
            raise TeamNotFoundException("Team not found")

        TeamService._ensure_owner(team, requester_id)

        member = HackathonTeamMember.query.filter_by(
            hackathon_team_id=team_id,
            member_id=member_id
        ).first()

        if not member:
            raise MemberNotFoundException("Member not found")

        db.session.delete(member)
        db.session.commit()

    @staticmethod
    def update_member_role(team_id,member_id,new_role,requester_id):
        team = HackathonTeam.query.get(team_id)
        if not team:
            raise TeamNotFoundException("Team not found")

        TeamService._ensure_owner(team, requester_id)

        member = HackathonTeamMember.query.filter_by(
            hackathon_team_id=team_id,
            member_id=member_id
        ).first()

        if not member:
            raise MemberNotFoundException("Member not found")

        member.role = TeamMemberRole(new_role)
        db.session.commit()
        return member


    @staticmethod
    def get_team_details(team_id):
        team = HackathonTeam.query.get(team_id)
        members = team.members
        if not team:
            raise TeamNotFoundException("Team not found")
        return team,members