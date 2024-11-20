from flask import Blueprint, request
from http import HTTPStatus
from sqlalchemy import inspect
from extensions import bcrypt


user_bp = Blueprint("post", __name__, url_prefix="/posts")