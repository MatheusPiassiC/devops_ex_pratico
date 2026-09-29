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