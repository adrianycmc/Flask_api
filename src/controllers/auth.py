from flask import Blueprint, request
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import create_access_token
from extensions import bcrypt


user_bp = Blueprint("auth", __name__, url_prefix="/auth")

def _check_password(password_hash, password_raw):
    return bcrypt.check_password_hash(password_hash, password_raw)
   

@user_bp.route("/login", methods=["POST"])
def login():
    from app import User, db
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    if not user or not _check_password(user.password, password):
        return {"message": "Bad username or password"}, HTTPStatus.UNAUTHORIZED


    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token}