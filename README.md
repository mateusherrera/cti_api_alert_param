# API para Parametrização de Gerador de Alertas
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)&nbsp;
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)&nbsp;
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)&nbsp;
![Postgre](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)&nbsp;
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)&nbsp;
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)&nbsp;


Esta API, desenvolvida com **Django REST Framework (DRF)**, permite a **configuração de perfis de alerta** para um sistema de **inteligência contra ameaças cibernéticas (Cyber Threat Intelligence - CTI)**.

O sistema monitora, com a frequência definida no próprio perfil de alerta, postagens coletadas de fóruns da **surface web** e **dark web**, analisando essas informações para identificar **potenciais ameaças**. A API possibilita que os usuários definam critérios personalizados para os alertas, incluindo:

* **Palavras-chave** encontradas nos post analisados, desde o último alerta;
* **Origem das postagens**, podendo ser de fóruns da **surface web** e/ou **dark web**;
* **Relevância** da ameaça detectada na postagem.

Dessa forma, o mecanismo de notificação é direcionado, garantindo que os usuários recebam **alertas relevantes e adaptados às suas necessidades**.


## Sumário

* [Visão Geral](#visão-geral)
* [Preparando ambiente](#preparando-ambiente)
    * [Instalação do Docker](#instalação-do-docker)
    * [Configuração das variáveis de ambiente](#configuração-das-variáveis-de-ambiente)
    * [Gerando a `SECRET_KEY` do Django](#gerando-a-secret_key-do-django)
    * [Iniciando Docker](#iniciando-docker)
    * [Criando e instalando requirements (sem docker)](#criando-e-instalando-requirements-sem-docker)
* [Autenticação](#autenticação)
    * [Criando um superusuário](#criando-um-superusuário)
    * [Acessando o painel administrativo](#acessando-o-painel-administrativo)
    * [Autenticação nas requisições](#autenticação-nas-requisições)
* [Endpoints](#endpoints)


## Visão Geral

A API permite a criação de **perfis personalizados** para a geração de **alertas de ameaças cibernéticas**, com base em configurações definidas pelos usuários. Cada perfil possibilita a especificação de critérios como **palavras-chave**, **fonte das postagens** e **percentual de relevância da ameaça** (percentual calculado pelo modelo treinado nas outras partes do projeto).

Dessa forma, o sistema assegura que os alertas emitidos sejam **precisos e adaptados às necessidades específicas de cada usuário**, aumentando a eficiência no monitoramento e na detecção de potenciais riscos cibernéticos.


## Preparando ambiente
### Instalação do Docker

O primeiro passo e instalar e configurar o Docker.
* No Windows, siga as instruções para configurar o Docker com WSL 2: [Docker com WSL 2](https://docs.docker.com/desktop/features/wsl/#turn-on-docker-desktop-wsl-2)
* No Ubuntu, siga as instruções para instalar o Docker de maneira oficial: [Docker no Ubuntu](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

No Ubuntu, instale também o `docker-compose`:
```sh
sudo apt-get install docker-compose -y
```

Além disso, lembre de adicionar ser usuário ao grupo do Docker:
```sh
sudo usermod -aG docker $USER
```

Para verificar se a alteração foi aplicada corretamente, execute:
```sh
groups $USER
```

### Configuração das variáveis de ambiente

Agora, é necessário definir algumas variáveis de ambiente para o funcionamento da API.

Na pasta `api/` crie um arquivo `.env` e adicione o seguinte conteúdo:
obs: É necessário remover os comentário apos as variáveis (os que estão marcados com `*` no início)

```sh
# Ambiente
ENV                     ='dev' # * Opções: 'dev' ou 'prod'
SECRET_KEY              ='chave_gerada_pelo/para_django'
ALLOWED_HOSTS           ='hosts,separados,por,virgula'
CORS_ORIGIN_WHITELIST   ='cors,separados,por,vírgula'

# Database
POSTGRES_DB         = 'nome_do_database' # * Criado automaticamente pelo docker-compose
POSTGRES_HOST       = 'db' # * Nome do container do PostgreSQL no docker-compose
POSTGRES_PORT       = 'porta_do_banco'
POSTGRES_USER       = 'usuario_para_db' # * Criado automaticamente pelo docker-compose
POSTGRES_PASSWORD   = 'senha_para_usario' # * Criado automaticamente pelo docker-compose
```

### Gerando a `SECRET_KEY` do Django

Para gerar uma chave segura, execute o seguinte comando Python (obs: com o Django instalado)

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Copie o valor gerado e substitua `chave_gerada_pelo/para_django` no arquivo `.env`.

### Iniciando Docker

Com tudo configurado, inicie os serviços do Docker:
```sh
docker-compose up -d
```

Reiniciando container após alterações no código:
```sh
docker-compose restart nome_do_container
```

Se precisar recriar os container
```sh
docker-compose down
docker-compose up -d
```

Para remover todas as imagens do Docker:
```sh
docker-compose down --rmi all
```

### Criando e instalando requirements (sem docker)

Para rodar o projeto localmente sem utilizar Docker, siga os passos abaixo para configurar o ambiente virtual e instalar as dependências do projeto.

#### Criando um ambiente virtual

No terminal, navegue até o diretório do projeto e crie um ambiente vitual python.
No Windows `python -m venv venv`. No Linux `python3 -m venv venv`.

#### Ativando o ambiente virtual

No Windows `.\venv\Scripts\activate`. No Linux `source venv/bin/activate`.

#### Instalando dependências

Com o ambiente virtual ativado, instale as dependências necessárias usando o arquivo `requirements.txt` (na pasta `api/`), com o comando: `pip install -r requirements.txt`.


## Autenticação

Para acessar e gerenciar usuários, permissões e grupos na API, utilize um superusuário no painel administrativo do Django.

### Criando um superusuário

Execute o seguinte comando no terminal para criar um superusuário no ambiente Docker:
```sh
docker-compose exec api python manage.py createsuperuser
```

Ou, apenas `python manage.py createsuperuser`, caso não estiver no container.

Depois basta preencher os dados solicitados.

### Acessando o painel administrativo

Com a aplicação rodando (exemplo em localhost, porta 8877) acesse: http://localhost:8877/admin

No painel, você pode:
* Criar novos usuário;
* Definir permissões;
* Gerenciar acessos;
* Manipular dados, entre outros.

### Autenticação nas requisições

A API utiliza **Basic Authentication**, onde as credenciais são os mesmos usuários cadastrados no Django Admin.

Para autenticar, envie no **cabeçalho da requisição** o seguinte:
```sh
Authorization: Basic base64(usuario:senha)
```

Onde `base64(usuario:senha)` e o usuario e a senha convertido em base 64 no formato `usuario:senha`.

* Exemplo:
`curl -u usuario:senha http://localhost:8877/api/v1/endpoint/`


## Endpoints
