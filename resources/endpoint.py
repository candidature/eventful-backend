from flask_restful import Resource, reqparse, request
from flask_cors import  cross_origin
from flask_jwt import jwt_required
from models.endpoint import EndpointModel

from models.association import AssociationModel



class Endpoint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('path', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('method', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('data')

    def get_by_name(self, endpoint_name):
        print ("Finding",endpoint_name)
        row = EndpointModel.find_by_name(endpoint_name)

        if(row):
            return row.json()

        return {'message': 'Endpoint does not exists'}


    def get(self, id):
        row = EndpointModel.find_by_id(id)
        if (row):
            print ("A get endpoint" , row.json())
            return row.json()

        return {'message': 'Endpoint does not exists'}


    def post(self, id = None):

        #request_data = request.get_json(force=True)
        print ("Inside POST",request.get_json() )
        request_data = Endpoint.parser.parse_args()

        print("Request data name " , request_data.name)

        em = EndpointModel(None,request_data['name'],request_data['path'],request_data['method'],request_data['data'])


        if EndpointModel.find_by_name(request_data['name']):
            import datetime
            return {'message' : "An endpoint with name '{}'  exists on date: {}  ".format(em.json(), str(datetime.datetime.utcnow())) }, 500  # bad request from client
        try:
            em.insert_or_update()
        except Exception as e:
            print ("Exception ", e)
            return {'message': "An error occured while inserting. add_new_endpoint {}".format(em.json())}, 400 # this is not users fault. - internal server error

        print ("JSON ", em.json())
        return em.json(), 201


    def delete(self, id):
        endpoint = EndpointModel.find_by_id(id)

        if not endpoint:
            return {'message': "endpoint '{}' does not exists".format(id)}, 410

        associated_endpoint = AssociationModel.find_by_endpoint_id(id)
        if associated_endpoint['associations']:
            return {'message': "There is association with this endpoint", 'endpoints': associated_endpoint}, 403
        endpoint.delete()
        return {'message' : "deleted ".format(id)  }, 201


    def put(self, id=None):
        print ("Id received is"+id)
        request_data = Endpoint.parser.parse_args()

        endpoint = EndpointModel.find_by_id(id)
        endpoint_name = request_data['name']
        import datetime
        if endpoint: # endpoint already exists, modify that
            try:
                #EndpointModel.update_endpoint(new_endpoint)
                endpoint.endpoint_name = request_data['name']
                endpoint.path = request_data['path']
                endpoint.method = request_data['method']
                endpoint.data = request_data['data']
                endpoint.insert_or_update()
                return {'endpoint': endpoint.json()}
            except Exception as e:
                print ("Exception updating in put ", e)
                return {'message': 'failed updating endpoint {} in put method'.format(endpoint_name)}
        else: # add new endpoint.
            try:
                print ("This is new endpoint")
                new_endpoint = EndpointModel(None, endpoint_name, request_data['path'],request_data['method'], request_data['data'])
                new_endpoint.insert_or_update()
                return {'endpoint': new_endpoint.json()}
            except Exception as e:
                print ("Exception adding in put", e)
                return {'message': 'failed adding endpoint {} in put method'.format(endpoint_name)}



class EndpointList(Resource):

    def get(self):
        return {'endpoints' : [endpoint.json() for endpoint in EndpointModel.query.all()]}, 200