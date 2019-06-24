from db import db

class EndpointModel(db.Model):
    __tablename__ = 'endpoints'

    id = db.Column(db.Integer, primary_key=True)
    endpoint_name = db.Column(db.String(80))
    path = db.Column(db.String(200))
    method = db.Column(db.String(20))
    data = db.Column(db.String(1000))

    

    def __init__(self, id, endpoint_name, path, method, data):
        self.id = id or None
        self.endpoint_name = endpoint_name
        self.path = path
        self.method = method
        if (data):
            self.data = data

    def json(self):
        return { 'id': self.id, 'endpoint_name': self.endpoint_name, 'path': self.path, 'method': self.method, 'data' : self.data}

    @classmethod
    def find_by_name(cls, endpoint_name):
        return EndpointModel.query.filter_by(endpoint_name=endpoint_name).first()

    @classmethod
    def find_by_id(cls, id):
        return EndpointModel.query.filter_by(id=id).first()


    def insert_or_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()