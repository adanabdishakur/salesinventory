import secrets,os

class Base:
    FLASK_APP = os.environ.get('FLASK_APP')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16)

class Development(Base):
    DEBUG = True
    FLASK_ENV = os.environ.get("FLASK_ENV")
    DATABASE = os.environ.get("DATABASE")
    POSTGRES_USER = os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
class Staging(Base):
    
    DATABASE ="dfp92klrjt35om"
    POSTGRES_USER ="rmwetopazivbph"
    POSTGRES_PASSWORD ="101ec10e494934016c0ece4ff3d6f7169c3ea52ee01e761f2110ccb83a0d015c"
    SQLALCHEMY_DATABASE_URL="postgres://rmwetopazivbph:101ec10e494934016c0ece4ff3d6f7169c3ea52ee01e761f2110ccb83a0d015c@ec2-34-254-69-72.eu-west-1.compute.amazonaws.com:5432/dfp92klrjt35om"


class Production(Base):
    pass