import json
import falcon

from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

engine = create_engine('sqlite:///practice.db') 
Session = sessionmaker(bind = engine)
session = Session()

class json_reader():
    @staticmethod
    def read(req):
        try:
            json_req = req.stream.read()
            data_req = json.loads(json_req)
        except json.decoder.JSONDecodeError:
            return None
        return data_req

class get_data():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200

        output = {}
        data = json_reader.read(req)

        if data is not None:
            if('data type' not in data):
                resp.status = falcon.HTTP_404
                output = { 'error' : 'plz enter data type'}
            else:
                if(data['data type'] == 'all'):
                    output = self.generate_full_data()
                else:
                    resp.status = falcon.HTTP_404
                    output = { 'error' : 'not such data type'}
        else:
            resp.status = falcon.HTTP_501  
            output = { 'error' : 'no json data'}  
        resp.body = json.dumps(output)

    def generate_full_data(self):
        output = {}
        all_data_list = []
        one_peron_data = {}
        query = session.query(Organization, Branch, Department, People).\
            filter(Organization.id == Branch.organization_id, Branch.id == Department.branch_id, Department.id == People.department_id).order_by(Branch.id)

        for org, bran, dep, peop in query:
            one_peron_data = {
                'organization' : org.name,
                'branch' : bran.name,
                'dep' : dep.name,
                'id' : peop.id,
                'first_name' : peop.first_name,
                'last_name' : peop.last_name,
                'position' : peop.position,
                'number' : peop.number,
                'bday' : str(peop.bday),
                'address' : peop.address,
                'gender' : peop.gender
            }
            all_data_list.append(one_peron_data)

        session.close()
        
        return {'server answer' : all_data_list}

class edit_data():
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_200

        output = {}
        data = json_reader.read(req)

        if data is not None:
            if('add people' not in data and 'edit people' not in data):
                resp.status = falcon.HTTP_404
                output = { 'error' : 'plz enter method'}   
            else:
                if('add people' in data): 
                    people_data = data['add people']
                    output = self.add_people(people_data)
                
                if('edit people' in data): 
                    people_data = data['edit people']
                    output = 'work'
                   # output = self.add_people(people_data)
        else:
            resp.status = falcon.HTTP_501  
            output = { 'error' : 'no json data'}  
        resp.body = json.dumps(output)

    def on_delete(self, req, resp):
        resp.status = falcon.HTTP_200

        output = {}
        data = json_reader.read(req)

        if data is not None:
            if('delete people' not in data):
                resp.status = falcon.HTTP_404
                output = { 'error' : 'plz enter method'}   
            else:
                if('delete people' in data): 
                    people_data = data['delete people']
                    output = self.delete_people(people_data)
        else:
            resp.status = falcon.HTTP_501  
            output = { 'error' : 'no json data'}  
        resp.body = json.dumps(output)

    def add_people(self, people_data):
        error_list = self.check_people_data(people_data)
            
        if(len(error_list) != 0):
            return {"error at adding" : error_list}

        try:
            for id in session.query(func.max(People.id)):
                    max_id = id

            peop = People(
                id = max_id[0]+1, 
                department_id = people_data['department_id'], 
                first_name = people_data['first_name'], 
                last_name = people_data['last_name'],
                position = people_data['position'], 
                number = people_data['number'],
                bday = people_data['bday'], 
                address = people_data['address'],
                gender = people_data['gender']
                )

            session.add(peop)
            session.commit()
            session.close()
            
        except TypeError:
            return {"error" : "type error"}

        return {"server answer" : "people added"}
    
    def delete_people(self, people_data):
        error_list = []

        if('id' not in people_data):
            error_list.append("no id")

        if(len(error_list) != 0):
            return {"error at adding" : error_list}

        try:
            session.query(People).filter(People.id == people_data['id']).delete()
            session.commit()
            session.close()
        except TypeError:
            return {"error" : "type error"}

        return {"server answer" : "people deleted"}

    def check_people_data(self, people_data):
        error_list = []

        if('first_name' not in people_data):
            error_list.append("no first_name")
        if('last_name' not in people_data):
            error_list.append("no last_name")
        if('position' not in people_data):
            error_list.append("no position")
        if('number' not in people_data):
            error_list.append("no number")
        if('bday' not in people_data):
            error_list.append("no bday")
        if('address' not in people_data):
            error_list.append("no address")
        if('gender' not in people_data):
            error_list.append("no gender")
        if('department_id' not in people_data):
            error_list.append("no department_id")

        return error_list

app = falcon.API()
app.add_route('/api/get_data', get_data())
app.add_route('/api/edit_data', edit_data())