import uuid
from pydantic import BaseModel
from datetime import datetime

class TournamentGeneralModel(BaseModel):
    uid_tournament: uuid.UUID
    name: str 
    description: str
    type: str 
    start_date: datetime 
    end_date: datetime 
    minimun_player_per_team: int
    minimun_player_general: int

class TournamentModel(BaseModel):
    name: str 
    description: str
    type: str 
    start_date: datetime 
    end_date: datetime 
    minimun_player_per_team: int
    minimun_player_general: int
