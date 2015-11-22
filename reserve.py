import datetime
import flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import event, DDL
from flask.ext.restless import APIManager
import flask_admin as admin
from flask_admin.contrib import sqla

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = 'NNyJXK4b2cLc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mila-gpu.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    gpu_id = db.Column(db.Integer, db.ForeignKey('gpu.id'), nullable=False)
    note = db.Column(db.String(300))

    gpu = db.relationship('GPU', backref='reservations')

    __table_args__ = (db.CheckConstraint('start < end'),)


# Guarantee integrity of the database by not allowing overlapping reservations
no_overlap = DDL("""
CREATE TRIGGER no_overlap BEFORE INSERT ON reservation
BEGIN
    SELECT CASE WHEN
        (SELECT COUNT(*) FROM reservation WHERE
         gpu_id = NEW.gpu_id AND start < NEW.end AND end > NEW.start) > 0
    THEN
        RAISE(FAIL, "Conflicting reservations")
    END;
END;
""")
event.listen(Reservation.__table__, 'after_create',
             no_overlap.execute_if(dialect='sqlite'))


gpu_notes = db.Table(
    'gpu_notes',
    db.Column('gpu_id', db.Integer, db.ForeignKey('gpu.id')),
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
)


class GPU(db.Model):
    __tablename__ = 'gpu'
    id = db.Column(db.Integer, primary_key=True)
    device = db.Column(db.String(10), nullable=False)
    reservable = db.Column(db.Boolean, default=True)
    host_id = db.Column(db.Integer, db.ForeignKey('host.id'), nullable=False)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'), nullable=False)
    notes = db.relationship('Note', secondary=gpu_notes, backref='gpus')

    host = db.relationship('Host', backref='gpus')
    model = db.relationship('Model', backref='gpus')

    __table_args__ = (db.UniqueConstraint('device', 'host_id'),)

    def __str__(self):
        return '{}:{} ({})'.format(self.host, self.device, self.model)

    def available(self):
        return not Reservation.query.filter(
            Reservation.gpu_id == self.id,
            Reservation.start < datetime.datetime.now(),
            Reservation.end > datetime.datetime.now()
        ).first()


model_notes = db.Table(
    'model_notes',
    db.Column('model_id', db.Integer, db.ForeignKey('model.id')),
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
)


class Model(db.Model):
    __tablename__ = 'model'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    memory = db.Column(db.Numeric)
    arch = db.Column(db.Numeric)
    notes = db.relationship('Note', secondary=model_notes, backref='models')

    def __str__(self):
        return self.name


host_notes = db.Table(
    'host_notes',
    db.Column('host_id', db.Integer, db.ForeignKey('host.id')),
    db.Column('note_id', db.Integer, db.ForeignKey('note.id'))
)


class Host(db.Model):
    __tablename__ = 'host'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    memory = db.Column(db.Numeric)
    storage = db.Column(db.Numeric)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    notes = db.relationship('Note', secondary=host_notes, backref='hosts')

    room = db.relationship('Room', backref='hosts')

    def __str__(self):
        return self.name


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(1000))

    def __str__(self):
        return self.note


class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __str__(self):
        return str(self.name)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100))

    reservations = db.relationship('Reservation', backref='user')

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username


# Create the admin interface
admin = admin.Admin(app, name='MILA GPU', template_mode='bootstrap3')
admin.add_view(sqla.ModelView(User, db.session))
admin.add_view(sqla.ModelView(Host, db.session))
admin.add_view(sqla.ModelView(Room, db.session))
admin.add_view(sqla.ModelView(Note, db.session))
admin.add_view(sqla.ModelView(Reservation, db.session))
admin.add_view(sqla.ModelView(GPU, db.session, 'GPU'))
admin.add_view(sqla.ModelView(Model, db.session, 'Model'))

manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Reservation, methods=['GET', 'POST'])
manager.create_api(GPU, methods=['GET'], include_methods=['available'],
                   results_per_page=0, allow_functions=True)
manager.create_api(User, methods=['GET', 'POST'])

if __name__ == "__main__":
    app.run()
