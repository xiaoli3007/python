#coding=utf-8
from itsdangerous import URLSafeTimedSerializer

from app import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])