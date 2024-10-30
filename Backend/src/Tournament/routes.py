from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import TournamentGeneralModel,TournamentModel
from typing import List
from src.db.main import get_session
from .service import TournamentService

tournament_router = APIRouter()
tournament_service = TournamentService()

@tournament_router.get("/",response_model=List[TournamentGeneralModel])
async def get_all_tournaments(session: AsyncSession = Depends(get_session)):

    tournaments =  await tournament_service.get_all_tournaments(session)
    return tournaments

@tournament_router.post("/",status_code=status.HTTP_201_CREATED,response_model=TournamentGeneralModel)
async def create_tournament( tournament_data: TournamentModel,session: AsyncSession = Depends(get_session))->dict:

    new_tournament = await tournament_service.add_tournament(session,tournament_data)
    return new_tournament

@tournament_router.get("/{tournament_uuid}",response_model=TournamentGeneralModel)
async def get_tournament(tournament_uuid:str, session: AsyncSession = Depends(get_session)):
    tournament =  await tournament_service.get_tournament(tournament_uuid,session)

    if tournament:
        return tournament
    else:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Torneo no encontrado")

@tournament_router.put("/{tournament_uuid}",response_model=TournamentGeneralModel)
async def update_tournament(tournament_uuid:str,
                            tournament_data: TournamentModel,session: AsyncSession = Depends(get_session)) ->dict:
    
    updated_tournament =  await tournament_service.update_tournament(tournament_uuid,session,tournament_data)

    if updated_tournament:
        return updated_tournament
    else:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Torneo no encontrado")

@tournament_router.delete("/{tournament_uuid}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_tournament(tournament_uuid:str,session: AsyncSession = Depends(get_session)):
    tournament_to_delete =  await tournament_service.delete_tournament(tournament_uuid,session)

    if tournament_to_delete:
        return tournament_to_delete
    else:
        raise HTTPException(status=status.HTTP_404_NOT_FOUND, detail="Torneo no encontrado")
