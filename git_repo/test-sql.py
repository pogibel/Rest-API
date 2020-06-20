from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from sqlalchemy import and_
    
engine = create_engine('sqlite:///practice.db') 
Sesion = sessionmaker(bind = engine)
session = Sesion()

a = 10
gender = 'FEMALE'
filters = [People.id.ilike('%' + str(a) + '%'), People.gender.like(gender)]
 
query = session.query(Organization, Branch, Department, People).filter(Organization.id == Branch.organization_id, Branch.id == Department.branch_id, Department.id == People.department_id).filter(and_(*filters))
 





for org, bran, dep, peop in query:
    print(org.id, org.name, bran.id, bran.name, dep.id, dep.name, peop.id, peop.first_name, peop.gender)

#print(query)