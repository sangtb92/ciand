from flask import Blueprint, jsonify, request, render_template, make_response
from project import db, bcrypt
from project.api.models import User
from sqlalchemy import exc
from project.api.ultis import validate_user_data
from project.api.constant import BAD_REQUEST, MSG_EMAIL_EXIST, MSG_INVALID_PAYLOAD, MSG_EMAIL_ADDED, ACCESS_FORBIDDEN, \
    CREATED, MSG_ACCESS_FORBIDDEN, NOT_FOUND, MSG_USER_NOT_EXIST, OK_REQUEST

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


# users ping test
@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


# register new user
@users_blueprint.route('/users/register', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'code': BAD_REQUEST,
        'message': MSG_INVALID_PAYLOAD
    }
    if not post_data:
        return jsonify(response_object), BAD_REQUEST
    user_name = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    re_password = post_data.get('re_password')
    phone_number = post_data.get('phone_number')
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')

    # validate request param
    resp_object = validate_user_data(email, user_name, password, re_password)
    if resp_object:
        return make_response(jsonify(resp_object)), resp_object.get('code')

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(user_name=user_name, password=password, email=email, phone_number=phone_number,
                                first_name=first_name, last_name=last_name, status=0, is_admin=False, is_active=False))

            db.session.commit()
            response_object = {
                'code': CREATED,
                'message': MSG_EMAIL_ADDED.format(email)
            }
            return jsonify(response_object), CREATED
        else:
            response_object = {
                'code': BAD_REQUEST,
                'message': MSG_EMAIL_EXIST
            }
            return jsonify(response_object), BAD_REQUEST
    except exc.IntegrityError as e:
        print(e)
        return jsonify(response_object), BAD_REQUEST


# get user by id
@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = None
    if auth_token:
        resp = User.decode_auth_token(auth_token)

    response_object = {
        'code': NOT_FOUND,
        'message': MSG_USER_NOT_EXIST
    }
    try:
        if not isinstance(resp, str):
            admin_user = User.query.filter_by(id=int(resp)).first()
            user = User.query.filter_by(id=int(user_id)).first()
        else:
            response_object = {
                'code': BAD_REQUEST,
                'message': resp
            }
            return make_response(jsonify(response_object)), BAD_REQUEST
        if not user:
            return jsonify(response_object), NOT_FOUND
        elif not admin_user.is_admin:
            response_object = {
                "code": ACCESS_FORBIDDEN,
                "message": MSG_ACCESS_FORBIDDEN
            }
            return jsonify(response_object), ACCESS_FORBIDDEN
        else:
            response_object = {
                'code': OK_REQUEST,
                'data': {
                    'id': user.id,
                    'username': user.user_name,
                    'email': user.email,
                    'active': user.is_active,
                    'registered_on': user.registered_on,
                    'last_login': user.last_login
                }
            }
            return jsonify(response_object), OK_REQUEST
    except ValueError as e:
        print(e)
        return make_response(jsonify(response_object)), NOT_FOUND


# list users
@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return make_response(jsonify(response_object)), 200


# login api
@users_blueprint.route('/users/login', methods=['POST'])
def user_login():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    email = post_data.get('email')
    if not post_data:
        return make_response(jsonify(response_object)), 400
    user = User.query.filter_by(email=email).first()
    if not user:
        return make_response(jsonify(response_object)), 404
    try:
        password = post_data.get('password')
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user_id=user.id)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    # covert bytes to string
                    'auth_token': auth_token.decode("utf-8")
                }
                return make_response(jsonify(response_object)), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.'
            }
            return make_response(jsonify(response_object)), 404
    except Exception as e:
        print(e)
        return make_response(jsonify(response_object)), 500


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
