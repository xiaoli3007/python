#coding=utf-8
from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)



class Post44(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))

if __name__ == '__main__':
    manager.run()