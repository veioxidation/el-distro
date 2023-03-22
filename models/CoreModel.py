from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.exc import IntegrityError

from create_engine import Base


class CoreModel(Base):
    __abstract__ = True

    uploaded = Column(DateTime, default=datetime.utcnow())

    @classmethod
    def query_by_id(cls, s, _id):
        try:
            return s.query(cls).filter_by(id=_id).first()
        except IntegrityError:
            # Handle any database errors that may occur
            s.rollback()
            raise ValueError(f'Invalid ID of {cls.__tablename__}')

    @classmethod
    def query_all(cls, s):
        return s.query(cls).all()

    @classmethod
    def add(cls, s, **kwargs):
        i = cls(**kwargs)
        s.add(i)
        s.commit()
        return i

    @classmethod
    def update_value(cls, s, _id, name, value):
        i = cls.query_by_id(s, _id)
        if not hasattr(i, name):
            raise ValueError(f'{name} property not found in {cls.__tablename__}')
        try:
            setattr(i, name, value)
            s.commit()
        except IntegrityError:
            # Handle any database errors that may occur
            s.rollback()
            raise ValueError(f'Error setting value ({value}) for ({name}) in the item {_id}')

    @classmethod
    def remove_by_id(cls, s, _id):
        i = cls.query_by_id(s, _id)
        s.delete(i)
        s.commit()

    def json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
