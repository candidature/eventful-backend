from db import db
from flask import jsonify
import json
class AssociationModel(db.Model):
    __tablename__ = 'association'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80))

    endpoint_id = db.Column(db.Integer, db.ForeignKey('endpoints.id'))
    endpoint = db.relationship('EndpointModel')

    runtime_id = db.Column(db.Integer, db.ForeignKey('runtimes.id'))
    runtime = db.relationship('RuntimeModel')

    code_id = db.Column(db.Integer, db.ForeignKey('codes.id'))
    code = db.relationship('CodeModel')

    trigger = db.Column(db.String(10), default='event')  # on event or on schedule , default on event
    schedule = db.Column(db.String(100), default='Null')  # cron style schedule - Future.

    enabled = db.Column(db.Boolean(), default=True)

    def __init__(self, name, endpoint_id=None, runtime_id=None, code_id=None, trigger='EVENT', schedule=None, enabled=True):
        self.name = name
        self.endpoint_id = endpoint_id
        self.runtime_id = runtime_id
        self.code_id = code_id
        self.trigger = trigger
        self.schedule = schedule
        self.enabled = enabled

    def json(self):
        data_dict = {
            "id" : self.id,
            "name" : self.name,

            "endpoint_id" : self.endpoint_id,
            "runtime_id" : self.runtime_id,
            "code_id" : self.code_id,

            "trigger" : self.trigger,
            "schedule" : self.schedule,
            "enabled" : self.enabled
        }

        return (data_dict)


    @classmethod
    def find_by_name(cls, name):
        print ("Finding association for ", name)
        return AssociationModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        print("Finding association for ", id)
        return AssociationModel.query.filter_by(id=id).first()


    @classmethod
    def find_by_endpoint_id(cls, endpoint_id):
        return {'associations': [association.json() for association in AssociationModel.query.filter_by(endpoint_id=endpoint_id).all()]}


    @classmethod
    def find_by_runtime_id(cls, runtime_id):
        return {'associations': [association.json() for association in AssociationModel.query.filter_by(runtime_id=runtime_id).all()]}


    @classmethod
    def find_by_code_id(cls, code_id):
        return {'associations': [association.json() for association in
                                 AssociationModel.query.filter_by(code_id=code_id).all()]}


    def insert_or_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()