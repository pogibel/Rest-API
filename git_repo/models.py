from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///practice.db') 

class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer,primary_key = True)
    name = Column(String(40))

class Branch(Base):
    __tablename__ = 'branches'

    id = Column(Integer,primary_key = True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    name = Column(String(40))

    organization = relationship("Organization", uselist = False)

Organization.branches = relationship("Branch", back_populates = "organization")

class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer,primary_key = True)
    branch_id = Column(Integer, ForeignKey('branches.id'))
    name = Column(String(40))

    branch = relationship("Branch", uselist = False)

Branch.departments = relationship("Department", back_populates = "branch")

class People(Base):
    __tablename__ = 'peoples'

    id = Column(Integer, primary_key = True, autoincrement = True)
    department_id = Column(Integer, ForeignKey('departments.id'))
    first_name = Column(String(20))
    last_name = Column(String(30))
    position = Column(String(20))
    number = Column(String(15))
    bday = Column(String(15))
    address = Column(String(100))
    gender = Column(String(20))

    department = relationship("Department", uselist = False)
  
Department.peoples = relationship("People", back_populates = "department")  

Base.metadata.create_all(bind = engine)