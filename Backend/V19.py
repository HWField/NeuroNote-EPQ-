# version that adds login / registration / user management 

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, and_, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)





from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
app.config['SECRET_KEY'] = 'Sjd($&^(£^$(*Whfoshfjnk)))'  # Change this to a secret key of your choice
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure a secret key for JWT
app.config['JWT_SECRET_KEY'] = 'testing'
jwt = JWTManager(app)


# Create an SQLite database inside the Backend folder
engine = create_engine('sqlite:///Backend/Database.db')
Base = declarative_base()

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
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

# Association table for the many-to-many relationship between Tag and Tag (for multiple parents)
tag_parent_association = Table('tag_parent', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('parent_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)

    
    name = Column(String, nullable=False)
    x = Column(Integer, nullable=True)
    y = Column(Integer, nullable=True)
    colour = Column(String, default="")
    
    # Foreign key to associate with a user
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='tags')  # Back-reference to User
    parents = relationship(
        'Tag', 
        secondary=tag_parent_association,
        primaryjoin=id == tag_parent_association.c.tag_id,
        secondaryjoin=id == tag_parent_association.c.parent_id,
        backref=backref('children', lazy='dynamic')
    )
    user_specific_id = Column(Integer, nullable=False)  # ID specific to the user
    __table_args__ = (
        UniqueConstraint('user_specific_id', 'user_id', name='_user_specific_id_uc'),
    )
    def set_user_specific_id(self, session):
        # Query to find the current max user_specific_id for this user
        max_id = session.query(func.max(Tag.user_specific_id)).filter(Tag.user_id == self.user_id).scalar()
        self.user_specific_id = (max_id or 0) + 1
        


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    colour = Column(String, default="")
    x = Column(Integer, nullable=True)
    y = Column(Integer, nullable=True)
    content = Column(String, default="")
    viewport = Column(String, default="")
    background = Column(String, default="")
    
    # Foreign key to associate with a user
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    user = relationship('User', back_populates='notes')  # Back-reference to User
    tags = relationship('Tag', secondary=note_tag_association, backref=backref('notes', lazy='dynamic'))
    
    
    
    user_specific_id = Column(Integer, nullable=False)  # ID specific to the user
    
    __table_args__ = (
        UniqueConstraint('user_specific_id', 'user_id', name='_user_specific_id_uc'),
    )
    def set_user_specific_id(self, session):
        # Query to find the current max user_specific_id for this user
        max_id = session.query(func.max(Note.user_specific_id)).filter(Note.user_id == self.user_id).scalar()
        self.user_specific_id = (max_id or 0) + 1
        
       
class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # Primary key
    email = Column(String, unique=True)  # Unique email
    password = Column(String)
    username = Column(String)
    user_status = Column(String, default="User")  # User, admin, staff

    # Relationship to Notes and Tags (optional for easier query access)
    notes = relationship('Note', back_populates='user', cascade="all, delete-orphan")
    tags = relationship('Tag', back_populates='user', cascade="all, delete-orphan") 

# Create the tables if they don't exist
Base.metadata.create_all(engine)

def populate_sample_data():
    current_max_tag_id = 0
    current_max_note_id = 0

    user = User(email="admin@admin", password="admin", username="adminuser", user_status="admin")
    dbsession.add(user)
    dbsession.commit()  # Save the user to generate an ID


    EPQ_tag = Tag(name="EPQ", x=0, y=0, user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(EPQ_tag)
    
    planning_tag = Tag(name="Planning A01", parents=[EPQ_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(planning_tag)

    research_tag = Tag(name="Research A02", parents=[EPQ_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(research_tag)
    
    ui_tag = Tag(name="UI", parents=[research_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    technical_tag = Tag(name="Technical", parents=[research_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    ai_tag = Tag(name="AI", parents=[research_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    visualisation_tag = Tag(name="Visualisation", parents=[research_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(ui_tag)
    dbsession.add(technical_tag)
    dbsession.add(ai_tag)
    dbsession.add(visualisation_tag)

    evaluation_tag = Tag(name="Evaluation A04", parents=[EPQ_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(evaluation_tag)

    skilldevelopment_tag = Tag(name="Skill Development A03", parents=[EPQ_tag] ,user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(skilldevelopment_tag)



    project_tag = Tag(name="Project Choice", parents=[EPQ_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(project_tag)

    homework_tag = Tag(name="Homework", parents=[EPQ_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(homework_tag)

    diary_tag = Tag(name="Diary", parents=[EPQ_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(diary_tag)

    airefereencing_tag = Tag(name="AI Referencing", parents=[EPQ_tag], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(airefereencing_tag)

    completed_tag = Tag(name="Completed", parents=[], user_id = user.id, user_specific_id = current_max_tag_id + 1)
    current_max_tag_id += 1
    dbsession.add(completed_tag)

    research1_note = Note(name="Note 1", tags=[diary_tag, homework_tag, technical_tag], user_id = user.id, user_specific_id = current_max_note_id + 1)
    current_max_note_id += 1
    research2_note = Note(name="Note 2", tags=[diary_tag, homework_tag, ai_tag], user_id = user.id, user_specific_id = current_max_note_id + 1)
    current_max_note_id += 1
    airefrence1_note = Note(name="Note 3", tags=[airefereencing_tag], user_id = user.id, user_specific_id = current_max_note_id + 1)
    current_max_note_id += 1
    airefrence2_note = Note(name="Note 4", tags=[airefereencing_tag, completed_tag], user_id = user.id, user_specific_id = current_max_note_id + 1)
    current_max_note_id += 1
    dbsession.add(research1_note)
    dbsession.add(research2_note)
    dbsession.add(airefrence1_note)
    dbsession.add(airefrence2_note)

    # Commit the changes to the database
    dbsession.commit()

# Populate sample data if not already present
if dbsession.query(Tag).count() == 0:
    populate_sample_data()


# @app.route('/')
# def home():
#     return redirect('/app')


@app.route('/login', methods=['POST'])
def login():
    # Expecting JSON data, not form data
    data = request.get_json()  # Use .get_json() to parse JSON
    print(data)
    email = data.get('email')
    password = data.get('password')
    
    # Query the user from the database
    user = dbsession.query(User).filter_by(email=email).first()
    
    # Check if user exists and passwords match
    if user is None:
        return jsonify({"message": "Invalid email"}), 400
    
    if check_password_hash(user.password, password):
    # if user.password == password:
        # Create JWT token on successful login
        access_token = create_access_token(identity=str(user.id))
        print("logged in") 
        return jsonify(access_token=access_token), 200
        
    else:
        return jsonify({"message": "Invalid password"}), 400


@app.route('/test', methods=['GET'])
@jwt_required()  # Protect this route with JWT authentication
def test():
    # try:
        current_user = get_jwt_identity()  # Retrieve the identity from the JWT token
    #     print("Decoded user identity:", current_user)  # Debugging line
    #     return jsonify(current_user), 200
    # except Exception as e:
        return jsonify("message", current_user), 200


@app.route('/register', methods=['POST'])
def register():
    print("recieved request for registration")
    data = request.get_json()  # Use .get_json() to parse JSON
    print(data)
    email = data.get('email')
    password = data.get('password')
    username = data.get('username')
  
    existing_user = dbsession.query(User).filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User Already Exists"}), 400
    else:
        user = User(email=email, password=generate_password_hash(password, method='pbkdf2:sha256'), username=username)
        dbsession.add(user)
        dbsession.commit()
        
        user = dbsession.query(User).filter_by(email=email).first()
        access_token = create_access_token(identity=str(user.id))
        print("logged in")
        return jsonify(access_token=access_token), 200
       
        
    
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
def create():
    data = request.json
    type = data.get('type')
    
    if type == 'edge':
        source_id = data.get('source')
        target_id = data.get('target')
        print(source_id, target_id)
        # Validate the input
        if not source_id or not target_id:
            return jsonify({'status': 'error', 'message': 'Source or target ID is missing.'}), 400


        # Determine the type of the source and target
        if source_id.startswith('tag_') and target_id.startswith('tag_'):
            source_tag_id = int(source_id.split('_')[1])
            target_tag_id = int(target_id.split('_')[1])

            # Query the tags
            source_tag = dbsession.query(Tag).filter_by(user_id=1, user_specific_id=source_tag_id).first()
            target_tag = dbsession.query(Tag).filter_by(user_id = 1, user_specific_id=target_tag_id).first()

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
            source_tag_id = int(source_id.split('_')[1])
            target_note_id = int(target_id.split('_')[1])

            # Query the tag and note
            source_tag = dbsession.query(Tag).filter_by(user_id=1, user_specific_id=source_tag_id).first()
            target_note = dbsession.query(Note).filter_by(user_id=1, user_specific_id=target_note_id).first()

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
        tag = Tag(name=name, user_id = 1)
        tag.set_user_specific_id(dbsession)
        dbsession.add(tag)
        try:
            dbsession.commit()
            print(f"Created note {tag.id}")
            elements = []
            element = {
                'id': tag.user_specific_id,
                'name': tag.name,
                'children': [child.user_specific_id for child in tag.children], #was child.id
                'notes': [note.user_specific_id for note in tag.notes], #was child.id
                'type': "tag",  # Add type property
                'data': 
            {
                'x': tag.x,
                'y': tag.y,
                'colour': tag.colour,
            }
            }
            elements.append(element)
            return  jsonify(elements = elements)
        
        except Exception as e:
            dbsession.rollback()
            print(f"Error creating tag: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to create tag}'}), 500
        
    elif type == 'note':
        name = data.get('name')
        note = Note(name=name,  user_id = 1)
        note.set_user_specific_id(dbsession)
        dbsession.add(note)
        try:
            dbsession.commit()
            print(f"Created note {note.id}")
            elements = []
            element = {
                'id': note.user_specific_id,
                'name': note.name,
                'tags': [tag.user_specific_id for tag in note.tags],
                'type': "note",  # Add type property
                'data': 
            {
                'x': note.x,
                'y': note.y,
                'colour': note.colour,
            }
            }
            elements.append(element)
            return  jsonify(elements = elements)
        except Exception as e:
            dbsession.rollback()
            print(f"Error creating tag: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to create note}'}), 500
        
 
    

@app.route('/delete', methods=['POST'])
# @login_required
def  delete():
    data = request.json
    type = data.get('type')
    
    if type == "edge":
        source_id = data.get('source')
        target_id = data.get('target')
        print(source_id, target_id)
        # Validate the input
        if not source_id or not target_id:
            return jsonify({'status': 'error', 'message': 'Source or target ID is missing.'}), 400

        try:
            # Determine the type of the source and target
            if source_id.startswith('tag_') and target_id.startswith('tag_'):
                source_tag_id = int(source_id.split('_')[1])
                target_tag_id = int(target_id.split('_')[1])

                # Query the tags
                source_tag = dbsession.query(Tag).filter_by(user_id=1, user_specific_id=source_tag_id).first()
                target_tag = dbsession.query(Tag).filter_by(user_id = 1, user_specific_id=target_tag_id).first()

                if source_tag and target_tag:
                    # Remove the parent-child relationship
                    if target_tag in source_tag.children:
                        source_tag.children.remove(target_tag)
                        dbsession.commit()
                        return jsonify({'status': 'success', 'message': 'Tag-Tag link deleted.'})
                    else:
                        return jsonify({'status': 'error', 'message': 'Link does not exist.'}), 400
                else:
                    return jsonify({'status': 'error', 'message': 'Tag(s) not found.'}), 404

            elif source_id.startswith('tag_') and target_id.startswith('note_'):
                source_tag_id = int(source_id.split('_')[1])
                target_note_id = int(target_id.split('_')[1])

                # Query the tag and note
            
                source_tag = dbsession.query(Tag).filter_by(user_id=1, user_specific_id=source_tag_id).first()
                target_note = dbsession.query(Note).filter_by(user_id = 1, user_specific_id=target_note_id).first()

                if source_tag and target_note:
                    # Remove the tag-note relationship
                    if source_tag in target_note.tags:
                        target_note.tags.remove(source_tag)
                        dbsession.commit()
                        return jsonify({'status': 'success', 'message': 'Tag-Note link deleted.'})
                    else:
                        return jsonify({'status': 'error', 'message': 'Link does not exist.'}), 400
                else:
                    return jsonify({'status': 'error', 'message': 'Tag or Note not found.'}), 404

            else:
                return jsonify({'status': 'error', 'message': 'Invalid link type.'}), 400

        except Exception as e:
            dbsession.rollback()
            print(f"Error deleting link: {e}")
            return jsonify({'status': 'error', 'message': 'Failed to delete link.'}), 500
   
    elif type == "node":    
        id = data.get('id')
        
        if id.startswith('tag_'):
            id = int(id.split('_')[1])
          
            tag = dbsession.query(Tag).filter_by(user_id=1, user_specific_id=id).first()

            if tag is None:
                return jsonify({'status': 'error', 'message': 'Tag not found'}), 404
            try:
                dbsession.delete(tag)
                dbsession.commit()
                return jsonify({'status': 'success', 'message': f'Tag {id} deleted.'})
            except Exception as e:
                dbsession.rollback()
                print(f"Error deleting tag {id}: {e}")
                return jsonify({'status': 'error', 'message': 'Failed to delete tag'}), 500
        elif id.startswith('note_'):
            id = int(id.split('_')[1])
            note = dbsession.query(Note).filter_by(user_id=1, user_specific_id=id).first()
            if note is None:
                return jsonify({'status': 'error', 'message': 'Note not found'}), 404
            try:
                dbsession.delete(note)
                dbsession.commit()
                return jsonify({'status': 'success', 'message': f'Note {id} deleted.'})
            except Exception as e:
                dbsession.rollback()
                print(f"Error deleting note {id}: {e}")
                return jsonify({'status': 'error', 'message': 'Failed to delete note'}), 500
        
    
    
@app.route('/update', methods=['POST'])
# @login_required
def update():   
    data = request.json
    operation = data.get('operation')
    
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
            print(f"Updated node {node_id}: x={x}, y={y}")
            return jsonify({'status': 'success', 'message': f'Node {node_id} updated.'})
        except Exception as e:
            dbsession.rollback()
            print(f"Error updating node {node_id}: {e}")
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
        note_id = int(note_id.split('_')[1])
        viewport = data.get('viewport')
        content = data.get('content')
        background = data.get('background')
        name = data.get('name')
        print("------- note", note_id, "has made a save request")

        # Validate input
        if note_id is None:
            print("------- note", note_id, "has invalid input data")
            return jsonify({'status': 'error', 'message': 'Invalid input data'}), 400

        # Query the note
        note = dbsession.query(Note).filter_by(user_id=1, user_specific_id=note_id).first()
        if note is None:
            print("------- note", note_id, "has not been found")
            return jsonify({'status': 'error', 'message': 'Note not found'}), 404
        else:
            print("------- note", note.name, "has been found")

        # Update the content
        note.viewport = viewport
        note.content = content
        note.background = background
        note.name = name
        print("------- note: ", note.name, ", has had content, viewport and background set")

        # try:
        # try:
        
        dbsession.commit()
        print(f"Updated note {note_id} to database")
        return jsonify({'status': 'success', 'message': 'Note content updated successfully.'})
            
        # except Exception as e:
        #     dbsession.rollback()
        #     print(f"Error updating note {note_id} content: {e}")
        #     return jsonify({'status': 'error', 'message': 'Failed to update note content'}), 500
        
    elif operation == "rename":
        data = request.json
        id = data.get('id')
        id = int(id.split('_')[1])
        type = data.get('type')
        name = data.get('name')
        if type == "tag":
            tag = dbsession.query(Tag).filter_by(user_id=1, user_specific_id=id).first()
            tag.name = name
        elif type == "note":
            note = dbsession.query(Note).filter_by(user_id=1, user_specific_id=id).first()
            note.name = name
        dbsession.commit()
        return jsonify({'status': 'success', 'message': '{type}: {id} name updated successfully.'})
        
  
      
@app.route('/load', methods=['POST'])
# @login_required
@jwt_required()
def load():
    
    data = request.json
    operation = data.get('operation')
    current_user = get_jwt_identity()
    
    if operation == "all":
        elements = []
        for tag in dbsession.query(Tag).filter_by(user_id=current_user).all():
            
            element = {
                'id': tag.user_specific_id,
                'name': tag.name,
                'children': [child.user_specific_id for child in tag.children],
                'notes': [note.user_specific_id for note in tag.notes],
                'type': "tag",  # Add type property
                'data': 
            {
                'x': tag.x,
                'y': tag.y,
                'colour': tag.colour,
            }
            }
            elements.append(element)
            
        for note in dbsession.query(Note).filter_by(user_id=current_user).all():
            element = {
                'id': note.user_specific_id,
                'name': note.name,
                'tags': [tag.user_specific_id for tag in note.tags],
                'type': "note",  # Add type property
                'data': 
                {
                    'x': note.x,
                    'y': note.y,
                    'colour': note.colour,
                }
            }
            elements.append(element)
        
        return jsonify(elements=elements)
    
    elif operation == "search": 
        query = data.get('query')
        
        def get_descendants(tag):
            """Recursively fetch all descendant tags."""
            descendants = []
            for child in tag.children:
                descendants.append(child)
                descendants.extend(get_descendants(child))
            return descendants

        elements = []
        processed_tags = set()  # Keep track of added tags
        processed_notes = set()  # Keep track of added notes

        # Find tags matching the query
        matched_tags = dbsession.query(Tag).filter(and_(
        Tag.user_id == current_user,  # Match the current user's tags
        Tag.name.ilike(f"%{query}%"))).all()

        # Process each matched tag and its descendants
        for tag in matched_tags:
            all_tags = [tag] + get_descendants(tag)  # Include the tag and its descendants

            for current_tag in all_tags:
                # Add tag to elements if not already processed
                if current_tag.id not in processed_tags:
                    elements.append({
                        'id': current_tag.user_specific_id,
                        'name': current_tag.name,
                        'children': [child.user_specific_id for child in current_tag.children],
                        'notes': [note.user_specific_id for note in current_tag.notes],
                        'type': "tag",
                        'data': {
                'x': current_tag.x,
                'y': current_tag.y,
                'colour': current_tag.colour,
            }
                    })
                    processed_tags.add(current_tag.id)

                # Add notes associated with this tag
                for note in current_tag.notes:
                    if note.id not in processed_notes:
                        elements.append({
                            'id': note.user_specific_id,
                            'name': note.name,
                            'tags': [], #don't include tags for notes to prevent errors as tries to link to non existent tags
                            'type': "note",
                            'data': {
                'x': note.x,
                'y': note.y,
                'colour': note.colour,
            }
                        })
                        processed_notes.add(note.id)
        matched_notes = dbsession.query(Note).filter(and_(Note.user_id == current_user, Note.name.ilike(f"%{query}%"))).all()
        
        for note in matched_notes:
            if note.id not in processed_notes:
                elements.append({
                    'id': note.user_specific_id ,
                    'name': note.name,
                    'tags': [tag.id for tag in note.tags],
                    'type': "note",
                    'data': {
                'x': note.x,
                'y': note.y,
                'colour': note.colour,
            }
                })
                processed_notes.add(note.id)
        print(elements)
        return jsonify(elements=elements)
        
    elif operation == "content":
        note_id = data.get('id')
        note_id = int(note_id.split('_')[1])    
        print(note_id, "is being sent")

        # Validate input
        if note_id is None:
            return jsonify({'status': 'error', 'message': 'Invalid input data'}), 400

        # Query the note
        note = dbsession.query(Note).filter_by(user_id=current_user, user_specific_id=note_id).first()
        if note is None:
            return jsonify({'status': 'error', 'message': 'Note not found'}), 404
        
      

        return jsonify({'status': 'success', 'content': note.content, 'viewport': note.viewport, 'background': note.background, 'name': note.name})
        

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=8000)