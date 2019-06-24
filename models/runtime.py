from db import db

class RuntimeModel(db.Model):
    __tablename__ = 'runtimes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    type = db.Column(db.String(80))
    user_name = db.Column(db.String(30))
    user_password = db.Column(db.String(30))
    user_hostname = db.Column(db.String(30))

    dockerfile = db.Column(db.String(5000))
    image_name = db.Column(db.String(1000))

    error = db.Column(db.String(1000))

    #endpoint_id = db.Column(db.Integer, db.ForeignKey('endpoints.id'))
    #endpoint = db.relationship('EndpointModel') # now every RuntimeModel has a property endpoint which matches with a endpoint_id

    def __init__(self, name, type, user_name=None, user_password=None, user_hostname=None, dockerfile=None, error=None):

        self.name = name
        self.type = type
        self.user_name = user_name
        self.user_password = user_password
        self.user_hostname = user_hostname

        self.dockerfile = dockerfile
        self.error = error

    def json(self):
        if(self.error):
            return {'id': self.id, 'type': self.type, 'name': self.name, 'user_name': self.user_name, 'user_password': self.user_password,
                    'user_hostname': self.user_hostname, 'image_name' : self.image_name,
                    'dockerfile': self.dockerfile, 'error': self.error}
        return {'id': self.id, 'type': self.type, 'name': self.name, 'user_name': self.user_name, 'user_password': self.user_password,
                'user_hostname': self.user_hostname, 'image_name' : self.image_name,
                'dockerfile': self.dockerfile }

    @classmethod
    def find_by_name(cls, name):
        return RuntimeModel.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return RuntimeModel.query.filter_by(id=id).first()

    def insert_or_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()