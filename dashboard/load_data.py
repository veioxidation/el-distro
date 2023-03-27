import pandas as pd

from models.Assignment import Assignment
from models.Member import Member
from models.Project import Project
from models.Skill import Skill
from models.db import Session


def load_data():
    with Session() as s:
        # Get All Datasets as a dictionary of Data Frames
        return {do.__name__:pd.read_sql(s.query(do).statement, s.bind) for do in [Member, Skill, Assignment, Project]}

if __name__ == '__main__':
    x = load_data()
    print('Data Loaded')



