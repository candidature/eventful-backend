from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.runtime import RuntimeModel

from models.association import AssociationModel

class Runtime(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank")  # local/remote/dockerfile
    parser.add_argument('type', type=str, required=True, help="This field cannot be left blank") # local/remote/dockerfile

    parser.add_argument('dockerfile')
    parser.add_argument('user_name')
    parser.add_argument('user_password')
    parser.add_argument('user_hostname')

    parser.add_argument('error')

    def get(self, id=None):
        print ("Finding",id)
        row = RuntimeModel.find_by_id(id)

        if(row):
            return row.json()

        return {'message': 'Runtime with id {} does not exists'.format(id)}


    #def __init__(self, runtime_name, type, user_name=None, user_password=None, dockerfile=None, error=None):
    def post(self,id=None):
        print (RuntimeModel.find_by_id(id))
        if RuntimeModel.find_by_id(id):
            import datetime
            return {'message': "A runtime with id '{}' already exists  , on date: {} ".format(id, str(datetime.utcnow()) ) }, 400 # bad request from client

        #request_data = request.get_json(force=True)

        request_data = Runtime.parser.parse_args()

        if request_data['type'] == 'LOCAL':
            # no need of username and password
            runtimeModel = RuntimeModel(request_data['name'], request_data['type'])
        elif request_data['type'] == 'REMOTE':
            # need user_name and user_password
            runtimeModel = RuntimeModel(request_data['name'], request_data['type'], request_data['user_name'],
                                        request_data['user_password'], request_data['user_hostname'] )
        elif request_data['type'] == 'CONTAINER':
            # need a dockerfile
            runtimeModel = RuntimeModel(request_data['name'], request_data['type'], None, None, None,
                                        request_data['dockerfile'])
        try:
            runtimeModel.insert_or_update()
        except Exception as e:
            print ("Error while inserting ", e)
            return {'message': "An error occured while inserting. insert_or_update."}, 500 # this is not users fault. - internal server error
        return runtimeModel.json(), 201

    def delete(self, id):
        runtimeModel = RuntimeModel.find_by_id(id)
        if not runtimeModel:
            return {'message': "RuntimeModel id: '{}' does not exists".format(id)}, 410

        associated_runtime = AssociationModel.find_by_runtime_id(id)
        if associated_runtime:
            return {'message': "There is association with this runtime", 'runtimes': associated_runtime}, 403

        runtimeModel.delete()
        return {'message' : "deleted ".format(id)  }, 201


    def put(self, id):
        runtimeModel = RuntimeModel.find_by_id(id)
        request_data = Runtime.parser.parse_args()
        name = request_data['name']
        if runtimeModel: # runtime already exists, modify that
            try:
                #EndpointModel.update_endpoint(new_endpoint)
                runtimeModel.name = request_data['name']
                runtimeModel.type = request_data['type']

                if 'user_name' in request_data:
                    runtimeModel.user_name = request_data['user_name']
                if 'user_password' in request_data:
                    runtimeModel.user_password = request_data['user_password']

                if 'user_hostname' in request_data:
                    runtimeModel.user_hostname = request_data['user_hostname']



                if 'dockerfile' in request_data:
                    runtimeModel.dockerfile = request_data['dockerfile']


                runtimeModel.insert_or_update()
                return {'endpoint': runtimeModel.json()}
            except Exception as e:
                print ("Exception in put method of runtime resource ", e)
                return {'message': 'failed updating runtime {} in put method - modifying existing'.format(name)}
        else: # add new runtime.
            try:
                if request_data['type'] == 'LOCAL':
                    new_runtime = RuntimeModel(request_data['name'],request_data['type'])
                elif request_data['type'] == 'REMOTE':
                    new_runtime = RuntimeModel(request_data['name'], request_data['type'], request_data['user_name'], request_data['user_password'],
                                               request_data['user_hostname'])

                elif request_data['type'] == 'CONTAINER':
                    # need a dockerfile
                    runtimeModel = RuntimeModel(request_data['name'], request_data['type'], None, None, None,
                                                request_data['dockerfile'])

                new_runtime.insert_or_update()
                return {'runtime': new_runtime.json()}
            except Exception as e:
                print("Exception in put method of runtime resource else block", e)
                return {'message': 'failed adding runtime {} in put method - new endpoint.'.format(name)}



class RuntimeList(Resource):
    def get(self):
        print ([runtime.json() for runtime in RuntimeModel.query.all()])
        return {'runtimes' : [runtime.json() for runtime in RuntimeModel.query.all()]}, 200