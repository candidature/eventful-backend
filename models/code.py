from db import db

class CodeModel(db.Model):
    __tablename__ = 'codes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    code = db.Column(db.String(5000))

    # will be set before running code
    environment_variables = db.Column(db.String(1000)) # on event or on schedule , default on event

    # will be installed after install.
    packages_install_commands = db.Column(db.String(1000))

    exposed_port = db.Column(db.String(10), default="5000")

    # command to checkout repo. like "git clone"
    # command to run after github checkout.

    error = db.Column(db.String(1000), default=None)


    def __init__(self, name, code, environment_variables=None, packages_install_commands=None, exposed_port = None, error=None):
        self.name = name
        self.code = code
        self.environment_variables = environment_variables
        self.packages_install_commands = packages_install_commands
        self.exposed_port = exposed_port
        self.error = error

    def json(self):
        return { 'id': self.id, 'name': self.name, 'code': self.code, 'environment_variables': self.environment_variables,
             'packages_install_commands': self.packages_install_commands,
             'exposed_port': self.exposed_port}

    @classmethod
    def find_by_name(cls, name):
        return CodeModel.query.filter_by(name=name.strip()).first()

    @classmethod
    def find_by_id(cls, id):
        return CodeModel.query.filter_by(id=id).first()

    def insert_or_update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()