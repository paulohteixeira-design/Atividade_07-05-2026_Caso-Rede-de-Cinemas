
from __future__ import annotations

import sqlite3

from .models import Cinema, Filme, Sessao


class CinemaRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def create(self, cinema: Cinema) -> int:
        cur = self.conn.execute(
            "INSERT INTO cinemas (nome, endereco, capacidade) VALUES (?, ?, ?)",
            (cinema.nome, cinema.endereco, cinema.capacidade),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def list_all(self) -> list[sqlite3.Row]:
        cur = self.conn.execute("SELECT * FROM cinemas ORDER BY id DESC")
        return list(cur.fetchall())

    def get_by_id(self, cinema_id: int) -> sqlite3.Row | None:
        cur = self.conn.execute("SELECT * FROM cinemas WHERE id = ?", (cinema_id,))
        return cur.fetchone()


class FilmeRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def create(self, filme: Filme) -> int:
        cur = self.conn.execute(
            "INSERT INTO filmes (titulo, genero, duracao_minutos, diretor, elenco) VALUES (?, ?, ?, ?, ?)",
            (filme.titulo, filme.genero, filme.duracao_minutos, filme.diretor, filme.elenco),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def list_all(self) -> list[sqlite3.Row]:
        cur = self.conn.execute("SELECT * FROM filmes ORDER BY id DESC")
        return list(cur.fetchall())

    def get_by_id(self, filme_id: int) -> sqlite3.Row | None:
        cur = self.conn.execute("SELECT * FROM filmes WHERE id = ?", (filme_id,))
        return cur.fetchone()


class SessaoRepository:
    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn

    def create(self, sessao: Sessao) -> int:
        cur = self.conn.execute(
            """
            INSERT INTO sessoes (cinema_id, filme_id, data, horario_inicio, publico_registrado)
            VALUES (?, ?, ?, ?, ?)
            """,
            (sessao.cinema_id, sessao.filme_id, sessao.data, sessao.horario_inicio, sessao.publico_registrado),
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def list_all(self) -> list[sqlite3.Row]:
        cur = self.conn.execute(
            """
            SELECT s.*, c.nome AS cinema_nome, f.titulo AS filme_titulo
            FROM sessoes s
            JOIN cinemas c ON c.id = s.cinema_id
            JOIN filmes f ON f.id = s.filme_id
            ORDER BY s.data DESC, s.horario_inicio DESC
            """
        )
        return list(cur.fetchall())

    def get_by_id(self, sessao_id: int) -> sqlite3.Row | None:
        cur = self.conn.execute("SELECT * FROM sessoes WHERE id = ?", (sessao_id,))
        return cur.fetchone()

    def get_detailed_by_id(self, sessao_id: int) -> sqlite3.Row | None:
        cur = self.conn.execute(
            """
            SELECT s.*, c.nome AS cinema_nome, c.capacidade AS cinema_capacidade,
                   f.titulo AS filme_titulo, f.duracao_minutos AS filme_duracao
            FROM sessoes s
            JOIN cinemas c ON c.id = s.cinema_id
            JOIN filmes f ON f.id = s.filme_id
            WHERE s.id = ?
            """,
            (sessao_id,),
        )
        return cur.fetchone()

    def update_publico(self, sessao_id: int, publico: int) -> None:
        self.conn.execute(
            "UPDATE sessoes SET publico_registrado = ? WHERE id = ?",
            (publico, sessao_id),
        )
        self.conn.commit()

    def total_por_filme(self, filme_id: int) -> int:
        cur = self.conn.execute(
            "SELECT COALESCE(SUM(publico_registrado), 0) AS total FROM sessoes WHERE filme_id = ?",
            (filme_id,),
        )
        return int(cur.fetchone()["total"])

    def total_por_cinema(self, cinema_id: int) -> int:
        cur = self.conn.execute(
            "SELECT COALESCE(SUM(publico_registrado), 0) AS total FROM sessoes WHERE cinema_id = ?",
            (cinema_id,),
        )
        return int(cur.fetchone()["total"])
