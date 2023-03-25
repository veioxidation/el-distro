from models.Assignment import Assignment
from models.Member import Member
from models.MemberSkills import member_skills
from models.Project import Project
from models.Skill import Skill
from models.db import Session

with Session() as s:
    # s.query(member_skills).delete()
    s.query(Assignment).delete()
    s.query(Member).delete()
    s.query(Project).delete()
    s.query(Skill).delete()
    s.commit()
