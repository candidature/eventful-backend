from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import identity, authenticate
from resources.user import UserRegister
from resources.endpoint import Endpoint, EndpointList
from resources.runtime import Runtime, RuntimeList
from resources.code import Code, CodeList
from resources.association import Association, AssociationList
from resources.default import Default
from flask_cors import CORS


app = Flask(__name__)

app.secret_key = 'jose'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPOGATE_EXCEPTIONS'] = True



@app.before_first_request
def create_table():
    db.create_all()

cors = CORS(app)
api = Api(app)

# /auth -> creates new endpoint
# when we call /auth, we send username and password
# jwt takes username,password and sends to authenticate
# if password matched, we return jwt token
# that jwt toekn can be sent to next request, JWT calls identity function
# using JWT token it finds userid and if it can do that means it's authenticated and its valid.

jwt = JWT(app, authenticate, identity)


api.add_resource(Endpoint, '/endpoint/dev/v1/<string:id>')
api.add_resource(EndpointList, '/endpoint/dev/v1/')

api.add_resource(Runtime, '/runtime/dev/v1/<string:id>')
api.add_resource(RuntimeList, '/runtime/dev/v1')

api.add_resource(Code, '/code/dev/v1/<string:id>')
api.add_resource(CodeList, '/code/dev/v1')

api.add_resource(Association, '/association/dev/v1/<string:id>')
api.add_resource(AssociationList, '/association/dev/v1')



api.add_resource(UserRegister, '/register/dev/v1')

api.add_resource(Default, '/<path:path>')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)