
from __future__ import annotations

from .controllers import CinemaController, FilmeController, SessaoController
from .db import Database
from .repositories import CinemaRepository, FilmeRepository, SessaoRepository


class AppView:
    def __init__(
        self,
        db: Database,
        cinema_controller: CinemaController,
        filme_controller: FilmeController,
        sessao_controller: SessaoController,
    ) -> None:
        self.db = db
        self.cinema_controller = cinema_controller
        self.filme_controller = filme_controller
        self.sessao_controller = sessao_controller

    def run(self) -> None:
        self.db.initialize()
        while True:
            self._menu()
            op = input("Escolha uma opção: ").strip()
            try:
                if op == "1":
                    self._cadastrar_cinema()
                elif op == "2":
                    self._listar_cinemas()
                elif op == "3":
                    self._cadastrar_filme()
                elif op == "4":
                    self._listar_filmes()
                elif op == "5":
                    self._cadastrar_sessao()
                elif op == "6":
                    self._listar_sessoes()
                elif op == "7":
                    self._registrar_publico()
                elif op == "8":
                    self._consultar_total_por_filme()
                elif op == "9":
                    self._consultar_total_por_cinema()
                elif op == "0":
                    print("Encerrando...")
                    break
                else:
                    print("Opção inválida.")
            except Exception as exc:
                print(f"Erro: {exc}")

    def _menu(self) -> None:
        print("\n=== Rede de Cinemas ===")
        print("1 - Cadastrar cinema")
        print("2 - Listar cinemas")
        print("3 - Cadastrar filme")
        print("4 - Listar filmes")
        print("5 - Cadastrar sessão")
        print("6 - Listar sessões")
        print("7 - Registrar público da sessão")
        print("8 - Total de público por filme")
        print("9 - Total de público por cinema")
        print("0 - Sair")

    def _cadastrar_cinema(self) -> None:
        nome = input("Nome: ")
        endereco = input("Endereço: ")
        capacidade = input("Capacidade: ")
        novo_id = self.cinema_controller.criar(nome, endereco, capacidade)
        print(f"Cinema cadastrado com ID {novo_id}.")

    def _listar_cinemas(self) -> None:
        with self.db.connect() as conn:
            rows = CinemaRepository(conn).list_all()
        for row in rows:
            print(dict(row))

    def _cadastrar_filme(self) -> None:
        titulo = input("Título: ")
        genero = input("Gênero: ")
        duracao = input("Duração em minutos: ")
        diretor = input("Diretor: ")
        elenco = input("Elenco: ")
        novo_id = self.filme_controller.criar(titulo, genero, duracao, diretor, elenco)
        print(f"Filme cadastrado com ID {novo_id}.")

    def _listar_filmes(self) -> None:
        with self.db.connect() as conn:
            rows = FilmeRepository(conn).list_all()
        for row in rows:
            print(dict(row))

    def _cadastrar_sessao(self) -> None:
        cinema_id = input("ID do cinema: ")
        filme_id = input("ID do filme: ")
        data = input("Data (YYYY-MM-DD): ")
        horario = input("Horário de início (HH:MM): ")
        novo_id = self.sessao_controller.criar(cinema_id, filme_id, data, horario)
        print(f"Sessão cadastrada com ID {novo_id}.")

    def _listar_sessoes(self) -> None:
        with self.db.connect() as conn:
            rows = SessaoRepository(conn).list_all()
        for row in rows:
            print(dict(row))

    def _registrar_publico(self) -> None:
        sessao_id = input("ID da sessão: ")
        quantidade = input("Quantidade de espectadores: ")
        self.sessao_controller.registrar_publico(sessao_id, quantidade)
        print("Público registrado com sucesso.")

    def _consultar_total_por_filme(self) -> None:
        filme_id = int(input("ID do filme: "))
        with self.db.connect() as conn:
            total = SessaoRepository(conn).total_por_filme(filme_id)
        print(f"Total de público do filme {filme_id}: {total}")

    def _consultar_total_por_cinema(self) -> None:
        cinema_id = int(input("ID do cinema: "))
        with self.db.connect() as conn:
            total = SessaoRepository(conn).total_por_cinema(cinema_id)
        print(f"Total de público do cinema {cinema_id}: {total}")
