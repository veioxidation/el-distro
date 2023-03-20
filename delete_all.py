from models.Assignment import Assignment
from models.Member import Member
from models.MemberSkillsets import member_skillsets
from models.Project import Project
from models.Skillset import Skillset
from models.db import Session

with Session() as s:
    # s.query(member_skillsets).delete()
    s.query(Assignment).delete()
    s.query(Member).delete()
    s.query(Project).delete()
    s.query(Skillset).delete()
    s.commit()
