# Projeto API Flask: Gerenciamento de Usuários

Este projeto consiste em uma API desenvolvida com o micro-framework Flask, que utiliza um banco de dados SQLite para gerenciar usuários e níveis de acesso. A API oferece funcionalidades completas de CRUD (Criar, Ler, Atualizar, Deletar) para a gestão de usuários, permitindo a criação de novos registros, a consulta e atualização de informações dos usuários cadastrados, e a exclusão de usuários. Cada usuário possui um nível de acesso atribuído, o que permite controlar o acesso a funcionalidades específicas da aplicação. A integração com Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended, Flask-Bcrypt e Flask-Marshmallow proporciona uma estrutura robusta para a implementação de segurança, serialização de dados e migrações de banco de dados.

Abaixo estão descrições das principais bibliotecas utilizadas, comandos essenciais e links para a documentação oficial.

## Bibliotecas Utilizadas

### 1. Flask
**Descrição**: Flask é um micro-framework web para Python, que facilita a criação de APIs e sites. Ele é simples, flexível e oferece uma boa base para criar aplicações web escaláveis.

**Principais Comandos**:
- `flask run`: Inicia o servidor de desenvolvimento da aplicação Flask.
- `flask shell`: Abre um shell interativo com o contexto do aplicativo carregado.
- `flask --app src/app run --debug`: Comando para rodar a aplicação no terminal com o modo debug ativado. A estrutura para o run segue o modelo do projeto.
- `flask routes`: Lista todas as rotas registradas na aplicação.
- `flask test`: Executa os testes da aplicação.
- `flask create-db` (personalizado):
   Muitas vezes, os desenvolvedores criam comandos personalizados para operações específicas, como criar o banco de dados. Esses comandos são definidos no código.
```
# Exemplo de implementação:

@app.cli.command("create-db")
def create_db():
    """Cria o banco de dados."""
    db.create_all()
    print("Banco de dados criado!")

# Uso no terminal:
flask create-db
```

- `flask init ou flask init-db` (personalizado): Comando personalizado para inicializar o banco de dados ou outras tarefas de configuração.
```
# Exemplo de implementação:

@app.cli.command("init-db")
def init_db():
    """Inicializa o banco de dados."""
    db.drop_all()
    db.create_all()
    print("Banco de dados inicializado!")

# Uso no terminal:
flask init-db
```

- `flask --help`: Exibe a ajuda com a lista de todos os comandos disponíveis.
- `flask debug`: Ativa o modo de depuração.
- `flask config` (comandos relacionados à configuração): Pode ser usado para inspecionar variáveis de configuração da aplicação.
```
# Exemplo (personalizado):

@app.cli.command("show-config")
def show_config():
    """Exibe as configurações da aplicação."""
    for key, value in app.config.items():
        print(f"{key}: {value}")
```

