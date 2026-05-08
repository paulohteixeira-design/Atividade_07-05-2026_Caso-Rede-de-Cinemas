
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Cinema:
    id: Optional[int]
    nome: str
    endereco: str
    capacidade: int


@dataclass(slots=True)
class Filme:
    id: Optional[int]
    titulo: str
    genero: str
    duracao_minutos: int
    diretor: str
    elenco: str


@dataclass(slots=True)
class Sessao:
    id: Optional[int]
    cinema_id: int
    filme_id: int
    data: str
    horario_inicio: str
    publico_registrado: int = 0
