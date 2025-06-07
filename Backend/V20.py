# version that adds login / registration / user management 
import json
from sqlalchemy.dialects.postgresql import JSONB
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, and_, UniqueConstraint, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session, declarative_base
# from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, create_refresh_token
)
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from datetime import timedelta

import os
import uuid
from werkzeug.utils import secure_filename
from flask import send_from_directory

app = Flask(__name__)

# cors for production

# CORS(app,
#      origins=["https://note.henryfield.net" ],
#      supports_credentials=True,
#      methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
#      allow_headers=["Content-Type", "Authorization"])

# cors for local testing
CORS(app, resources={r"/*": {"origins": "*"}})



app.config['SECRET_KEY'] = 'Sjd($&^(£^$(*Whfoshfjnk)))'  # Change this to a secret key of your choice
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://henry:Naseby2411@localhost:5432/BackendDb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable modification tracking

# Add after other app configurations
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=30)  # Short-lived access token (30seconds)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False   # Long-lived refresh token
# Configure a secret key for JWT
app.config['JWT_SECRET_KEY'] = 'testing'
jwt = JWTManager(app)


# Create an SQLite database inside the Backend folder
engine = create_engine('postgresql://henry:Naseby2411@localhost:5432/BackendDb')
Base = declarative_base()

@app.teardown_appcontext
def shutdown_session(exception=None):
    dbsession.remove()
# dbSession = sessionmaker(bind=engine)
# dbsession = dbSession()

dbsession = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
@app.teardown_appcontext
def shutdown_session(exception=None):
    dbsession.remove()

# Association table for the many-to-many relationship between Note and Tag
note_tag_association = Table('note_tag', Base.metadata,
    Column('note_id', Integer, ForeignKey('notes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id')),
    UniqueConstraint('note_id', 'tag_id', name='uq_note_tag')  # Add this line
)

# Association table for the many-to-many relationship between Tag and Tag (for multiple parents)
tag_parent_association = Table('tag_parent', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('parent_id', Integer, ForeignKey('tags.id'))
)

class Entity(Base):
    """Abstract Entity class representing Notes and Tags."""
    __tablename__ = 'entities'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Global unique ID
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # User-specific entity owner
    user_specific_id = Column(Integer, nullable=False)  # Unique per-user entity ID
    type = Column(String, nullable=False)  # Either 'note' or 'tag'

    __table_args__ = (UniqueConstraint('user_id', 'user_specific_id', name='uq_user_specific_id'),)

    user = relationship('User', backref='entities')

    def __init__(self, user_id, entity_type):
        self.user_id = user_id
        self.type = entity_type
        self.user_specific_id = self._generate_user_specific_id()

    def _generate_user_specific_id(self):
        """Find the next available user-specific ID for this user."""
        # Add a row-level lock to prevent race conditions
        from sqlalchemy import text
        
        # First lock the rows for this user to prevent concurrent ID generation
        dbsession.execute(
            text("LOCK TABLE entities IN SHARE ROW EXCLUSIVE MODE")
        )
        
        # Now get the highest ID with the lock in place
        last_entity = dbsession.query(Entity)\
            .filter_by(user_id=self.user_id)\
            .order_by(Entity.user_specific_id.desc())\
            .first()
        return 1 if not last_entity else last_entity.user_specific_id + 1
    

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)  # Inherits ID from Entity
    name = Column(String, nullable=False)
    colour = Column(String, default="")
    parents = relationship(
        'Tag', 
        secondary=tag_parent_association,
        primaryjoin=id == tag_parent_association.c.tag_id,
        secondaryjoin=id == tag_parent_association.c.parent_id,
        backref=backref('children', lazy='dynamic')
    )
    entity = relationship('Entity', backref='tag', uselist=False, single_parent=True, 
                     cascade="all, delete-orphan")
    
    def __init__(self, user_id, name, parents=None):
        entity = Entity(user_id, "tag")
        dbsession.add(entity)
        dbsession.flush()  # Ensure Entity is saved to get its ID
        self.id = entity.id
        self.name = name
        if parents:
            self.parents = parents  # If parents are passed, associate them with this tag
        else:
            self.parents = []  
        


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)  # Inherits ID from Entity
    format = Column(String, default="document")
    name = Column(String, nullable=False)
    colour = Column(String, default="")
    content = Column(JSONB, default=lambda:[])
    viewport = Column(String, default="")
    background = Column(String, default="")
    tags = relationship('Tag', secondary=note_tag_association, backref=backref('notes', lazy='dynamic'))
    entity = relationship('Entity', backref='note', uselist=False, single_parent=True,
                     cascade="all, delete-orphan") 
     
    def __init__(self, user_id, name, format=None, tags=None):
        entity = Entity(user_id, "note")
        dbsession.add(entity)
        dbsession.flush()  # Ensure Entity is saved to get its ID
        self.id = entity.id
        self.name = name
        self.format = format
        if tags is not None:
            self.tags = tags  # Assign the passed tags list to the note

class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # Primary key
    email = Column(String, unique=True)  # Unique email
    password = Column(String)
    username = Column(String)
    user_status = Column(String, default="User")  # User, admin, staff
    preferences = Column(JSONB, default={})  # JSONB column for storing user preferences
    tabs = Column(JSONB, default={})  # JSONB column for storing user tabs

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Can be null for anonymous feedback
    
    # Basic feedback data
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'), nullable=False)
    category = Column(String, nullable=False)
    message = Column(String, nullable=False)
    
    # Screenshot IDs (stored as JSONB array)
    screenshot_ids = Column(JSONB, default=[])
    
    # Metadata
    created_at = Column(DateTime, default=func.now())
    status = Column(String, default="unread")  # unread, read, responded, closed
    
    # Relationship to user
    user = relationship('User', backref=backref('feedback', lazy='dynamic'))
    
    def __init__(self, rating, category, message, user_id=None, name=None, email=None, screenshot_ids=None):
        self.rating = rating
        self.category = category
        self.message = message
        self.user_id = user_id
        self.screenshot_ids = screenshot_ids or []


