from db import db

class StatusModel(db.Model):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(5000))

    endpoint_id = db.Column(db.Integer, db.ForeignKey('endpoints.id'))
    endpoint = db.relationship('EndpointModel')

    #endpoint_id = db.Column(db.Integer, db.ForeignKey('endpoints.id'))
    #endpoint = db.relationship('EndpointModel') # now every RuntimeModel has a property endpoint which matches with a endpoint_id

    def __init__(self, data, endpoint_id):
        self.data = data
        self.endpoint_id = endpoint_id

    def json(self):
        return {'id': self.id, 'data' : self.data, 'endpoint_id': self.endpoint_id, 'endpoint' : self.endpoint}

    @classmethod
    def find_by_endpoint_id(cls, endpoint_id):
        return StatusModel.query.filter_by(endpoint_id=endpoint_id.strip()).first()

    @classmethod
    def find_by_status_id(cls, status_id):
        return StatusModel.query.filter_by(status_id=status_id.strip()).first()


    def insert_or_update(self):
        db.session.add(self)
        db.session.commit()


# /status/<endpoint_id>/status_id/output
