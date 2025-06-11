# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Judge(db.Model):

    __tablename__ = 'Judge'

    id = db.Column(db.Integer, primary_key=True)

    #__Judge_FIELDS__
    name = db.Column(db.String(255),  nullable=True)
    pin = db.Column(db.String(255),  nullable=True)

    #__Judge_FIELDS__END

    def __init__(self, **kwargs):
        super(Judge, self).__init__(**kwargs)


class Entry(db.Model):

    __tablename__ = 'Entry'

    id = db.Column(db.Integer, primary_key=True)

    #__Entry_FIELDS__
    description = db.Column(db.Text, nullable=True)

    #__Entry_FIELDS__END

    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)


class Competition(db.Model):

    __tablename__ = 'Competition'

    id = db.Column(db.Integer, primary_key=True)

    #__Competition_FIELDS__
    is_active = db.Column(db.Boolean, nullable=True)
    start_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    end_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Competition_FIELDS__END

    def __init__(self, **kwargs):
        super(Competition, self).__init__(**kwargs)


class Rubric(db.Model):

    __tablename__ = 'Rubric'

    id = db.Column(db.Integer, primary_key=True)

    #__Rubric_FIELDS__
    question = db.Column(db.String(255),  nullable=True)
    max_score = db.Column(db.Integer, nullable=True)

    #__Rubric_FIELDS__END

    def __init__(self, **kwargs):
        super(Rubric, self).__init__(**kwargs)


class Score(db.Model):

    __tablename__ = 'Score'

    id = db.Column(db.Integer, primary_key=True)

    #__Score_FIELDS__
    value = db.Column(db.Integer, nullable=True)
    submitted_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    #__Score_FIELDS__END

    def __init__(self, **kwargs):
        super(Score, self).__init__(**kwargs)



#__MODELS__END
