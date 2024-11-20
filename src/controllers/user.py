from flask import Blueprint, request
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required
from utils import requires_role
from models.user import User, db
from extensions import bcrypt
from views.user import UserSchema, CreateUserSchema
from marshmallow import ValidationError

user_bp = Blueprint("user", __name__, url_prefix="/users")

def _create_user():
    user_schema = CreateUserSchema()
    try:
        data = user_schema.load(request.json) 
    except ValidationError as err:
        return err.messages, HTTPStatus.UNPROCESSABLE_ENTITY
    
    user = User(username=data["username"], password=bcrypt.generate_password_hash(data["password"]),role_id=data["role_id"])
    db.session.add(user)
    db.session.commit()
    
def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    users_schema = UserSchema(many=True)
    return users_schema.dump(users)
    

# Criação e Listagem de usuários
@user_bp.route("/", methods=["GET", "POST"])
@jwt_required()
# O decorador define quem tem o acesso
@requires_role("admin")
def list_or_create_user():
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}

# Listagem por ID    
@user_bp.route("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {"id": user.id, "username": user.username}

# PATH atualiza um atributo por vez
@user_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json
    
    # Update dinâmico
    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()
    
    return {"id": user.id, "username": user.username}

@user_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT