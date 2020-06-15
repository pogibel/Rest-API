import json
import falcon

from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///practice.db') 
Sesion = sessionmaker(bind = engine)
session = Sesion()

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
        data =json_reader.read(req)

        if data is not None:
            if('data type' not in data):
                resp.status = falcon.HTTP_404
                output = { 'error' : 'plz enter data type'}
            else:
                if(data['data type'] == 'all'):
                    output = self.generate_full_data()
                    print(output)
                else:
                    resp.status = falcon.HTTP_404
                    output = { 'error' : 'not such data type'}
        else:
            resp.status = falcon.HTTP_501  
            output = { 'error' : 'no json data'}  
        resp.body = json.dumps(output)

    @staticmethod
    def generate_full_data():
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
                'first_name' : peop.first_name,
                'last_name' : peop.last_name,
                'position' : peop.position,
                'number' : peop.number,
                'bday' : str(peop.bday),
                'address' : peop.address,
                'gender' : peop.gender
            }
            all_data_list.append(one_peron_data)
            
        output = {'server answer' : all_data_list}
        
        return output

app = falcon.API()
app.add_route('/api/get_data', get_data())