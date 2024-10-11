# API para Parametrização de Gerador de Alertas
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&labelColor=11111b&color=B5E8E0&logoColor=e0e0e0)

Application Programming Interface (API) desenvolvida em Django REST Framework que é responsável pela parametrização de perfis de alerta para um sistema de notificação de inteligência contra ameaças cibernéticas (Cyber Threat Intelligence). O sistema monitora postagens colhidas de fóruns da surface e dark web, analisando essas informações para identificar potenciais ameaças. A API permite que os usuários configurem perfis de alerta personalizados, definindo critérios como palavras-chave, origem das postagens e nível de criticidade, assegurando que as notificações sejam direcionadas de forma eficiente.

## Sumário

* [Visão Geral](#visao-geral)
* [Autenticação](#autenticacao)
    * [Refresh Token](#refresh)
    * [Access Token](#access)
* [Pacotes](#pacotes)
* [Tabelas](#tabelas)
* [Endpoints](#endpoints)


<a id="visao-geral"></a>

## Visão Geral

A API tem como objetivo permitir a criação de perfis personalizados para a geração de alertas de ameaças cibernéticas com base em configurações definidas pelos usuários. Esses perfis possibilitam a definição de critérios como palavras-chave, fonte das postagens e percentual de relevância em relação à ameaça cibernética (esse valor é calculado por outra parte do projeto). Dessa forma, o sistema garante que os alertas emitidos sejam ajustados conforme as necessidades específicas, oferecendo maior precisão e eficiência no monitoramento de potenciais riscos cibernéticos.


<a id="autenticacao"></a>

## Autenticação

A autenticação na API será baseada no uso de JSON Web Tokens (JWT). O processo começa quando o usuário, previamente cadastrado e com as permissões apropriadas, envia suas credenciais para a API. Em resposta, a API gera dois tokens: um Access Token e um Refresh Token. O Access Token concede acesso temporário a recursos protegidos, enquanto o Refresh Token é utilizado para renovar o Access Token sem a necessidade de um novo login, facilitando o gerenciamento de sessões.

<a id="refresh"></a>

### Refresh Token

O Refresh Token tem um tempo de vida mais longo em comparação ao Access Token e é usado exclusivamente para gerar novos Access Tokens quando este expira. Enquanto o Refresh Token estiver válido, ele permite que o usuário continue autenticado sem precisar submeter suas credenciais novamente. Esse token é ideal para manter sessões de usuário ativas por períodos prolongados, garantindo uma experiência de uso contínua e segura.

<a id="access"></a>

### Access Token

O Access Token tem um tempo de vida curto e é utilizado para acessar recursos específicos da API que requerem autenticação. Cada requisição a esses endpoints protegidos deve incluir o Access Token no cabeçalho de autorização. Esse token garante que apenas usuários autenticados e autorizados possam realizar operações nos recursos sensíveis da API. Quando o Access Token expira, o cliente pode solicitar um novo usando o Refresh Token.


<a id="pacotes"></a>

## Pacotes

A base para o desenvolvimento da API foi o Django REST Framework, os demais pacotes estão listados em `requirements.txt`.


<a id="tabelas"></a>

## Tabelas


<a id="endpoints"></a>

## Endpoints