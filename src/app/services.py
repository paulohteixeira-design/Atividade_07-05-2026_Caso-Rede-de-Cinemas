
from __future__ import annotations

from datetime import datetime

from .models import Cinema, Filme, Sessao
from .repositories import CinemaRepository, FilmeRepository, SessaoRepository


class CinemaService:
    def __init__(self, repo: CinemaRepository) -> None:
        self.repo = repo

    def cadastrar(self, nome: str, endereco: str, capacidade: int) -> int:
        if not nome.strip() or not endereco.strip():
            raise ValueError("Nome e endereço são obrigatórios.")
        if capacidade <= 0:
            raise ValueError("Capacidade deve ser maior que zero.")
        return self.repo.create(Cinema(None, nome.strip(), endereco.strip(), capacidade))


class FilmeService:
    def __init__(self, repo: FilmeRepository) -> None:
        self.repo = repo

    def cadastrar(self, titulo: str, genero: str, duracao_minutos: int, diretor: str, elenco: str) -> int:
        if not titulo.strip() or not genero.strip() or not diretor.strip() or not elenco.strip():
            raise ValueError("Todos os campos do filme são obrigatórios.")
        if duracao_minutos <= 0:
            raise ValueError("Duração deve ser maior que zero.")
        filme = Filme(None, titulo.strip(), genero.strip(), duracao_minutos, diretor.strip(), elenco.strip())
        return self.repo.create(filme)


class SessaoService:
    INTERVALO_MINUTOS = 15

    def __init__(self, sessao_repo: SessaoRepository, cinema_repo: CinemaRepository, filme_repo: FilmeRepository) -> None:
        self.sessao_repo = sessao_repo
        self.cinema_repo = cinema_repo
        self.filme_repo = filme_repo

    def cadastrar(self, cinema_id: int, filme_id: int, data: str, horario_inicio: str) -> int:
        if self.cinema_repo.get_by_id(cinema_id) is None:
            raise ValueError("Cinema não encontrado.")
        if self.filme_repo.get_by_id(filme_id) is None:
            raise ValueError("Filme não encontrado.")
        self._validar_data_hora(data, horario_inicio)
        return self.sessao_repo.create(Sessao(None, cinema_id, filme_id, data, horario_inicio, 0))

    def registrar_publico(self, sessao_id: int, quantidade: int) -> None:
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")

        sessao = self.sessao_repo.get_detailed_by_id(sessao_id)
        if sessao is None:
            raise ValueError("Sessão não encontrada.")

        novo_total = int(sessao["publico_registrado"]) + quantidade
        capacidade = int(sessao["cinema_capacidade"])
        if novo_total > capacidade:
            raise ValueError(f"Limite excedido. Capacidade do cinema: {capacidade}.")

        self.sessao_repo.update_publico(sessao_id, novo_total)

    def total_por_filme(self, filme_id: int) -> int:
        return self.sessao_repo.total_por_filme(filme_id)

    def total_por_cinema(self, cinema_id: int) -> int:
        return self.sessao_repo.total_por_cinema(cinema_id)

    @staticmethod
    def _validar_data_hora(data: str, horario_inicio: str) -> None:
        try:
            datetime.strptime(f"{data} {horario_inicio}", "%Y-%m-%d %H:%M")
        except ValueError as exc:
            raise ValueError("Data ou horário inválidos. Use YYYY-MM-DD e HH:MM.") from exc
