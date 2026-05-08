
from __future__ import annotations

import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: str | None = None) -> None:
        base_dir = Path(__file__).resolve().parents[2]
        self.db_path = Path(db_path) if db_path else base_dir / "data" / "cinema.db"

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS cinemas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    endereco TEXT NOT NULL,
                    capacidade INTEGER NOT NULL CHECK (capacidade > 0)
                );

                CREATE TABLE IF NOT EXISTS filmes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    genero TEXT NOT NULL,
                    duracao_minutos INTEGER NOT NULL CHECK (duracao_minutos > 0),
                    diretor TEXT NOT NULL,
                    elenco TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS sessoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cinema_id INTEGER NOT NULL,
                    filme_id INTEGER NOT NULL,
                    data TEXT NOT NULL,
                    horario_inicio TEXT NOT NULL,
                    publico_registrado INTEGER NOT NULL DEFAULT 0 CHECK (publico_registrado >= 0),
                    FOREIGN KEY (cinema_id) REFERENCES cinemas(id) ON DELETE CASCADE,
                    FOREIGN KEY (filme_id) REFERENCES filmes(id) ON DELETE CASCADE,
                    UNIQUE (cinema_id, data, horario_inicio)
                );
                """
            )
