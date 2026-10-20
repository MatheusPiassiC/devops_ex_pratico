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

Para gerar o relatório de cobertura usado pelo SonarCloud:

```bash
python -m pytest --cov=app --cov-report=xml:coverage.xml
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
`2.0` no Docker Hub.

Antes do primeiro push, configure estes secrets no repositorio GitHub em
`Settings > Secrets and variables > Actions`:

- `DOCKERHUB_USERNAME`: seu usuario do Docker Hub.
- `DOCKERHUB_TOKEN`: um access token do Docker Hub, em vez da senha.

A imagem publicada tera o formato:

```text
SEU_USUARIO/minha-aplicacao:2.0
```

## SAST com SonarCloud

O workflow `.github/workflows/sonarcloud.yml` executa os testes, gera
`coverage.xml` e envia a análise estática para o SonarCloud em pushes para
`main` e em pull requests. O `fetch-depth: 0` preserva o histórico necessário
para o SonarCloud calcular o código novo.

### Configuração no GitHub e no SonarCloud

1. Crie ou importe este repositório no [SonarCloud](https://sonarcloud.io/).
2. Confirme no arquivo `sonar-project.properties` os valores de
   `sonar.projectKey` e `sonar.organization` fornecidos pelo SonarCloud.
3. Gere um token em **SonarCloud > My Account > Security** e salve-o no
   repositório GitHub como `Settings > Secrets and variables > Actions >
   New repository secret`, com o nome `SONAR_TOKEN`.
4. No projeto do SonarCloud, abra **Administration > Analysis Method** e
   desative **Automatic Analysis**. Este projeto usa a análise baseada em CI
   pelo GitHub Actions; os dois modos não podem ser usados simultaneamente.
5. No SonarCloud, selecione o quality gate **Sonar way** (ou um gate próprio)
   e configure, para **código novo**:
   - `New Vulnerabilities = 0`;
   - `New Security Hotspots Reviewed = 100%`;
   - `New Coverage >= 80%` (ajuste o percentual à política da equipe);
   - opcionalmente, `New Bugs = 0` e `New Code Smells = 0`.
6. Em **GitHub > Settings > Branches**, adicione o check do SonarCloud como
   requisito para fazer merge em `main`.

Assim, apontamentos antigos não bloqueiam a equipe: o gate é avaliado contra o
período definido em **Administration > New Code**. Em um pull request, o
SonarCloud compara a alteração com a branch de destino; no `main`, a referência
é a definição de código novo configurada no projeto.

O SAST (Static Application Security Testing) procura vulnerabilidades,
bugs e problemas de qualidade sem executar a aplicação. O `pytest` valida o
comportamento, o `pytest-cov` mede quais linhas foram exercitadas e o
`sonarqube-scan-action` envia o código e a cobertura para o SonarCloud. O
`sonar.qualitygate.wait=true` faz o job aguardar o resultado do gate e falhar
quando os critérios forem reprovados.

## SCA com Trivy

O workflow `.github/workflows/trivy.yml` executa duas verificações:

- uma varredura do repositório (`fs`) para vulnerabilidades em dependências,
  secrets acidentalmente versionados e problemas de configuração;
- uma varredura da imagem Docker construída no próprio runner, incluindo os
  pacotes do sistema operacional da imagem base.

O relatório completo é gerado em SARIF e enviado para **GitHub >
Security > Code scanning alerts**. Esse relatório não bloqueia o pipeline.

A etapa `Verificacao bloqueante da imagem` bloqueia o workflow somente para
vulnerabilidades `HIGH` e `CRITICAL` que tenham correção disponível:

```yaml
severity: CRITICAL,HIGH
ignore-unfixed: true
exit-code: "1"
```

`ignore-unfixed: true` é importante: uma vulnerabilidade sem versão corrigida
não pode ser resolvida apenas interrompendo o build. Nesse caso, avalie a
exposição, atualize a imagem base quando possível, aplique uma mitigação ou
registre uma exceção com prazo.

As vulnerabilidades `LOW` e `MEDIUM` aparecem no relatório, mas não bloqueiam
o desenvolvimento. Essa régua evita que o pipeline fique vermelho por
problemas de menor impacto antes de a equipe tratar o legado.

O workflow constrói a imagem com a tag do commit:

```text
minha-aplicacao:${{ github.sha }}
```

Por isso, ele não depende de `DOCKERHUB_USERNAME` ou `DOCKERHUB_TOKEN` e pode
ser executado em pull requests. A publicação da imagem continua sendo
responsabilidade do workflow `docker.yml`.
