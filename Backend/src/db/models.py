from typing import List, Optional
from sqlmodel import Relationship, SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from sqlalchemy import String
from enum import Enum
from datetime import datetime

class Tournament_Player(SQLModel, table=True):
    """
    Modelo de base de datos para la tabla `Tournament_Player`, que representa la tabla de rompimiento entre Tournament y Player

    Atributos:
        uid_tournament (uuid.UUID): Identificador único del torneo.
        uid_player (uuid.UUID): Identificador del jugador
        cancelled (bool): Indica si un jugador canceló, es decir, se retiró.
    Métodos:
        __repr__: Representación del objeto Tournament_Player como cadena.
    """

    __tablename__ = "tournament_player"

    uid_tournament: uuid.UUID = Field(foreign_key="tournament.uid_tournament", primary_key=True)
    uid_player: uuid.UUID = Field(foreign_key="player.uid", primary_key=True)
    cancelled: bool

    def __repr__(self) -> str:
        """
        Representa al objeto Tournament_Player como una cadena.

        Returns:
            str: Representación del jugador en formato 'Jugador <uid_player>'.
        """
        return f"Tournament_Player (Jugador {self.uid_player})"


class Player_Match(SQLModel, table = True):
    __tablename__ = "player_match"

    uid_match: uuid.UUID = Field(foreign_key="match.uid_match", primary_key=True)
    uid_player: uuid.UUID = Field(foreign_key="player.uid", primary_key=True)
    position: int

class Match(SQLModel, table= True):
    __tablename__ = "match"

    uid_match: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            unique=True,
            default=uuid.uuid4
        )
    )

    duracion: int
    players: Optional[List["Player"]] = Relationship(back_populates="matches",link_model=Player_Match)
    
class Player(SQLModel, table=True):
    """
    Modelo de base de datos para la tabla `Player`, que representa a un jugador en el sistema.

    Atributos:
        uid (uuid.UUID): Identificador único del jugador. Se genera automáticamente usando UUID4.
        name (str): Nombre del jugador, con un límite máximo de caracteres.

    Métodos:
        __repr__: Representación del objeto Player como cadena.
    """

    __tablename__ = "player"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            unique=True,
            default=uuid.uuid4
        )
    )

    name: str = Field(sa_column=Column(String(20), nullable=False))

    tournaments: List["Tournament"] = Relationship(back_populates="players", link_model=Tournament_Player)
    team_id: str | None = Field(default=None, foreign_key="team.name")
    teams: Optional["Team"] = Relationship(back_populates="players")
    matches: Optional[List["Match"]] = Relationship(back_populates="players",link_model=Player_Match)

    def __repr__(self) -> str:
        """
        Representa al objeto Player como una cadena.

        Returns:
            str: Representación del jugador en formato 'Jugador <nombre>'.
        """
        return f"Jugador {self.name}"


class Team(SQLModel, table=True):
    __tablename__ = "team"

    name: str = Field(default=None, nullable=False, primary_key=True)  
    players:List["Player"] = Relationship(back_populates="teams")


class TournamentType(str, Enum):
    SIMPLE = "Eliminatorias simples"
    DOUBLE = "Eliminatorias dobles"
    LEAGUE = "Liga"


class Tournament(SQLModel, table=True):
    """
    Modelo de base de datos para la tabla `Tournament`, que representa a un torneo en el sistema.

    Atributos:
        uid_tournament (uuid.UUID): Identificador único del torneo. Se genera automáticamente usando UUID4.
        name (str): Nombre del torneo, con un límite máximo de caracteres.
        description (str): Descripción del torneo, con un número máximo de caracteres.
        type (TournamentType): El tipo de juego en el torneo.
        start_date (datetime): Fecha de inicio del torneo.
        end_date (datetime): Fecha de finalización del torneo.
        minimun_player_per_team: Cantidad mínima de jugadores por equipo.
        minimun_player_general: Aforo mínimo para iniciar el torneo.
    Métodos:
        __repr__: Representación del objeto Tournament como cadena.
    """

    __tablename__ = "tournament"

    uid_tournament: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            unique=True,
            default=uuid.uuid4
        )
    )

    name: str = Field(sa_column=Column(String(20), nullable=False))
    description: str = Field(sa_column=Column(String(200), nullable=False))
    type: TournamentType = Field(sa_column=Column(String(23), nullable=False))
    start_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False))
    end_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, nullable=False))
    minimun_player_per_team: int
    minimun_player_general: int

    players: List["Player"] = Relationship(back_populates="tournaments", link_model=Tournament_Player)

    def __repr__(self) -> str:
        """
        Representa al objeto Tournament como una cadena.

        Returns:
            str: Representación del torneo en formato 'Torneo <nombre>'.
        """
        return f"Torneo {self.name}"
