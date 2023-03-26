from flask import render_template, request, jsonify, Blueprint

from models.Skill import Skill
from models.db import Session

skills_bp = Blueprint('skills', __name__)


@skills_bp.route('/skills', methods=['GET'])
def skills():
    with Session() as s:
        skills = s.query(Skill).all()
    return render_template('skills.html', skills=skills)


@skills_bp.route('/add_skill', methods=['POST'])
def add_skill():
    skill_name = request.form['name']
    if not all([skill_name]):
        return jsonify(success=False), 400

    # Add new skill
    with Session() as s:
        new_skill = Skill.add(s, name=skill_name)
        return jsonify(success=True,
                       skill={'id': new_skill.id,
                              'name': new_skill.name}), 201


@skills_bp.route('/delete_skill/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    with Session() as s:
        try:
            Skill.remove_by_id(s, skill_id)
            return jsonify(success=True), 200
        except Exception as e:
            return jsonify(success=False, error="Skill not found"), 404


@skills_bp.route('/skills', methods=['GET'])
def get_all_skills():
    with Session() as s:
        resp = [skill.json() for skill in s.query(Skill).all()]

    return jsonify(resp), 200
