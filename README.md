# Exercicio DevOps com FastAPI

Aplicacao simples em FastAPI com o endpoint `GET /hello`.

## Pre-requisitos

- Python 3.12 ou superior

## Configuracao local

Crie e ative um ambiente virtual:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependencias de desenvolvimento:

```bash
python -m pip install -r requirements-dev.txt
```

## Executar a aplicacao

```bash
uvicorn app.main:app --reload
```

Acesse http://127.0.0.1:8000/hello. A resposta esperada e:

```json
{"message":"Hello World"}
```

A documentacao interativa fica disponivel em http://127.0.0.1:8000/docs.

## Executar os testes

```bash
python -m pytest
```

## Executar com Docker

Construa a imagem:

```bash
docker build -t minha-aplicacao:1.0 .
```

Execute o container:

```bash
docker run --rm -p 8000:8000 minha-aplicacao:1.0
```

Acesse http://127.0.0.1:8000/hello.

## Pipeline do GitHub Actions

O workflow em `.github/workflows/docker.yml` e executado em pushes para `main`.
Ele constroi a imagem, testa o endpoint `/hello` em um container e publica a tag
`1.0` no Docker Hub.

Antes do primeiro push, configure estes secrets no repositorio GitHub em
`Settings > Secrets and variables > Actions`:

- `DOCKERHUB_USERNAME`: seu usuario do Docker Hub.
- `DOCKERHUB_TOKEN`: um access token do Docker Hub, em vez da senha.

A imagem publicada tera o formato:

```text
SEU_USUARIO/minha-aplicacao:1.0
```