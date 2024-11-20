from flask import Blueprint, request
from http import HTTPStatus
from models.role import Role, db

user_bp = Blueprint("role", __name__, url_prefix="/roles")

@user_bp.route("/", methods=["POST"])
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    return {"message": "Role created!"}, HTTPStatus.CREATED