# Create the tables if they don't exist
Base.metadata.create_all(engine)



def populate_sample_data():
    print("Populating sample data...")
    user = User(email="admin@admin", password=generate_password_hash("admin", method='pbkdf2:sha256'), username="admin", user_status="admin")
    dbsession.add(user)
    dbsession.commit()  # Save the user to generate an ID
    tags = {}
    tag_names = [
        "Physics", "Homework", "Classwork", "Mechanics", "Electricity", "Waves", "Thermodynamics",
        "Nuclear Physics", "Quantum Physics", "Astrophysics", "Forces", "Energy", "Momentum", "Electromagnetism",
        "Particle Physics", "Optics", "Oscillations", "Kinematics", "Dynamics", "Magnetism", "Radioactivity",
        "Capacitors", "Materials", "Fluids", "Circular Motion", "Gravitational Fields", "Magnetic Fields",
        "Electronics", "Experimental Techniques", "Mathematical Methods"
    ]

    parent_map = {
        "Homework": "Physics", "Classwork": "Physics", "Mechanics": "Physics", "Electricity": "Physics",
        "Waves": "Physics", "Thermodynamics": "Physics", "Nuclear Physics": "Physics", "Quantum Physics": "Physics",
        "Astrophysics": "Physics", "Forces": "Mechanics", "Energy": "Mechanics", "Momentum": "Mechanics",
        "Electromagnetism": "Electricity", "Particle Physics": "Nuclear Physics", "Optics": "Waves",
        "Oscillations": "Waves", "Kinematics": "Mechanics", "Dynamics": "Mechanics", "Magnetism": "Electromagnetism",
        "Radioactivity": "Nuclear Physics", "Capacitors": "Electricity", "Materials": "Mechanics", "Fluids": "Mechanics",
        "Circular Motion": "Mechanics", "Gravitational Fields": "Astrophysics", "Magnetic Fields": "Electromagnetism",
        "Electronics": "Electricity", "Experimental Techniques": "Physics", "Mathematical Methods": "Physics"
    }

    for name in tag_names:
        parent = [tags[parent_map[name]]] if name in parent_map else []
        tags[name] = Tag(name=name, parents=parent, user_id=user.id)
        dbsession.add(tags[name])

    notes = [
        Note(name="Newton's Laws Homework", tags=[tags["Homework"], tags["Forces"]], user_id=user.id),
        Note(name="Classwork on Projectile Motion", tags=[tags["Classwork"], tags["Kinematics"]], user_id=user.id),
        Note(name="Momentum Conservation Problems", tags=[tags["Homework"], tags["Momentum"]], user_id=user.id),
        Note(name="Work Done and Energy Transfer", tags=[tags["Classwork"], tags["Energy"]], user_id=user.id),
        Note(name="Gravitational Potential Energy Notes", tags=[tags["Classwork"], tags["Gravitational Fields"]], user_id=user.id),
        Note(name="Simple Harmonic Motion Equations", tags=[tags["Classwork"], tags["Oscillations"]], user_id=user.id),
        Note(name="Refraction and Lenses", tags=[tags["Classwork"], tags["Optics"]], user_id=user.id),
        Note(name="Wave Interference Homework", tags=[tags["Homework"], tags["Waves"]], user_id=user.id),
        Note(name="Ohm's Law Experiment", tags=[tags["Classwork"], tags["Electricity"], tags["Experimental Techniques"]], user_id=user.id),
        Note(name="Capacitor Charge and Discharge", tags=[tags["Classwork"], tags["Capacitors"]], user_id=user.id),
        Note(name="Radioactivity and Half-Life", tags=[tags["Classwork"], tags["Radioactivity"]], user_id=user.id),
        Note(name="Photoelectric Effect Explanation", tags=[tags["Classwork"], tags["Quantum Physics"]], user_id=user.id),
        Note(name="Magnetic Field Lines Investigation", tags=[tags["Classwork"], tags["Magnetic Fields"]], user_id=user.id),
        Note(name="Thermodynamics First Law", tags=[tags["Classwork"], tags["Thermodynamics"]], user_id=user.id),
        Note(name="Black Hole Physics", tags=[tags["Classwork"], tags["Astrophysics"]], user_id=user.id),
        Note(name="Particle Accelerators Notes", tags=[tags["Classwork"], tags["Particle Physics"]], user_id=user.id),
        Note(name="Circular Motion in Satellites", tags=[tags["Classwork"], tags["Circular Motion"]], user_id=user.id),
        Note(name="Electric Fields and Potential", tags=[tags["Classwork"], tags["Electromagnetism"]], user_id=user.id),
        Note(name="Fluid Dynamics Principles", tags=[tags["Classwork"], tags["Fluids"]], user_id=user.id),
        Note(name="Mathematical Methods for Physics", tags=[tags["Classwork"], tags["Mathematical Methods"]], user_id=user.id)
    ]

    for note in notes:
        dbsession.add(note)

    dbsession.commit()

    # Commit the changes to the database
    dbsession.commit()

# Populate sample data if not already present
if dbsession.query(User).count() == 0:
    populate_sample_data()


