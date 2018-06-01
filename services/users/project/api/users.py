from flask import Blueprint, jsonify, request, render_template
from project import db
from project.api.models import User
from sqlalchemy import exc

users_blueprint = Blueprint('users', __name__, template_folder='./templates')

# users ping test
@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


# register new user
@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    print(post_data)
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    phone_number = post_data.get('phone_number')
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(user_name=username, password=password, email=email, phone_number=phone_number,
                                first_name=first_name, last_name=last_name))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!'
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That email already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError:
        return jsonify(response_object), 400


# get user by id
@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    response_object = {
        'status': 'fail',
        'message': 'User does not exist.'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.user_name,
                    'email': user.email,
                    'active': user.is_active,
                    'registered_on': user.registered_on,
                    'last_login': user.last_login
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


# list users
@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user = User(username, email)
        db.session.add(user)
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)
