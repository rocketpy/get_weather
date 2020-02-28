from flask import Blueprint
from get_weather.auth import auth


bp = Blueprint('auth', __name__)
