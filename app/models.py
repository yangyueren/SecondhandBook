#!/usr/local/bin/python3

from db import db

from flask_login import UserMixin

# insert into user values(1,'pwpwpw', 'name', 'qqcom', 'addre', '188');


class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(64))
    password = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(64))
    address = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    paypal = db.Column(db.String(64))
    # name = db.Column(db.String(64), unique=True, index=True)
    #
    # pwd = db.Column(db.Integer, default=0)

    def __init__(self, name, password, email, address, phone, paypal):
        # self.user_id = user_id
        self.name = name
        self.password = password
        self.email = email
        self.address = address
        self.phone = phone
        self.paypal = paypal

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def get_name(self):
        return self.name

    def __repr__(self):
        return '<User %r>' % self.name

    def __str__(self):
        return '<User %s>' % self.name


class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # seller_id = db.Column(db.Integer, nullable=True)

    isbn = db.Column(db.String(64))
    book_name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    publisher = db.Column(db.String(64))
    publish_date = db.Column(db.String(64))
    content = db.Column(db.String(200))
    book_type = db.Column(db.String(64))
    picture_url = db.Column(db.String(64))
    ini_price = db.Column(db.Float)
    sell_price = db.Column(db.Float, nullable=True)

    def __init__(self, isbn, book_name, author, publisher,
                 publish_date, content, book_type, picture_url, ini_price, sell_price):
        # self.book_id = book_id
        self.isbn = isbn
        self.book_name = book_name
        self.author = author
        self.publisher = publisher
        self.publish_date = publish_date
        self.content = content
        self.book_type = book_type
        self.picture_url = picture_url
        self.ini_price = ini_price
        self.sell_price = sell_price
        # self.seller_id = seller_id


class SeekBook(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # seller_id = db.Column(db.Integer, nullable=True)

    isbn = db.Column(db.String(64))
    book_name = db.Column(db.String(64))
    author = db.Column(db.String(64))
    publisher = db.Column(db.String(64))
    publish_date = db.Column(db.String(64))
    content = db.Column(db.String(400))
    book_type = db.Column(db.String(64))
    picture_url = db.Column(db.String(64))
    ini_price = db.Column(db.Float)
    sell_price = db.Column(db.Float, nullable=True)

    def __init__(self, isbn, book_name, author, publisher,
                 publish_date, content, book_type, picture_url, ini_price, sell_price):
        # self.book_id = book_id
        self.isbn = isbn
        self.book_name = book_name
        self.author = author
        self.publisher = publisher
        self.publish_date = publish_date
        self.content = content
        self.book_type = book_type
        self.picture_url = picture_url
        self.ini_price = ini_price
        self.sell_price = sell_price


class SellBook(db.Model):
    pri_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, nullable=True)
    seller_id = db.Column(db.Integer, nullable=True)
    # buyer_id = db.Column(db.Integer, nullable=True)
    is_sold = db.Column(db.Boolean)

    """
    :return: 
    :param
    :param
    
    """
    def __init__(self, book_id, seller_id, is_sold=False):
        self.book_id = book_id
        self.seller_id = seller_id
        # self.buyer_id = buyer_id
        self.is_sold = is_sold
        # self.selling_mode = selling_mode


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.Integer, nullable=True)
    seller_id = db.Column(db.Integer, nullable=True)
    book_id = db.Column(db.Integer)
    user_name = db.Column(db.String(64))
    money = db.Column(db.Float)
    order_date = db.Column(db.String(64))
    phone = db.Column(db.String(64))
    address = db.Column(db.String(64))
    book_name = db.Column(db.String(64))
    book_content = db.Column(db.String(400))
    picture_url = db.Column(db.String(64))
    paypal = db.Column(db.String(64))

    selling_mode = db.Column(db.Integer())
    is_received = db.Column(db.Boolean)

    def __init__(self, buyer_id, seller_id, book_id, user_name, money, order_date, phone, address,
                 book_name, book_content, picture_url, paypal, selling_mode=0, is_received=False):
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.book_id = book_id
        self.user_name = user_name
        self.money = money
        self.order_date = order_date
        self.phone = phone
        self.address = address
        self.book_name = book_name
        self.book_content = book_content
        self.picture_url = picture_url
        self.paypal = paypal
        self.is_received = is_received
        self.selling_mode = selling_mode


class Contact(db.Model):
    """
    :param mode: 1-> send, 0->receive
    """
    pri_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    date = db.Column(db.String(64))
    content = db.Column(db.String(256))
    mode = db.Column(db.Boolean)

    # date should be produced by the db
    def __init__(self, user_id, receiver_id, date, content, mode):
        self.user_id = user_id
        self.receiver_id = receiver_id
        self.date = date
        self.content = content
        self.mode = mode

