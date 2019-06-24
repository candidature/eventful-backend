from flask_restful import Resource, reqparse, request
from models.code import CodeModel


class Code(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank")
    parser.add_argument('code')
    parser.add_argument('environment_variables') # on event or on schedule , default on event # generally endpoint which is an event.
    parser.add_argument('packages_install_commands')
    parser.add_argument('exposed_port')
    parser.add_argument('error')

    def get(self, id):
        print ("Finding",id)
        row = CodeModel.find_by_id(id)

        if(row):
            return row.json()

        return {'message': 'Codename does not exists'}


    def post(self,id=None):

        request_data = Code.parser.parse_args()
        name = request_data['name']



        if CodeModel.find_by_name(name):
            return {'message': "Code with name '{}' already exists ".format(id)}, 400 # bad request from client

        #request_data = request.get_json(force=True)
        codeModel = CodeModel(name, request_data['code'])


        if 'environment_variables' not in request_data:
            codeModel.environment_variables = request_data['environment_variables']
        if 'packages_install_commands' in request_data:
            codeModel.packages_install_commands = request_data['packages_install_commands']
        if 'exposed_port' in request_data:
            codeModel.exposed_port = request_data['exposed_port']

        try:
            codeModel.insert_or_update()
        except Exception as e:
            print ("Exception in post method ", e)
            return {'message': "An error occured while inserting. insert_or_update {}".format(name)}, 500 # this is not users fault. - internal server error
        return codeModel.json(), 201

    def delete(self, id):
        codeModel = CodeModel.find_by_id(id)
        if not codeModel:
            return {'message': "CodeModel '{}' does not exists".format(id)}
        codeModel.delete()
        return {'message' : "deleted ".format(id)  }, 201


    def put(self, id):
        codeModel = CodeModel.find_by_id(id)
        request_data = Code.parser.parse_args()
        name = request_data['name']

        if codeModel: # runtime already exists, modify that
            try:
                #EndpointModel.update_endpoint(new_endpoint)
                codeModel.code = request_data['code']
                if 'environment_variables' in request_data:
                    codeModel.environment_variables = request_data['environment_variables']
                if 'packages_install_commands' in request_data:
                    codeModel.packages_install_commands = request_data['packages_install_commands']
                if 'exposed_port' in request_data:
                    codeModel.exposed_port = request_data['exposed_port']

                codeModel.insert_or_update()
                return {'endpoint': codeModel.json()}
            except Exception as e:
                print ("Exception in codeModel if block ", e)
                return {'message': 'failed updating code {} in put method'.format(name)}
        else: # add new endpoint.
            try:
                new_code = CodeModel(name, request_data['code'])

                if 'environment_variables' in request_data:
                    new_code.environment_variables = request_data['environment_variables']
                if 'packages_install_commands' in request_data:
                    new_code.packages_install_commands = request_data['packages_install_commands']
                if 'exposed_port' in request_data:
                    new_code.exposed_port = request_data['exposed_port']

                new_code.insert_or_update()
                return {'code': new_code.json()}
            except Exception as e:
                print("Exception in codeModel else block ", e)
                return {'message': 'failed adding code {} in put method'.format(name)}



class CodeList(Resource):
    def get(self):
        return {'codes' : [code.json() for code in CodeModel.query.all()]}