# @app.route('/')
# def home():
#     return redirect('/app')
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Endpoint for refreshing an access token using a refresh token"""
    current_user = get_jwt_identity()
    
    # Create new access token
    access_token = create_access_token(identity=current_user)
    print("################### refreshed access token")
    
    return jsonify(access_token=access_token), 200


@app.route('/login', methods=['POST'])
def login():
    # Expecting JSON data, not form data
    data = request.get_json()  # Use .get_json() to parse JSON
    # print(data)
    email = data.get('email').lower()
    password = data.get('password')
    # print("################### recieved login request for", email)
  
    
    # Query the user from the database
    user = dbsession.query(User).filter_by(email=email).first()
    

    # Check if user exists and passwords match
    if user is None:    
        return jsonify({"message": "Invalid email"}), 400
    
    if check_password_hash(user.password, password):
    # if user.password == password:
        # Create JWT token on successful login
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        # print("logged in") 
        return jsonify(access_token=access_token, refresh_token=refresh_token, username = user.username, email = user.email, userStatus = user.user_status, preferences = user.preferences), 200
        
    else:
        return jsonify({"message": "Invalid password"}), 400


# @app.route('/test', methods=['GET'])
# @jwt_required()  # Protect this route with JWT authentication
# def test():
#     # try:
#         current_user = get_jwt_identity()  # Retrieve the identity from the JWT token
#     #     print("Decoded user identity:", current_user)  # Debugging line
#     #     return jsonify(current_user), 200
#     # except Exception as e:
#         return jsonify("message", current_user), 200


@app.route('/register', methods=['POST'])
def register():
    # print("recieved request for registration")
    data = request.get_json()  # Use .get_json() to parse JSON
    # print(data)
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
    terms = data.get('terms')
    
    if terms == False:
        # print("didnt accept terms")
        return jsonify({"message": "Please accept the terms and conditions"}), 400
    existing_user = dbsession.query(User).filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Account already Exists, please Login"}), 400
    else:
        user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), username=username)
        dbsession.add(user)
        dbsession.commit()
        
        user = dbsession.query(User).filter_by(email=email).first()
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        # print("logged in")
        return jsonify(access_token=access_token, refresh_token = refresh_token, username = user.username, email = user.email, userStatus = user.user_status, preferences = user.preferences), 200
       
        
    
# @app.route('/logout', methods=['GET'])
# @login_required  # Ensure the user is logged in to log out
# def logout():
#     logout_user()  # Log out the user
#     flash('You have been logged out.', 'success')
#     return redirect('/login')


# @app.route('/app')
# @login_required
# def index():
#     return render_template('V19.html')

    

    
@app.route('/create', methods=['POST'])
# @login_required
@jwt_required()
def create():
    data = request.json
    type = data.get('type')
    userId = get_jwt_identity()
    
    if type == 'edge':
        source_id = data.get('source')
        target_id = data.get('target')
        # print(source_id, target_id)
        # Validate the input
        if not source_id or not target_id:
            return jsonify({'status': 'error', 'message': 'Source or target ID is missing.'}), 400

        # Determine the type of the source and target
        if source_id.startswith('tag_') and target_id.startswith('tag_'):
            source_tag_id = int(source_id.split('_')[1])
            target_tag_id = int(target_id.split('_')[1])

            # Query the tags
            
            
            source_tag = dbsession.query(Tag).join(Entity).filter(
            Entity.user_id == userId,  # Ensure it belongs to the logged-in user
            Entity.user_specific_id == source_tag_id  # Find using per-user unique ID
            ).first()
            
            target_tag = dbsession.query(Tag).join(Entity).filter(
            Entity.user_id == userId,  # Ensure it belongs to the logged-in user
            Entity.user_specific_id == target_tag_id  # Find using per-user unique ID
            ).first()
            
            if source_tag and target_tag:   
                # Add the parent-child relationship
                if target_tag not in source_tag.children:
                    source_tag.children.append(target_tag)
                    dbsession.commit()
                    return jsonify({'status': 'success', 'message': 'Tag-Tag link created.'})
                else:
                    return jsonify({'status': 'error', 'message': 'Link already exists.'}), 400
            else:
                return jsonify({'status': 'error', 'message': 'Tag(s) not found.'}), 404

        elif source_id.startswith('tag_') and target_id.startswith('note_'):
            # print("########################tag-note tag source", source_id, "note target", target_id)
            source_tag_id = int(source_id.split('_')[1])
            target_note_id = int(target_id.split('_')[1])

            # Query the tag and note
        
            source_tag = dbsession.query(Tag).join(Entity).filter(
            Entity.user_id == userId,  # Ensure it belongs to the logged-in user
            Entity.user_specific_id == source_tag_id  # Find using per-user unique ID
            ).first()
            
            
            # target_note = dbsession.query(Note).filter_by(user_id=1, user_specific_id=target_note_id).first()
            target_note = dbsession.query(Note).join(Entity).filter(
            Entity.user_id == userId,  # Ensure it belongs to the logged-in user
            Entity.user_specific_id == target_note_id  # Find using per-user unique ID
            ).first()
            
            if source_tag and target_note:
                # Add the tag-note relationship
                if source_tag not in target_note.tags:
                    target_note.tags.append(source_tag)
                    dbsession.commit()
                    return jsonify({'status': 'success', 'message': 'Tag-Note link created.'})
                else:
                    return jsonify({'status': 'error', 'message': 'Link already exists.'}), 400
            else:
                return jsonify({'status': 'error', 'message': 'Tag or Note not found.'}), 404

        else:
            return jsonify({'status': 'error', 'message': 'Invalid link type.'}), 400
        
    elif type == 'tag':
        name = data.get('name')
        tag = Tag(name=name, user_id = userId)
        # tag.set_user_specific_id(dbsession)
        dbsession.add(tag)
        try:
            dbsession.commit()
            # print(f"Created tag {tag.entity.user_specific_id}")
            elements = []
            element = {
                'id': tag.entity.user_specific_id,
                'name': tag.name,
                'children': [child.entity.user_specific_id for child in tag.children],
                'notes': [note.entity.user_specific_id for note in tag.notes],
                'type': "tag",  # Add type property
                'data': 
            {
                # 'x': tag.x,
                # 'y': tag.y,
                'colour': tag.colour,
            }
            }
            elements.append(element)
            return jsonify(elements = elements)
        
        except Exception as e:
            dbsession.rollback()
            # print(f"Error creating tag: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to create tag}'}), 500
        
    elif type == 'note':
        name = data.get('name')
        format = data.get('format')
        
       
        note = Note(name=name, tags=[], format=format, user_id=int(userId))
        
        
        # note.set_user_specific_id(dbsession)
        dbsession.add(note)
        try:
            dbsession.commit()
            # print(f"#####################Created note {note.entity.user_specific_id}#####################")
            elements = []
            element = {
                    'id': note.entity.user_specific_id,
                    'name': note.name,
                    'tags': [tag.entity.user_specific_id for tag in note.tags],
                    'type': "note",  # Add type property
                    'format': note.format,
                    'data': 
                    {
                        # 'x': note.x,
                        # 'y': note.y,
                        'colour': note.colour,
                    }
                }
            elements.append(element)
            return jsonify(elements = elements)
        except Exception as e:
            dbsession.rollback()
            # print(f"Error creating note: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to create note}'}), 500
 
    elif type == 'version':
        note_id = data.get('note_id')    
        user_id = get_jwt_identity()
        version_name = data.get('version_name', f"Manual save {datetime.now().strftime('%H:%M:%S')}")
        
        # Find the note
        note = dbsession.query(Note).join(Entity).filter(
            Entity.user_id == int(user_id),
            Entity.user_specific_id == note_id
        ).first()
        
        if note is None:
            return jsonify({'status': 'error', 'message': 'Note not found'}), 404
        
        try:
            # Get current content (most recent version)
            if not note.content or not isinstance(note.content, list):
                return jsonify({'status': 'error', 'message': 'No content to version'}), 400
                
            current_version = note.content[0]
            current_content = current_version.get("content") if isinstance(current_version, dict) else current_version
            
            # Create new manual version
            version_entry = {
                "content": current_content,
                "timestamp": datetime.now().isoformat(),
                "version_type": "manual",
                "version_name": version_name
            }
            
            # Add to versions
            note.content = [version_entry] + note.content
            
            # Apply smart pruning
            note.content = smart_prune_versions(note.content)
            
            dbsession.commit()
            return jsonify({
                'status': 'success', 
                'message': 'Manual version created successfully',
                'version_name': version_name
            })
        except Exception as e:
            dbsession.rollback()
            return jsonify({'status': 'error', 'message': f'Failed to create version: {str(e)}'}), 500
 
    

@app.route('/delete', methods=['POST'])
@jwt_required()
def  delete():
    data = request.json
    type = data.get('type')
    userId = get_jwt_identity()
    
    if type == "edge":
        source_id = data.get('source')
        target_id = data.get('target')
        # print(source_id, target_id)
        # Validate the input
        if not source_id or not target_id:
            return jsonify({'status': 'error', 'message': 'Source or target ID is missing.'}), 400

        try:
            # Determine the type of the source and target
            if source_id.startswith('tag_') and target_id.startswith('tag_'):
                source_tag_id = int(source_id.split('_')[1])
                target_tag_id = int(target_id.split('_')[1])

                # Query the tags
                source_tag = dbsession.query(Tag).join(Entity).filter(
                Entity.user_id == userId,  # Ensure it belongs to the logged-in user
                Entity.user_specific_id == source_tag_id  # Find using per-user unique ID
                ).first()
                
                target_tag = dbsession.query(Tag).join(Entity).filter(
                Entity.user_id == userId,  # Ensure it belongs to the logged-in user
                Entity.user_specific_id == target_tag_id  # Find using per-user unique ID
                ).first()
                
                if source_tag and target_tag:
                    # Remove the parent-child relationship
                    if target_tag in source_tag.children:
                        source_tag.children.remove(target_tag)
                        dbsession.commit()
                        dbsession.flush()  # Ensure relationships are cleared
                        return jsonify({'status': 'success', 'message': 'Tag-Tag link deleted.'})
                    else:
                        return jsonify({'status': 'error', 'message': 'Link does not exist.'}), 400
                else:
                    return jsonify({'status': 'error', 'message': 'Tag(s) not found.'}), 404

            elif source_id.startswith('tag_') and target_id.startswith('note_'):
                source_tag_id = int(source_id.split('_')[1])
                target_note_id = int(target_id.split('_')[1])

                # Query the tag and note
                try:
                    source_tag = dbsession.query(Tag).join(Entity).filter(
                        Entity.user_id == userId,
                        Entity.user_specific_id == source_tag_id
                    ).first()
                    
                    target_note = dbsession.query(Note).join(Entity).filter(
                        Entity.user_id == userId,
                        Entity.user_specific_id == target_note_id
                    ).first()
                    
                    if source_tag and target_note:
                        # More robust approach - delete directly from the association table
                        stmt = note_tag_association.delete().where(
                            and_(
                                note_tag_association.c.note_id == target_note.id,
                                note_tag_association.c.tag_id == source_tag.id
                            )
                        )
                        dbsession.execute(stmt)
                        dbsession.commit()
                        return jsonify({'status': 'success', 'message': 'Tag-Note link deleted.'})
                    else:
                        return jsonify({'status': 'error', 'message': 'Tag or Note not found.'}), 404
                except Exception as e:
                    dbsession.rollback()
                    # print(f"Error deleting link: {e}")
                    return jsonify({'status': 'error', 'message': str(e)}), 500
            else:
                return jsonify({'status': 'error', 'message': 'Invalid link type.'}), 400

        except Exception as e:
            dbsession.rollback()
            # print(f"Error deleting link: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to delete link.'}), 500
   
    elif type == "node":    
        id = data.get('id')
        
        if id.startswith('tag_'):
            tag_id = int(id.split('_')[1])
          
            tag = dbsession.query(Tag).join(Entity).filter(
                Entity.user_id == userId,  # Ensure it belongs to the logged-in user
                Entity.user_specific_id == tag_id  # Find using per-user unique ID
                ).first()

            if tag is None:
                return jsonify({'status': 'error', 'message': 'Tag not found'}), 404
            try:
                
                dbsession.delete(tag)
                dbsession.commit()
                return jsonify({'status': 'success', 'message': f'Tag {id} deleted.'})
            
            except Exception as e:
                dbsession.rollback()
                # print(f"Error deleting tag {id}: {e}")
                return jsonify({'status': 'error', 'message': 'Failed to delete tag'}), 500
            
        elif id.startswith('note_'):
            note_id = int(id.split('_')[1])
            note = dbsession.query(Note).join(Entity).filter(
                Entity.user_id == userId,  # Ensure it belongs to the logged-in user
                Entity.user_specific_id == note_id  # Find using per-user unique ID
                ).first()
            if note is None:
                return jsonify({'status': 'error', 'message': 'Note not found'}), 404
            try:     
                dbsession.delete(note)
                dbsession.commit()
                return jsonify({'status': 'success', 'message': f'Note {id} deleted.'})
            except Exception as e:
                dbsession.rollback()
                # print(f"Error deleting note {id}: {e}")
                return jsonify({'status': 'error', 'message': 'Failed to delete note'}), 500
        
    
    
    
def smart_prune_versions(versions, max_total=100):
    """
    Smart pruning of versions to keep meaningful history:
    - Always keeps all manual versions when possible
    - Keeps more recent automatic versions 
    - Spaces out older versions to maintain coverage
    """
    if len(versions) <= max_total:
        return versions
    
    # Separate manual and auto versions
    manual_versions = [v for v in versions if v.get("version_type") == "manual"]
    auto_versions = [v for v in versions if v.get("version_type") != "manual"]
    
    # If we have too many manual versions already, keep the most recent ones
    if len(manual_versions) >= max_total:
        return manual_versions[:max_total]
    
    # Calculate how many auto versions we can keep
    remaining_slots = max_total - len(manual_versions)
    
    # If we can keep all auto versions, return all versions
    if len(auto_versions) <= remaining_slots:
        return manual_versions + auto_versions
    
    # Keep more recent auto versions (2/3 of slots) and sample older ones (1/3 of slots)
    recent_count = min(int(remaining_slots * 0.67), len(auto_versions))
    historical_count = remaining_slots - recent_count
    
    # Get recent versions
    recent_auto_versions = auto_versions[:recent_count]
    
    # Sample from older versions at regular intervals for historical perspective
    older_auto_versions = auto_versions[recent_count:]
    historical_versions = []
    
    if historical_count > 0 and older_auto_versions:
        # Space them out evenly
        indices = [int(i * len(older_auto_versions) / historical_count) for i in range(historical_count)]
        historical_versions = [older_auto_versions[i] for i in indices]
    
    # Combine all versions
    result = manual_versions + recent_auto_versions + historical_versions
    
    # Sort by recency (newest first)
    return sorted(result, key=lambda v: v.get("timestamp", ""), reverse=True)

@app.route('/update', methods=['POST'])
@jwt_required()
def update():   
    data = request.json
    operation = data.get('operation')
    user = get_jwt_identity()
    
    if operation == "location":
        node_id = data.get('id')

        x = data.get('x')
        y = data.get('y')

        # Validate input
        if node_id is None or x is None or y is None:
            return jsonify({'status': 'error', 'message': 'Invalid input data'}), 400

        # Determine if the node is a Tag or Note
        if node_id.startswith('tag_'):
            node_id = int(node_id.split('_')[1])
            node = dbsession.query(Tag).filter_by(user_id=1, user_specific_id=node_id).first()
    
            
        elif node_id.startswith('note_'):
            node_id = int(node_id.split('_')[1])
            node = dbsession.query(Note).filter_by(user_id=1, user_specific_id=node_id).first()
            
        else:
            return jsonify({'status': 'error', 'message': 'Invalid node ID format'}), 400
        
        # Update position
        node.x = round(x)
        node.y = round(y)

        try:
            dbsession.commit()
            # print(f"Updated node {node_id}: x={x}, y={y}")
            return jsonify({'status': 'success', 'message': f'Node {node_id} updated.'})
        except Exception as e:
            dbsession.rollback()
            # print(f"Error updating node {node_id}: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to update node position'}), 500
     
    elif operation == "unlock":  
        id = data.get('id')
        if id == "all":
            try:
                for tag in dbsession.query(Tag).filter_by(user_id=1).all():
                    tag.x = None
                    tag.y = None
                for note in dbsession.query(Note).filter_by(user_id=1).all():
                    note.x = None
                    note.y = None
                dbsession.commit()
                return jsonify({'status': 'success', 'message': 'All nodes unlocked.'})
            except Exception as e:
                dbsession.rollback()
                return jsonify({'status': 'error', 'message': 'Failed to unlock nodes'}), 500
        else:
            if id.startswith('tag_'):
                id = int(id.split('_')[1])
                node = dbsession.query(Tag).filter_by(user_id=1, user_specific_id=id).first()
            elif id.startswith('note_'):
                id = int(id.split('_')[1])
                node = dbsession.query(Note).filter_by(user_id=1, user_specific_id=id).first()
            node.x = None
            node.y = None
            dbsession.commit()
        return jsonify({'status': 'success', 'message': f'Node {id} unlocked.'})     

    elif operation == "content":
        data = request.json
        note_id = data.get('id')
        new_content = data.get('content')
        tags_ids = data.get('tags', [])
        name = data.get('name')
        
        # Validate input
        if note_id is None:
            return jsonify({'status': 'error', 'message': 'Invalid input data'}), 400

        # Query the note
        note = dbsession.query(Note).join(Entity).filter(
            Entity.user_id == int(user),
            Entity.user_specific_id == note_id
            ).first()
        
        if note is None:
            return jsonify({'status': 'error', 'message': 'Note not found'}), 404
        
        print("------- note", note.name, "has been found with content type:")
        
        # Initialize content properly
        if note.content is None:
            print("------- Initializing empty content array")
            note.content = []
        elif not isinstance(note.content, list):
            print("------- Converting legacy content to versioned format")
            old_content = note.content
            note.content = [{
                "content": old_content,
                "timestamp": datetime.now().isoformat(),
                "version_type": "legacy"
            }]
        
        # Constants for versioning thresholds
        MIN_VERSION_TIME_INTERVAL = 5 * 60  # 5 minutes between auto versions
        MIN_CHANGE_THRESHOLD = 0.15  # 15% content change threshold
        
        # Check if content has actually changed
        has_changed = False
        should_create_version = False
        force_manual_version = data.get('create_manual_version', False)
        version_name = data.get('version_name', None)
        if force_manual_version:
            # Always create a version if manually requested
            should_create_version = True
            has_changed = True
            
            
        elif not note.content:
            # No existing versions
            should_create_version = True
            has_changed = True
            # print("###### making the first version")
        else:
            try:
                # Safely get the current content
                current_version = note.content[0] if note.content else None
                current_content = current_version.get("content") if isinstance(current_version, dict) else current_version
                
                # Compare as strings to handle complex structures
                current_json = json.dumps(current_content, sort_keys=True) if current_content else ""
                new_json = json.dumps(new_content, sort_keys=True) if new_content else ""
                has_changed = current_json != new_json
                
                if has_changed:
                    # Check if we should create a new version based on time threshold
                    time_threshold_met = True
                    if isinstance(current_version, dict) and "timestamp" in current_version:
                        last_time = datetime.fromisoformat(current_version["timestamp"])
                        time_diff = (datetime.now() - last_time).total_seconds()
                        time_threshold_met = time_diff > MIN_VERSION_TIME_INTERVAL
                    
                    # Check if change is significant enough (based on content size difference)
                    change_size_threshold_met = True
                    if current_json and new_json:
                        # Calculate difference magnitude (simple approach using length difference)
                        size_diff_ratio = abs(len(new_json) - len(current_json)) / max(len(current_json), 1)
                        change_size_threshold_met = size_diff_ratio > MIN_CHANGE_THRESHOLD
                    
                    # Only create a version if either threshold is met
                    should_create_version = time_threshold_met or change_size_threshold_met
                    
                    print(f"------- Time threshold met: {time_threshold_met}, Change threshold met: {change_size_threshold_met}")
                
                print(f"------- Content changed? {has_changed}, Creating new version? {should_create_version}")
            except Exception as e:
                print(f"------- Error comparing content: {e}")
                should_create_version = True  # Assume we should version if comparison fails

        if has_changed:
            if should_create_version:
                # Create a new version
                print("------- Creating new version entry")
                version_entry = {
                    "content": new_content,
                    "timestamp": datetime.now().isoformat(),
                    "version_type": "manual" if force_manual_version else "auto"
                }
                
                # Add version name if provided (for manual versions)
                if version_name:
                    version_entry["version_name"] = version_name
                
                # Create a new list instead of modifying the existing one in-place
                new_content_array = [version_entry] + note.content
            else:
                # Just update the current version instead of creating a new one
                print("------- Updating existing version entry")
                # Create a new list with updated first element
                current_version = note.content[0].copy() if isinstance(note.content[0], dict) else {"content": note.content[0]}
                current_version["content"] = new_content
                current_version["timestamp"] = datetime.now().isoformat()
                new_content_array = [current_version] + note.content[1:]
            
            # Apply smart pruning
            new_content_array = smart_prune_versions(new_content_array)
            
            # IMPORTANT: Assign the entire new array to trigger SQLAlchemy change detection
            note.content = new_content_array
        # Update other fields
        note.name = name
        
        # Update tags
        new_tags = []
        for tag_id in tags_ids:
            tag = dbsession.query(Tag).join(Entity).filter(
                Entity.user_id == int(user),
                Entity.user_specific_id == tag_id
            ).first()
            
            if tag:
                new_tags.append(tag)
            else:
                print(f"Warning: Tag with ID {tag_id} not found for user {user}")
        
        # Replace all tag associations
        note.tags = new_tags
        
        # Handle whiteboard-specific fields
        if note.format == "whiteboard":
            print("------- note is a whiteboard, setting viewport and background")
            note.viewport = data.get('viewport')
            note.background = data.get('background')
        elif note.format == "document":
            print("------- note is a document, setting viewport")
            note.viewport = data.get('viewport')
            
        
        try:
            # Explicitly commit and refresh
            dbsession.commit()
            dbsession.refresh(note)
            
            # Verify the update worked
            print(f"------- After update: note has {len(note.content)} versions")
            
            return jsonify({'status': 'success', 'message': 'Note content updated successfully.'})
        except Exception as e:
            dbsession.rollback()
            print(f"Error updating note {note_id} content: {e}")
            return jsonify({'status': 'error', 'message': f'Failed to update note content: {str(e)}'}), 500
    
    elif operation == "restore":
        note_id = data.get('note_id')
        version_index = data.get('version_index')
        user_id = get_jwt_identity()
        # print("########################## restoring version", version_index, "of note", note_id, "for user", user_id)
        note = dbsession.query(Note).join(Entity).filter(
            Entity.user_id == int(user_id),
            Entity.user_specific_id == note_id
        ).first()
        
        if note is None:
            return jsonify({'status': 'error', 'message': 'Note not found'}), 404
        
        if not note.content or not isinstance(note.content, list) or version_index >= len(note.content):
            return jsonify({'status': 'error', 'message': 'Version not found'}), 404
        
        try:
            # Get the version to restore
            version_to_restore = note.content[version_index]
            restored_content = version_to_restore.get("content") if isinstance(version_to_restore, dict) else version_to_restore
            
            # Create a new version with the restored content
            restored_version = {
                "content": restored_content,
                "timestamp": datetime.now().isoformat(),
                "version_type": "restored",
                "version_name": ""
            }
            
            # Move the restored version to the front
            new_content_array = [restored_version] + note.content
            note.content = new_content_array
            
            # Apply smart pruning
            note.content = smart_prune_versions(note.content)
            
            dbsession.commit()
            return jsonify({'status': 'success', 'message': 'Version restored successfully'})
        except Exception as e:
            dbsession.rollback()
            return jsonify({'status': 'error', 'message': f'Failed to restore version: {str(e)}'}), 500
        
        
    elif operation == "rename":
        data = request.json
        id = data.get('id')
        
        type = id.split('_')[0]
        id = int(id.split('_')[1])
        name = data.get('name')
        if type == "tag":
            tag = dbsession.query(Tag).join(Entity).filter(
            Entity.user_id == user,  # Ensure it belongs to the logged-in user
            Entity.user_specific_id == id  # Find using per-user unique ID
            ).first()
            tag.name = name
        elif type == "note":
            # note = dbsession.query(Note).filter_by(user_id=1, user_specific_id=id).first()
            
            note = dbsession.query(Note).join(Entity).filter(
            Entity.user_id == int(user),  # Ensure it belongs to the logged-in user
            Entity.user_specific_id == id  # Find using per-user unique ID
        ).first()
            note.name = name
        dbsession.commit()
        return jsonify({'status': 'success', 'message': '{type}: {id} name updated successfully.'})
        
   
    elif operation == "user":
        # print("########################## updating user data")

        try:
            # Get the current user
            user_id = get_jwt_identity()
            user = dbsession.query(User).filter_by(id=user_id).first()

            # print("########################## REQUEST JSON:", request.json)

            if not user:
                return jsonify({'status': 'error', 'message': 'User not found'}), 404
                
            # Fix for issue: create a working copy of preferences
            preferences = dict(user.preferences) if user.preferences is not None else {}
                
            # Check for username update
            if 'username' in request.json:
                user.username = request.json['username']
                
            # Check for email update
            if 'email' in request.json:
                user.email = request.json['email']
                
            # Check for password update
            if 'newPassword' in request.json:
                print("########################## new password found")
                try:
                    currentPassword = request.json['currentPassword']
                    newPassword = request.json['newPassword']
                    print("current password", currentPassword)
                    if check_password_hash(user.password, currentPassword):
                        
                        user.password = generate_password_hash(newPassword, method='pbkdf2:sha256')
                        print("########################## password updated")
                    else:
                        print("########################## error1")
                        return jsonify({'status': 'error', 'message': 'Current password is incorrect'})
                except:
                    print("########################## error2")
                    return jsonify({'status': 'error', 'message': 'Current password is required'})
                    
            # check for avatar
            # if 'avatar' in request.json:
            #     print("########################## avatar found")
            #     preferences.update(request.json['avatar'])
                
            # if 'streamerMode' in request.json:
            #     print("########################## streamer mode found")
            #     preferences.update(request.json['streamerMode'])
                
            # Check for preferences update
            if 'preferences' in request.json:
                print("########################## preferences found", request.json['preferences'])
                # print(f"Updating preferences with: {request.json['preferences']}")
                preferences.update(request.json['preferences'])
                
            
            if 'theme' in request.json:
                preferences['theme'] = request.json['theme']
                # print(f"Updated user preferences: {preferences}")
                
            # Check for tabs update
            if 'tabs' in request.json:
                preferences['tabs'] = request.json['tabs']
                # print(f"Updated user preferences: {preferences}")
                
            # Check for recent notes update
            if 'recentNotes' in request.json:
                # print(f"Updating recent notes with: {request.json['recentNotes']}")
                preferences['recentNotes'] = request.json['recentNotes']
                # print(f"Updated user preferences: {preferences}")
                
            # IMPORTANT: This flags the entire preferences object as changed
            user.preferences = preferences

            # Commit changes and ensure they persist
            dbsession.commit()
            # Verify the data was saved by re-querying
            dbsession.refresh(user)
            # print(f"User preferences after update: {user.preferences}")

            return jsonify({
                'status': 'success',
                'message': 'User data updated successfully',
                'preferences': user.preferences
            })

        except Exception as e:
            dbsession.rollback()
            # print(f"Error updating user data: {e}")
            import traceback
            traceback.print_exc()
            return jsonify({'status': 'error', 'message': f'Failed to update user data: {str(e)}'}), 500
    
    
    
    # elif operation == "tabs":
    #     data = request.json
    #     tabs = data.get('tabs')
    #     user = dbsession.query(User).filter_by(id=current_user).first()
    #     user.tabs = tabs
    #     dbsession.commit()
    #     return jsonify({'status': 'success', 'message': 'User tabs updated successfully.'})
    
      
@app.route('/load', methods=['POST'])
# @login_required
@jwt_required()
def load():
    
    data = request.json
    
    operation = data.get('operation')
    current_user = get_jwt_identity()
    
    if operation == "graph":
        elements = []
        for tag in dbsession.query(Tag).join(Entity).filter(Entity.user_id == current_user).all():    
            element = {
                'id': tag.entity.user_specific_id,
                'name': tag.name,
             'children': [child.entity.user_specific_id for child in tag.children],
                'notes': [note.entity.user_specific_id for note in tag.notes],
                'type': "tag",  # Add type property
                'data': 
            {
                # 'x': tag.x,
                # 'y': tag.y,
                'colour': tag.colour,
            }
            }
            elements.append(element)
            
        for note in dbsession.query(Note).join(Entity).filter(Entity.user_id == current_user).all():
            element = {
                'id': note.entity.user_specific_id,
                'name': note.name,
                     'tags': [tag.entity.user_specific_id for tag in note.tags],
                'type': "note",  # Add type property
                'format': note.format,
                'data': 
                {
                    # 'x': note.x,
                    # 'y': note.y,
                    'colour': note.colour,
                }
            }
            elements.append(element)
        
        return jsonify(elements=elements)
    
    
        
    elif operation == "content":
        note_id = data.get('id')
        # note_id = int(note_id.split('_')[1])    
        # print("#######################################",note_id, "is being sent")

        # Validate input
        if note_id is None:
            return jsonify({'status': 'error', 'message': 'Invalid input data'}), 400

        # Query the note
        note = dbsession.query(Note).join(Entity).filter(
            Entity.user_id == current_user,  # Ensure it belongs to the logged-in user
            Entity.user_specific_id == note_id  # Find using per-user unique ID
            ).first()
        if note is None:
            return jsonify({'status': 'error', 'message': 'Note not found'}), 404
        
        current_content = None
        if note.content:
            if isinstance(note.content, list):
                if note.content and isinstance(note.content[0], dict):
                    current_content = note.content[0].get("content")  # Extract content from versioned format
                else:
                    current_content = note.content[0]  # Handle older array format
            else:
                current_content = note.content  # Handle legacy format
                
        return jsonify({
            'status': 'success', 
            'content': current_content, 
            'viewport': note.viewport, 
            'background': note.background, 
            'name': note.name, 
            'tags': [tag.entity.user_specific_id for tag in note.tags]
        })
    
    elif operation == "user":
        user = dbsession.query(User).filter_by(id=current_user).first()
        return jsonify({'status': 'success', 'username': user.username, 'email': user.email, 'userStatus': user.user_status, 'preferences': user.preferences})

    elif operation == "tabs":
        user = dbsession.query(User).filter_by(id=current_user).first()
        tabs = user.preferences.get('tabs', []) if user and user.preferences else []
        # print("sent tabs", tabs)
        return jsonify(tabs)
    
    elif operation == "versions":
        note_id = data.get('note_id')
        user_id = get_jwt_identity()
    
        note = dbsession.query(Note).join(Entity).filter(
            Entity.user_id == int(user_id),
            Entity.user_specific_id == note_id
        ).first()
        
        if note is None:
            return jsonify({'status': 'error', 'message': 'Note not found'}), 404
        
        versions = []
        if note.content and isinstance(note.content, list):
            for i, version in enumerate(note.content):
                version_info = {
                    "index": i,
                    "is_current": i == 0
                }
                
                if isinstance(version, dict):
                    # Format the timestamp for display
                    timestamp = version.get("timestamp")
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp)
                            friendly_time = dt.strftime("%b %d, %Y %I:%M %p")
                        except:
                            friendly_time = timestamp
                    else:
                        friendly_time = "Unknown date"
                    
                    version_info.update({
                        "timestamp": timestamp,
                        "friendly_time": friendly_time,
                        "version_type": version.get("version_type", "auto"),
                        "version_name": version.get("version_name", f"Version {i+1}"),
                        "content": version.get("content", "")
                    })
                else:
                    version_info.update({
                        "timestamp": "Unknown",
                        "friendly_time": "Unknown date",
                        "version_type": "legacy",
                        "version_name": f"Version {i+1}",
                        "content": "none"
                    })
                
                versions.append(version_info)
        
        return jsonify({
            'status': 'success',
            'versions': versions
        })
    
 # Add image upload endpoint
 
@app.route('/feedback', methods=['POST'])
@jwt_required(optional=True)  # Make JWT optional to allow anonymous feedback
def feedback():
    try:

        # JSON data
        data = request.json
        rating = int(data.get('rating'))
        category = data.get('category')
        message = data.get('message')
        screenshots_data = data.get('screenshots', {})
        
        # Get current user if authenticated
        try:
            current_user_id = get_jwt_identity()
        except:
            current_user_id = None
        
        # Validate required fields
        if not rating or not category or not message:
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
        
        # Create new feedback entry
        new_feedback = Feedback(
            rating=rating,
            category=category,
            message=message,
            user_id=current_user_id,
            screenshot_ids=[]  # Initialize with empty array
        )
        
        dbsession.add(new_feedback)
        dbsession.flush()  # Get the ID without committing
        
        screenshot_ids = []
        
        # Handle screenshots if provided in form data
         # Create feedback screenshots folder if it doesn't exist
        screenshots_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'feedback')
        if not os.path.exists(screenshots_folder):
            os.makedirs(screenshots_folder)
        
        # Process screenshots from JSON (base64 encoded)
        for key, base64_data in screenshots_data.items():
            try:
                # Extract the actual base64 data (remove metadata)
                if ',' in base64_data:
                    format_data, base64_string = base64_data.split(',', 1)
                else:
                    base64_string = base64_data
                
                # Get file extension from mimetype
                file_ext = '.png'  # Default to png
                if 'image/jpeg' in format_data:
                    file_ext = '.jpg'
                elif 'image/gif' in format_data:
                    file_ext = '.gif'
                
                # Generate filename
                filename = f"feedback_{new_feedback.id}_{uuid.uuid4()}{file_ext}"
                file_path = os.path.join(screenshots_folder, filename)
                
                # Decode base64 and save as image
                import base64
                img_data = base64.b64decode(base64_string)
                with open(file_path, 'wb') as f:
                    f.write(img_data)
                
                # Add filename to list
                screenshot_ids.append(filename)
            except Exception as e:
                print(f"Error processing screenshot {key}: {e}")
        
        # Update the feedback record with screenshot IDs
        new_feedback.screenshot_ids = screenshot_ids
        
        dbsession.commit()
        
        return jsonify({
            'status': 'success', 
            'message': 'Feedback submitted successfully',
            'feedback_id': new_feedback.id
        }), 201
        
    except Exception as e:
        dbsession.rollback()
        # print(f"Error saving feedback: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': 'Failed to save feedback'}), 500

# Helper function to check allowed file types
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route('/upload-file', methods=['POST'])
@jwt_required()
def upload_file():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        # Generate safe filename with UUID to prevent conflicts
        ext = os.path.splitext(secure_filename(file.filename))[1]
        filename = f"{uuid.uuid4()}{ext}"
        
        # Create user-specific folder if it doesn't exist
        user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        
        file_path = os.path.join(user_folder, filename)
        file.save(file_path)
        
        # Return URL to access the file
        return jsonify({
            "url": f"/files/{user_id}/{filename}"
        }), 200
  
@app.route('/files/<user_id>/<filename>')
# @jwt_required()
def serve_image(user_id, filename):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
    return send_from_directory(user_folder, filename)

# @app.route('/files', methods=['GET'])
# @jwt_required()
# def serve_file():
#     user_id = get_jwt_identity()
#     data = request.json
#     filename = data.get('path')
#     user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
#     return send_from_directory(user_folder, filename)
    
@app.route("/health")
def health():
    return jsonify(status="ok", service="flask"), 200   
if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000, allow_unsafe_werkzeug=True)