
from __future__ import annotations

from .services import CinemaService, FilmeService, SessaoService


class CinemaController:
    def __init__(self, service: CinemaService) -> None:
        self.service = service

    def criar(self, nome: str, endereco: str, capacidade: str) -> int:
        return self.service.cadastrar(nome, endereco, int(capacidade))


class FilmeController:
    def __init__(self, service: FilmeService) -> None:
        self.service = service

    def criar(self, titulo: str, genero: str, duracao_minutos: str, diretor: str, elenco: str) -> int:
        return self.service.cadastrar(titulo, genero, int(duracao_minutos), diretor, elenco)


class SessaoController:
    def __init__(self, service: SessaoService) -> None:
        self.service = service

    def criar(self, cinema_id: str, filme_id: str, data: str, horario_inicio: str) -> int:
        return self.service.cadastrar(int(cinema_id), int(filme_id), data, horario_inicio)

    def registrar_publico(self, sessao_id: str, quantidade: str) -> None:
        self.service.registrar_publico(int(sessao_id), int(quantidade))