[Documentação do Flask](https://flask.palletsprojects.com/)


### 2. Flask-SQLAlchemy
**Descrição**: Flask-SQLAlchemy é uma extensão que adiciona suporte a SQLAlchemy, um ORM (Object Relational Mapper), permitindo o uso de banco de dados relacionais de forma mais fácil no Flask.

**Principais Comandos**:
- `db.create_all()`: Cria as tabelas no banco de dados.
- `db.drop_all()`: Remove todas as tabelas do banco de dados.
- `db.session.add()`: Adiciona um novo objeto à sessão.

```
# Exemplo:
user = User(name="João", email="joao@example.com")
db.session.add(user)
db.session.commit()
```
- `db.session.commit()`: Confirma as mudanças no banco de dados.
- `db.session.rollback()`: Reverte todas as alterações pendentes na sessão.
- `db.session.delete()`: Remove um objeto do banco de dados.
```
# Exemplo:
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```
- `Model.query`: Permite consultar objetos no banco de dados.
```
# Como consultar registros:
User.query.all()

# Filtrar registros:
User.query.filter_by(name="João").first()
```

[Documentação do Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)


### 3. Flask-Migrate
**Descrição**: Flask-Migrate é uma extensão para Flask que facilita o gerenciamento de migrações de banco de dados, utilizando Alembic.

**Comandos Principais**:
- `flask db init`: Inicializa o diretório de migrações.
- `flask db migrate -m "Mensagem"`: Gera um novo script de migração com base nas mudanças nos modelos.
- `flask db upgrade`: Aplica as migrações no banco de dados.
- `flask db downgrade`: Reverte as últimas migrações aplicadas.
- `flask db history`: Mostra o histórico de migrações.
- `flask db show`: Exibe a versão atual do banco de dados.
- `flask db stamp`: Marca o banco de dados como atualizado para uma versão específica, sem aplicar as migrações.
- `flask db merge -m "Une ramificações de migração"`: Une várias ramificações de migração em uma única.
- `flask db edit`: Abre o script de migração atual em um editor de texto.

Resumo de Fluxo de Trabalho de Migração:
```
# Crie o diretório de migração:
flask db init

# Detecte alterações nos modelos e gere uma migração:
flask db migrate -m "Descrição da alteração"

# Aplica as alterações ao banco:
flask db upgrade

# Reverte alterações, se necessário:
flask db downgrade
```

Esses comandos cobrem a maioria dos casos de uso no desenvolvimento com Flask-SQLAlchemy e Flask-Migrate.

[Documentação do Flask-Migrate](https://flask-migrate.readthedocs.io/)

### 4. Flask-JWT-Extended
**Descrição**: Flask-JWT-Extended é uma extensão para Flask que facilita a implementação de autenticação com JSON Web Tokens (JWT).

**Comandos Principais**:
- `@jwt_required()`: Protege uma rota, exigindo que o cliente forneça um token JWT válido para acessar o recurso.
Uso:
```
from flask_jwt_extended import jwt_required

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return {"message": "Você acessou um endpoint protegido!"}
```

- `create_access_token(identity)`: Gera um token de acesso (JWT) para o usuário com base no parâmetro identity, que geralmente é um identificador único do usuário (como o ID ou email).
Uso:
```
from flask_jwt_extended import create_access_token
from datetime import timedelta

token = create_access_token(identity="user_id", expires_delta=timedelta(hours=1))
```

- `create_refresh_token(identity)`: Gera um token de "refresh" para permitir que o cliente obtenha novos tokens de acesso sem precisar autenticar novamente.
Uso:
```
from flask_jwt_extended import create_refresh_token

refresh_token = create_refresh_token(identity="user_id")
```

- `@jwt_refresh_token_required` (Deprecated em versões recentes): Exige um token de "refresh" válido para acessar a rota. Em versões recentes, use `@jwt_required(refresh=True)`.
Uso:
```
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return {"access_token": new_access_token}
```

- `get_jwt_identity()`: Recupera a identidade do usuário (identity) armazenada no token JWT.
Uso:
```
from flask_jwt_extended import get_jwt_identity

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    return {"user": current_user}
```

- `get_jwt()`: Retorna todas as informações contidas no token JWT atual, como claims adicionais.
Uso:
```
from flask_jwt_extended import get_jwt

@app.route('/token_info', methods=['GET'])
@jwt_required()
def token_info():
    jwt_data = get_jwt()
    return {"jwt_claims": jwt_data}
```

- `set_access_cookies()`: Configura o token de acesso como um cookie no cliente.
```
from flask_jwt_extended import set_access_cookies

response = jsonify({"message": "Login bem-sucedido!"})
set_access_cookies(response, access_token)
return response
```

- `unset_jwt_cookies()`: Remove os cookies de autenticação, útil para logout.
```
from flask_jwt_extended import unset_jwt_cookies

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"message": "Logout bem-sucedido!"})
    unset_jwt_cookies(response)
    return response
```

- `add_claims_to_access_token(identity)`: Adiciona claims personalizados ao token JWT.
```
from flask_jwt_extended import create_access_token

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {"roles": ["admin", "editor"]}

token = create_access_token(identity="user_id")
```

- `@jwt.token_in_blocklist_loader`: Define uma função para verificar se um token está em uma lista de bloqueio (blacklist), útil para revogar tokens.
```
from flask_jwt_extended import token_in_blocklist

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklisted_tokens
```

**Gerenciamento de Erros**:
- `@jwt.invalid_token_loader`: Personaliza a resposta quando o token é inválido.
```
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"error": "Token inválido"}), 401
```

- `@jwt.unauthorized_loader`: Personaliza a resposta para requisições sem o token.
```
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"error": "Token ausente"}), 401
```

- `@jwt.revoked_token_loader`: Define a resposta para tokens revogados.
```
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token revogado"}), 401
```
- `decode_token()`: Decodifica um token JWT.
  
**Resumo:** Os comandos acima cobrem a criação, validação e personalização do comportamento de tokens JWT, permitindo proteger endpoints, adicionar claims e gerenciar o ciclo de vida do token de forma segura e eficiente.


[Documentação do Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)

### 5. Flask-Bcrypt
**Descrição**: O Flask-Bcrypt é uma extensão do Flask que fornece uma maneira fácil de gerar e verificar hashes de senhas com o algoritmo bcrypt, garantindo segurança no armazenamento de credenciais. Ele protege contra ataques de força bruta e rainbow tables, sendo essencial para autenticação em sistemas seguros.

**Principais Comandos**:
- `bcrypt.generate_password_hash(password, rounds=12)`: Gera um hash seguro a partir de uma senha, utilizando o algoritmo bcrypt.

Parâmetros:
<br>
`password`: A senha em texto simples que será convertida em hash.
<br>
`rounds`(opcional): Número de rodadas para o algoritmo bcrypt (quanto maior, mais seguro, mas também mais lento).

```
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

hashed_password = bcrypt.generate_password_hash("minha_senha_secreta")
print(hashed_password)
# Saída: b'$2b$12$...'
```

- `bcrypt.check_password_hash(hashed_password, password)`: Verifica se uma senha em texto simples corresponde a um hash armazenado.

Parâmetros:
<br>
`hashed_password`: O hash gerado anteriormente (armazenado no banco de dados, por.
<br>
`password`(opcional): A senha em texto simples que será comparada.

```
stored_hash = b'$2b$12$...'  # Hash armazenado no banco de dados
senha_valida = bcrypt.check_password_hash(stored_hash, "minha_senha_secreta")
print(senha_valida)  # True ou False
```

- `bcrypt.init_app(app)`: Inicializa o Flask-Bcrypt com a aplicação Flask. Deve ser usado para integrar o Bcrypt ao projeto.

Parâmetros:
<br>
`app`: A instância do aplicativo Flask.

```
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt()
bcrypt.init_app(app)
```

[Documentação do Flask-Bcrypt](https://flask-bcrypt.readthedocs.io/)

### 6. Flask-Marshmallow
**Descrição**: O Flask-Marshmallow é uma extensão que facilita o processamento de dados em APIs, automatizando a serialização, desserialização e validação. Ele é amplamente utilizado para transformar dados entre objetos Python e formatos JSON.

**Principais Comandos**:
- `ma.init_app(app)`: Inicializa o Flask-Marshmallow com a aplicação Flask.

Parâmetros:
<br>
`app`: A instância do aplicativo Flask.

```
from flask import Flask
from flask_marshmallow import Marshmallow

app = Flask(__name__)
ma = Marshmallow()
ma.init_app(app)
```

- `@ma.Schema`: Cria uma classe de esquema que define como os dados serão serializados (transformados em JSON) ou desserializados (convertidos para objetos Python).

```
from flask_marshmallow import Schema
from marshmallow import fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)
```

- `dump(obj)`: O objeto Python que será serializado.

Parâmetros:
<br>
`obj`: A instância do aplicativo Flask.

```
user = {"id": 1, "username": "john_doe", "email": "john@example.com"}
serialized_user = user_schema.dump(user)
print(serialized_user)  # {'id': 1, 'username': 'john_doe', 'email': 'john@example.com'}
```

- `load(data)`: Desserializa e valida dados recebidos, transformando-os em objetos Python.

Parâmetros:
<br>
`data`: Os dados (como JSON) que serão validados e transformados.

```
input_data = {"username": "jane_doe", "email": "jane@example.com"}
validated_data = user_schema.load(input_data)
print(validated_data)  # {'username': 'jane_doe', 'email': 'jane@example.com'}
```

- `many=True`: Permite processar vários objetos ao mesmo tempo (listas de dados) para serialização ou desserialização.

```
users = [
    {"id": 1, "username": "john_doe", "email": "john@example.com"},
    {"id": 2, "username": "jane_doe", "email": "jane@example.com"}
]
serialized_users = users_schema.dump(users)
print(serialized_users)
# [{'id': 1, 'username': 'john_doe', 'email': 'john@example.com'}, {'id': 2, 'username': 'jane_doe', 'email': 'jane@example.com'}]
```

- `fields (de marshmallow)`: Define os campos e tipos esperados no esquema.

`fields.Int`: Inteiro.

`fields.Str`: String.

`fields.Email`: Validação de e-mail.

`fields.Bool`: Booleano.

<br>

```
class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    in_stock = fields.Bool()
```

[Documentação do Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/)

### Como Funciona no Código?
As bibliotecas são inicializadas e configuradas no arquivo principal da aplicação (app.py) utilizando os métodos .init_app() para conectá-las à instância do Flask, garantindo que suas funcionalidades estejam disponíveis em toda a aplicação.

```
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()

# Configurações e inicialização
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
migrate.init_app(app, db)
jwt.init_app(app)
bcrypt.init_app(app)
ma.init_app(app)
```

## Como Instalar as Bibliotecas?

Para instalar todas as bibliotecas necessárias para o projeto, siga os passos abaixo:

1. **Criação do Ambiente Virtual** (se ainda não estiver criado):
   ```
   python -m venv .venv
   ```
   
2. **Ativação do Ambiente Virtual**:
   - No Windows:
   ```
   .venv\Scripts\activate
    ```
   - No Linux/macOS:
   ```
   source .venv/bin/activate
   ```
   
3. **Instalação das Dependências**:
```
   pip install flask
   pip install flask-sqlalchemy
   pip install flask-migrate
   pip install flask-jwt-extended
   pip install flask-bcrypt
   pip install flask-marshmallow
   pip install marshmallow-sqlalchemy
```

💡 ***O que é o pip?***
<br>
O **pip** é o gerenciador de pacotes padrão do Python. Ele permite instalar, atualizar e gerenciar bibliotecas e dependências diretamente do Python Package Index (PyPI) ou de outras fontes. Com o pip, você pode integrar facilmente ferramentas e bibliotecas ao seu projeto.

💡 ***Importância do ``.venv`` como Ambiente Virtual.***
<br>
O ambiente virtual (ou virtual environment) é uma ferramenta crucial para o desenvolvimento de projetos em Python. Ele permite criar um ambiente isolado onde você pode instalar bibliotecas específicas para um projeto, sem afetar o sistema ou outros projetos. Isso traz diversas vantagens:

1. Isolamento de dependências: Cada projeto pode ter suas próprias versões de pacotes, sem interferir nas dependências de outros projetos ou do Python global.
2. Facilidade na gestão de dependências: Ao criar um ambiente virtual, você pode controlar facilmente as bibliotecas e versões utilizadas, garantindo que o projeto seja executado de maneira consistente em diferentes máquinas.
3. Segurança e organização: Como as dependências são instaladas de forma isolada, você reduz o risco de conflitos entre bibliotecas e garante que seu ambiente de desenvolvimento seja mais seguro e organizado.


## Como Rodar o Projeto?
1. **Iniciar o Servidor Flask**
   Após instalar as dependências, inicie o servidor Flask com o seguinte comando:
   
   ```
   flask run
   ```
2. **Testar os Endpoints da API**
    Use ferramentas como Postman ou Insomnia para testar os endpoints da sua API.


## Uso do Postman

**O que é o Postman?** 
<br>
O Postman é uma ferramenta popular de desenvolvimento e testes de APIs (Interface de Programação de Aplicações). Ela permite aos desenvolvedores enviar requisições HTTP para um servidor e analisar as respostas de maneira fácil e interativa. O Postman é usado para testar APIs RESTful, mas também pode ser utilizado para trabalhar com SOAP, GraphQL, e outros tipos de APIs.

#### Funcionalidades Principais do Postman:
- Envio de Requisições HTTP: Você pode enviar diferentes tipos de requisições (GET, POST, PUT, DELETE, etc.) para testar as rotas da sua API.
- Coleções: Permite organizar diferentes requisições em "coleções", facilitando o agrupamento de endpoints e testes para projetos inteiros.
- Testes Automáticos: Oferece suporte para scripts que permitem verificar automaticamente a validade das respostas, como status HTTP, estrutura dos dados, ou valores de resposta.
- Documentação de API: Permite gerar e compartilhar documentação automaticamente a partir das requisições e coleções.
- Ambientes e Variáveis: Suporte para variáveis globais e de ambiente, permitindo testar diferentes configurações, como URLs ou tokens de autenticação, de maneira flexível.
   
***Como o Postman se Integra ao Projeto de API Flask?***
<br>
O Postman é uma ferramenta excelente para testar e depurar APIs Flask de forma independente, sem a necessidade de integrar diretamente ao código da aplicação. Aqui estão algumas maneiras de como o Postman se integra a um projeto de API Flask:

1. Testando Endpoints da API
- *Configuração de Requisição:* No Postman, você pode configurar o tipo de requisição HTTP (GET, POST, PUT, DELETE, etc.), adicionar cabeçalhos (headers), parâmetros de consulta (query parameters), e o corpo da requisição (request body).
- *Envio de Requisição:* Após configurar a requisição, você pode enviar o pedido ao servidor Flask e visualizar a resposta (status, dados, etc.).
- *Exemplo de Requisição GET:*
  - `URL`: http://localhost:5000/api/user
  - `Método`: GET
  - `Resposta`: O Postman exibirá os dados retornados pela API, como JSON ou outro formato.

2. Testando Autenticação (JWT, por exemplo)
Se a API Flask utiliza JWT (JSON Web Tokens) para autenticação, o Postman pode ser configurado para enviar tokens nas requisições. Isso é feito na aba "Authorization" do Postman, onde você pode definir um tipo de autenticação como Bearer Token e fornecer o token gerado pela sua API Flask.

3. Testando o Fluxo de CRUD
- **Create:** Teste as rotas POST da API para criar recursos no banco de dados.
- **Read:** Teste as rotas GET para obter dados de recursos existentes.
- **Update:** Teste as rotas PUT ou PATCH para modificar dados de recursos.
- **Delete:** Teste as rotas DELETE para remover recursos.

4. Simulando Diferentes Cenários
- O Postman permite testar diferentes cenários enviando dados variados (como parâmetros diferentes ou corpos de requisição com formatos distintos) e observando como a API Flask reage.
- Você pode simular falhas no envio de dados e verificar se os erros são tratados corretamente, retornando os códigos de status apropriados, como 400 (Bad Request), 404 (Not Found), 500 (Internal Server Error), entre outros.
  
5. Automação de Testes
O Postman permite escrever scripts de testes automatizados. Por exemplo, após enviar uma requisição, você pode validar se o status da resposta é o esperado, ou se o corpo da resposta contém valores específicos.

6. Importação e Exportação de Coleções
As coleções de requisições podem ser exportadas do Postman e compartilhadas com outros desenvolvedores ou membros da equipe. Isso facilita o trabalho colaborativo ao testar e debugar a API.
- Você pode exportar coleções em formato JSON e importar em outras instâncias do Postman ou compartilhá-las com a equipe de desenvolvimento.
  
7. Integração com Ambiente de Desenvolvimento
O Postman pode ser integrado com o ambiente de desenvolvimento de uma API Flask para testar rapidamente as modificações feitas no código sem precisar escrever novos scripts de teste. Por exemplo, se você modificar uma rota ou funcionalidade no Flask, pode imediatamente testar essa alteração utilizando o Postman.

#### Como Usar o Postman com Flask? 
1. **Inicie o Servidor Flask:** Execute o servidor Flask no terminal:
```
flask run
```
2. **Abra o Postman e Configure uma Requisição:**
- Selecione o tipo de requisição (GET, POST, etc.).
- Insira a URL do endpoint da API (por exemplo, http://localhost:5000/api/user).
- Se necessário, adicione parâmetros, cabeçalhos, ou corpo da requisição.

3. **Envie a Requisição:** Clique em "Send" para enviar a requisição. O Postman exibirá a resposta da API.

4. **Análise da Resposta:** O Postman mostrará o código de status da resposta, os dados retornados e os tempos de resposta. Se a API retornar erros, você poderá identificar os problemas na resposta.

## 💻 Tecnologias utilizadas
<p>
  <img width="40" src="https://user-images.githubusercontent.com/25181517/183423507-c056a6f9-1ba8-4312-a350-19bcbc5a8697.png" alt="Python">
  <img width="40" src="https://user-images.githubusercontent.com/25181517/183423775-2276e25d-d43d-4e58-890b-edbc88e915f7.png" alt="Flask" title="Flask">
  <img width="40" src="https://user-images.githubusercontent.com/25181517/192109061-e138ca71-337c-4019-8d42-4792fdaa7128.png" alt="Postman" title="Postman">
</p>


## 📫 Contribuindo 

Para contribuir com esse projeto, ou simplesmente clonar e testar em sua máquina, siga estas etapas:

1. Bifurque este repositório e clone para sua máquina.
2. Crie um branch: `git checkout -b <nome_branch>`.
3. Faça suas alterações e confirme-as: `git commit -m '<mensagem_commit>'`
4. Envie para o branch original: `git push origin <nome_do_projeto> / <local>`
5. Crie a solicitação de pull.

<p align="left">
  Caso queira entrar em contato: ⤵️
</p>

<p align="left">

  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adrianycmc/)
</p>

