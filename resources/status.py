from flask_restful import Resource, request, abort
from flask import request as request_flask

import json
import pickle


class Status(Resource):
    #parser = reqparse.RequestParser()
    #parser.add_argument('content', type=str, required=True, help="This field cannot be left blank")

    ## /status/<endpoint_id>/status_id/output
    def get(self, endpoint_id, status_id=None):
        # read file at /status/endpoint_id/status_id
        # print content of above to the endpoint output
        #from sh import tail

        return {'output': ''}

# match endpoint.
# if endpoint matched, match method.
# pass the query string and body (only in case of POST)