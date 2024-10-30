from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import TournamentModel
from sqlmodel import select, desc
from ..db.models import Tournament

class TournamentService:
    async def get_all_tournaments(self,session:AsyncSession):
        statement = select(Tournament)
        result = await session.exec(statement)
        return result.all()
    
    async def get_tournament(self, tournament_uid: str,session:AsyncSession):
        statement = select(Tournament).where(Tournament.uid_tournament == tournament_uid)
        result = await session.exec(statement)
        tournament = result.first()
        return tournament if tournament is not None else None
    
    async def add_tournament(self, session:AsyncSession,tournament_data=TournamentModel ):
        tournament_data_dict = tournament_data.model_dump()
        new_tournament = Tournament(**tournament_data_dict)
        session.add(new_tournament)
        await session.commit()
        return new_tournament
    
    async def update_tournament(self, tournament_uid: str, session:AsyncSession,update_data=TournamentModel):
        tournament_to_update=await self.get_tournament(tournament_uid)

        if tournament_to_update is not None:
            update_data_dict = update_data.model_dump()

            for k,v in update_data_dict.items():
                setattr(tournament_to_update,k,v)
            
            await session.commit()
            return tournament_to_update
        else:
            None

    async def delete_tournament(self, tournament_uid: str, session:AsyncSession):
        tournament_to_delete=await self.get_tournament(tournament_uid)

        if tournament_to_delete is not None:
            await session.delete(tournament_to_delete)
            await session.commit()
            return {}
        else:
            None
