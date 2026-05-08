
from __future__ import annotations

from app.controllers import CinemaController, FilmeController, SessaoController
from app.db import Database
from app.repositories import CinemaRepository, FilmeRepository, SessaoRepository
from app.services import CinemaService, FilmeService, SessaoService
from app.view import AppView


def build_app() -> AppView:
    db = Database()
    with db.connect() as conn:
        cinema_repo = CinemaRepository(conn)
        filme_repo = FilmeRepository(conn)
        sessao_repo = SessaoRepository(conn)

        cinema_service = CinemaService(cinema_repo)
        filme_service = FilmeService(filme_repo)
        sessao_service = SessaoService(sessao_repo, cinema_repo, filme_repo)

        cinema_controller = CinemaController(cinema_service)
        filme_controller = FilmeController(filme_service)
        sessao_controller = SessaoController(sessao_service)

    return AppView(db, cinema_controller, filme_controller, sessao_controller)


if __name__ == "__main__":
    build_app().run()
