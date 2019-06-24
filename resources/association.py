from flask_restful import Resource, request, abort, reqparse
from flask import request as request_flask
from models.association import AssociationModel
import json


class Association(Resource):
    #parser = reqparse.RequestParser()
    #parser.add_argument('content', type=str, required=True, help="This field cannot be left blank")
    parser = reqparse.RequestParser()

    parser.add_argument('endpoint_id')
    parser.add_argument('runtime_id')
    parser.add_argument('code_id')

    parser.add_argument('trigger')
    parser.add_argument('schedule')

    parser.add_argument('enabled')

    def get(self, association_name):
        print("Finding", association_name)
        row = AssociationModel.find_by_name(association_name)

        if (row):
            return row.json()

        return {'message': 'Association does not exists'}

    def post(self, association_name):
        if AssociationModel.find_by_name(association_name):
            return {'message': "A Association with name '{}' already exists ".format(association_name)}, 400  # bad request from client

        # request_data = request.get_json(force=True)

        request_data = Association.parser.parse_args()

        associationModel = AssociationModel(association_name)

        if 'endpoint_id' not in request_data:
            associationModel.endpoint_id = request_data['endpoint_id']
        if 'runtime_id' in request_data:
            associationModel.runtime_id = request_data['runtime_id']
        if 'code_id' in request_data:
            associationModel.code_id = request_data['code_id']


        if 'trigger' in request_data:
            associationModel.trigger = request_data['trigger']


        if 'schedule' in request_data:
            associationModel.schedule = request_data['schedule']


        if 'enabled' in request_data:
            associationModel.enabled = request_data['enabled']

        try:
            associationModel.insert_or_update()
        except Exception as e:
            return {'message': "An error occured while inserting. insert_or_update {}".format(
                e)}, 500  # this is not users fault. - internal server error
        return associationModel.json(), 201

    def delete(self, association_name):
        associationModel = AssociationModel.find_by_name(association_name)
        if not associationModel:
            return {'message': "AssociationModel '{}' does not exists".format(association_name)}
        associationModel.delete()
        return {'message': "deleted ".format(association_name)}, 201

    def put(self, association_name):
        associationModel = AssociationModel.find_by_name(association_name)
        request_data = Association.parser.parse_args()

        if associationModel:  # Association already exists, modify that
            try:
                # EndpointModel.update_endpoint(new_endpoint)
                if 'endpoint_id' in request_data:
                    associationModel.endpoint_id = request_data['endpoint_id']
                if 'runtime_id' in request_data:
                    associationModel.runtime_id = request_data['runtime_id']
                if 'code_id' in request_data:
                    associationModel.code_id = request_data['code_id']

                if 'trigger' in request_data:
                    associationModel.trigger = request_data['trigger']

                if 'schedule' in request_data:
                    associationModel.schedule = request_data['schedule']

                if 'enabled' in request_data:
                    associationModel.enabled = request_data['enabled']

                associationModel.insert_or_update()
                return {'association': associationModel.json()}
            except Exception as e:
                return {'message': 'failed updating association {} in put method Exception: {}'.format(association_name, e)}
        else:  # add new endpoint.
            try:
                new_association = AssociationModel(association_name)

                if 'endpoint_id' in request_data:
                    new_association.endpoint_id = request_data['endpoint_id']
                if 'runtime_id' in request_data:
                    new_association.runtime_id = request_data['runtime_id']
                if 'code_id' in request_data:
                    new_association.code_id = request_data['code_id']


                if 'trigger' in request_data:
                    associationModel.trigger = request_data['trigger']

                if 'schedule' in request_data:
                    associationModel.schedule = request_data['schedule']


                if 'enabled' in request_data:
                    new_association.enabled = request_data['enabled']

                new_association.insert_or_update()
                return {'association': new_association.json()}
            except Exception as e:
                return {'message': 'failed adding association {} in put method, Exception: {}'.format(association_name, e)}


class AssociationList(Resource):
    def get(self):
        return {'associations': [association.json() for association in AssociationModel.query.all()]}


