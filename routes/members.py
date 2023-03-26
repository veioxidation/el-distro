from flask import Flask, render_template, request, jsonify, Blueprint

from create_engine import DB_URI
from functions import *
from models.db import Session

members_bp = Blueprint('members', __name__)

# MEMBERS
@members_bp.route('/members', methods=['GET'])
def members():
    with Session() as s:
        members = s.query(Member).all()
        skills = s.query(Skill).all()
        return render_template('members.html', members=members, skills=skills)


@members_bp.route('/add_member', methods=['POST'])
def add_member():
    member_name = request.form['name']
    member_email = request.form['email']
    member_skills = request.form.getlist('skills')
    member_capacity = int(request.form['capacity'])

    if not all([member_name, member_email, member_skills, member_capacity]):
        return jsonify({'error': 'Missing fields'}), 400

    # Check if member with the same email already exists
    with Session() as s:
        try:
            new_member = add_new_member(s,
                                        name=member_name,
                                        email=member_email,
                                        skill_id_list=member_skills,
                                        capacity=member_capacity)

            # Render the new member row and return it
            # new_member_row = render_template('member_row.html', member=new_member)

            return jsonify(success=True, member={'id': new_member.id,
                                                 'name': new_member.name,
                                                 'capacity': new_member.capacity,
                                                 'skills_list': new_member.skills_list}, )
        except Exception as e:
            # Handle any errors that occur during the database operation
            s.rollback()
            return jsonify(success=False, error=str(e))


@members_bp.route('/delete_member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    with Session() as s:
        try:
            Member.remove_by_id(s, member_id)
            return jsonify(success=True), 200
        except Exception as e:
            return jsonify(success=False, error="Member not found"), 404

