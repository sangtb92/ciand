from project import db


class Account(db.Model):
    __tablename__ = 'tbl_account'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    phone_number = db.Column(db.String(16), nullable=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Integer, nullable=False, default=0)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    is_active = db.Column(db.Boolean, default=False, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    stores = db.relationship('Store', backref='account')

    def __init__(self, user_name, password, email, phone_number, first_name, last_name, status, is_admin, is_active):
        self.user_name = user_name
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.email = email
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.is_active = is_active
        self.is_admin = is_admin


class Store(db.Model):
    __tablename__ = 'tbl_store'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(255), nullable=False, unique=True)
    store_address = db.Column(db.String(255), nullable=False)
    store_manager = db.Column(db.Integer, db.ForeignKey('tbl_account.id'))
    store_items = db.relationship('Item', backref='store')
    store_menu = db.relationship('MenuItem', backref='store')

    def __init__(self, store_name, store_address, store_manager):
        self.store_name = store_name
        self.store_address = store_address
        self.store_manager = store_manager


class Item(db.Model):
    __tablename__ = 'tbl_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(255), nullable=False, unique=True)
    item_price = db.Column(db.Float, nullable=False)
    item_status = db.Column(db.SmallInteger, nullable=False)
    item_quantity = db.Column(db.Float, nullable=False)
    item_origin = db.Column(db.String(255), nullable=True)
    item_desc = db.Column(db.String(), nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('tbl_store.id'))

    def __init__(self, item_name, item_price, item_status, item_quantity, item_origin, item_desc):
        self.item_name = item_name
        self.item_price = item_price
        self.item_quantity = item_quantity
        self.item_status = item_status
        self.item_origin = item_origin
        self.item_desc = item_desc


class MenuItem(db.Model):
    __tablename__ = 'tbl_menu_item'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    menu_item_name = db.Column(db.Integer, nullable=False, unique=True)
    menu_item_price = db.Column(db.Float, nullable=False)
    menu_item_desc = db.Column(db.String, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('tbl_store.id'))

    def __init__(self, menu_item_name, menu_item_price, menu_item_desc):
        self.menu_item_name = menu_item_name
        self.menu_item_desc = menu_item_desc
        self.menu_item_price = menu_item_price


class Table(db.Model):
    __tablename__ = 'tbl_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    table_name = db.Column(db.String(255), nullable=False, unique=True)
    table_seating = db.Column(db.Integer, nullable=False)
    table_desc = db.Column(db.String, nullable=True)
    store_id = db.Column(db.Integer, db.ForeignKey('tbl_store.id'))
    pass


class Bill(db.Model):
    __tablename__ = 'tbl_bill'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    open_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Boolean, default=False, nullable=False)
    close_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, open_date, status, close_date, toppings, main_items):
        self.open_date = open_date
        self.status = status
        self.close_date = close_date
        self.toppings = toppings
        self.main_items = main_items


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
