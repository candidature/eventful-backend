from flask_restful import Resource, request, abort
from flask import request as request_flask
from models.endpoint import EndpointModel
from models.association import AssociationModel

import json
import os
import shutil

class Default(Resource):
    #parser = reqparse.RequestParser()
    #parser.add_argument('content', type=str, required=True, help="This field cannot be left blank")

    def get(self, path):
        query_string = request_flask.query_string.decode() or None
        print ("Type of query_string is ", type(query_string))
        print("GET URL ", path)
        print("Query String ", query_string)
        return {'method': 'GET', 'query_string': query_string, 'path': path, 'status': ''}

    def post(self,path):

        try:
            if not request.json:
                abort(400,description = 'You can only send JSON body, also make sure you have set header to application/json')
        except:
            abort(400,
                  description='body is not really JSON ')

        body = request.json or None
        query_string = request_flask.query_string.decode() or None

        print ("POST URL ", path)
        print ("Query String ", query_string)
        print("Got this in POST body", json.dumps(body))




        matched_endpoints = MatchEndpoint(path, 'POST').match_endpoint()
        print (matched_endpoints)

        # insert matching endpoints name, requester id, ip, time of last request
        # if time is less than 60 seconds, block next request.

        print("IP address of requester ", request.remote_addr)


        from celery_app import aon_container


        endpoint_runtime_code = []

        for matched_endpoint in matched_endpoints:
            for association in AssociationModel.query.filter_by(endpoint_id=matched_endpoint['id']).all():
                endpoint_runtime_code.append({'endpoint_id': matched_endpoint['id'], 'runtime_id': association.runtime_id,
                                              'code_id' : association.code_id})

        if(endpoint_runtime_code):
            for task in endpoint_runtime_code:
                print ("Creating task for ", task)
                aon_container.delay(task)
        else:
            print ("There is no task to create")

        return {'method': 'POST', 'query_string': query_string, 'path': path, 'body': body, 'matched': matched_endpoints,'association': endpoint_runtime_code}

class RuntimeCode:
    pass
    def getRuntimeCode_by_endpoint_id(self, endpoint_id):

        pass

    def assembleDockerfile(self):
        pass


class MatchEndpoint():
    def __init__(self, path, method, query_string=None, body=None):
        self.path = path
        self.method = method
        self.query_string = query_string
        self.body = body

    def match_endpoint(self):

        matched_endpoints = [row.json() for row in EndpointModel.query.filter_by(path=self.path , method=self.method).all()]

        return matched_endpoints

    def match_query_string(self):
        pass

    def match_body(self):
        pass


class RuntimeContainer(Resource):
    RuntimeFolder='Runetimes'
    def __init__(self, endpoint_id, runtime_id, code_id):
        self.endpoint_id = endpoint_id
        self.runtime_id = runtime_id
        self.code_id = code_id
        self.RuntimeFolder += self.endpoint_id + "/" + self.runtime_id + "/"+self.code_id
        if(os.path.isdir(self.RuntimeFolder) or os.path.exists(self.RuntimeFolder)):
            try:
                shutil.rmtree(self.RuntimeFolder)
            except:
                raise Exception("Cannot re-create {}".format(self.RuntimeFolder) )

        os.makedirs(self.RuntimeFolder)

    def createDockerfile(self):
        # take existing dockerfile
        # add environment variables.
        # add install statements.
        # expose port stattement
        # other handlers

        pass

    def createContainer(self):
        pass

    def removeContainer(self):
        pass

    def saveImpage(self):
        pass
# match endpoint.
# if endpoint matched, match method.
# pass the query string and body (only in case of POST)

