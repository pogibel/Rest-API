from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///practice.db') 
Sesion = sessionmaker(bind = engine)
session = Sesion()

q = session.query(People).filter_by(id = 1)

q = q.filter_by(first_name = "name")



print(q)