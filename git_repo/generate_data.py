from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import random
from mimesis import Person
from mimesis import Address
from mimesis import Datetime
from mimesis.enums import Gender

dateTime = Datetime('ru')
address = Address('ru')
person = Person('ru')

count_org = 1
count_bran = 3
count_dep = 10
count_peop = 150    

positions = ['position0', 'position1','position2','position3','position4', 'position5']
gender = [Gender.MALE, Gender.FEMALE]

def gen_number():
    result = str(random.randrange(100,999)) + '-' + str(random.randrange(10,99)) + '-' + str(random.randrange(10,99))
    return result

engine = create_engine('sqlite:///practice.db') 
Sesion = sessionmaker(bind = engine)
session = Sesion()

for i in range(count_org):
    org = Organization(id = i, name = 'Организация' + str(i))
    session.add(org)
    session.commit()

for i in range(count_bran):
    brabn = Branch(id = i, organization_id = random.randrange(count_org), name = 'Фелиал' + str(i))
    session.add(brabn)
    session.commit()

for i in range(count_dep):
    dep = Department(id = i, branch_id = random.randrange(count_bran), name = 'Отдел' + str(i))
    session.add(dep)
    session.commit()

for i in range(count_peop):
    gender0 = gender[random.randrange(len(gender))]

    peop = People(
        id = i, 
        first_name = person.first_name(gender = gender0), 
        last_name = person.last_name(gender = gender0),
        department_id = random.randrange(count_dep), 
        position = positions[random.randrange(len(positions))],
        number = gen_number(),
        bday = dateTime.date(start = 1970, end = 2002),
        address = address.address(),
        gender = gender0.name
        )
    session.add(peop)
    session.commit()

session.close()