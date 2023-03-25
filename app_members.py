from flask import render_template, request, jsonify, Blueprint

from functions import add_new_member
from models.Member import Member
from models.Skill import Skill
from models.db import Session


members_interface = Blueprint('members_interface', __name__, template_folder='templates')


