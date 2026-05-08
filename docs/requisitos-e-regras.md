# Rede de Cinemas — Requisitos e Regras de Negócio

## Escopo
Sistema de apoio à gestão de uma rede de cinemas, com foco em cadastro de filmes, cinemas, sessões, consulta de programação e registro diário de público.

## Requisitos funcionais principais

**RF01** — Cadastrar cinema com nome, endereço e capacidade.

**RF02** — Cadastrar filme com título, duração, gênero, diretor e elenco.

**RF03** — Cadastrar sessão vinculada a um cinema, uma sala e um filme.

**RF04** — Consultar filmes em cartaz por cinema.

**RF05** — Registrar o público presente em uma sessão em uma data específica.

**RF06** — Consultar total de público por sessão, por filme e por cinema.

**RF07** — Consultar detalhes do filme, incluindo elenco, diretor e gênero.

## Regras de negócio essenciais

**RN01** — Toda sessão deve estar associada a um único cinema, uma única sala e um único filme.

**RN02** — O horário da sessão deve respeitar a duração do filme e o intervalo mínimo entre sessões da mesma sala.

**RN03** — A capacidade de público de uma sessão não pode ultrapassar a capacidade da sala vinculada.

**RN04** — O registro de público deve ser diário e vinculado a uma sessão existente.

**RN05** — O total de público por filme deve ser calculado a partir da soma de todas as sessões associadas ao filme.

**RN06** — O total de público por cinema deve ser calculado a partir da soma de todas as sessões do cinema.

**RN07** — Um filme pode possuir múltiplos gêneros e múltiplos integrantes de elenco.

**RN08** — Um cinema pode possuir várias salas e várias sessões ao longo do dia.
