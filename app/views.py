from flask import jsonify
from operator import or_, and_
from app import models
from db import db
from app import app, login_manager
from app.forms import *
from flask import render_template, request, session, flash, make_response, send_file, send_from_directory, redirect, \
    url_for
import os, time
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from config import IMAGE_PATH
from flask_login import login_user, login_required, logout_user, current_user


@login_manager.user_loader  # 使用user_loader装饰器的回调函数非常重要，他将决定 user 对象是否在登录状态
def user_loader(user_id):  # 这个id参数的值是在 login_user(user)中传入的 user 的 id 属性
    return models.User.query.filter(models.User.user_id == user_id).first()


@app.route('/', methods=["GET", "POST"])
def hello_world():
    form = LoginForm(request.form)
    return render_template('login.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'GET':
        # print('get')
        return render_template('login.html', form=form)
    elif request.method == 'POST':

        if form.validate():
            name = form.name.data
            pw = form.password.data
            # print(name)
            data = models.User.query.filter(and_(models.User.name == name, models.User.password == pw)).count()
            # print(data)
            if data > 0:
                user = models.User.query.filter(models.User.name == name).first()
                login_user(user)

                session['user_name'] = name

                return redirect(url_for('search_book'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('user_name', None)
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    error = ''
    if request.method == 'GET':
        return render_template('register.html', form=form, error=error)
    elif request.method == 'POST':
        name = form.name.data
        password1 = form.password1.data
        password2 = form.password2.data

        email = form.email.data
        address = form.address.data
        phone = form.phone.data
        paypal = form.paypal.data

        has_phone = models.User.query.filter(models.User.phone == phone).count()
        has_name = models.User.query.filter(models.User.name == name).count()

        if password1 == password2:
            if has_phone == 0 and has_name == 0:
                me = models.User(name, password1, email, address, phone, paypal)
                db.session.add(me)
                db.session.commit()
                return redirect(url_for("login"))
            else:
                error = '手机号或昵称重复'
                return render_template('register.html', form=form, error=error)
        else:
            error = '密码不一致'
            return render_template('register.html', form=form, error=error)


@app.route('/h_modify_user_info', methods=['GET', 'POST'])
@login_required
def h_modify_user_info():
    form = ChangeUserInfo(request.form)
    error = ''
    user_id = current_user.get_id()
    user = models.User.query.filter(models.User.user_id == user_id).first()
    if request.method == 'GET':
        return render_template('h_modify_user_info.html', user=user, form=form, error=error)
    elif request.method == 'POST':

        password1 = form.password1.data
        password2 = form.password2.data

        email = form.email.data
        address = form.address.data
        phone = form.phone.data
        paypal = form.paypal.data

        has_phone = models.User.query.filter(models.User.phone == phone).count()

        if password1 == password2:
            if has_phone <= 1:
                user.phone = phone
                user.email = email
                user.paypal = paypal
                user.password = password1
                user.address = address
                db.session.commit()
                return redirect(url_for("h_search_book"))
            else:
                error = '手机号重复'
                return render_template('h_modify_user_info.html', user=user, form=form, error=error)
        else:
            error = '密码不一致'
            return render_template('h_modify_user_info.html', user=user, form=form, error=error)


@app.route('/upload_book', methods=['GET', 'POST'])
@login_required
def upload_book():
    form = BookForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'GET':
        return render_template('upload_book.html', form=form)
    elif request.method == 'POST' and form.validate():

        isbn = form.isbn.data
        book_name = form.book_name.data
        author = form.author.data
        publisher = form.publisher.data
        publish_date = form.publish_date.data
        content = form.content.data
        book_type = form.book_type.data

        ini_price = form.ini_price.data
        sell_price = form.sell_price.data

        picture = form.picture.data
        picture_url = picture.filename

        filename = secure_filename(picture.filename)

        picture.save(os.path.join(
            IMAGE_PATH, filename
        ))

        book = models.Book(isbn, book_name, author, publisher, publish_date, content,
                           book_type, picture_url, ini_price, sell_price)
        db.session.add(book)
        db.session.flush()
        book_id = book.book_id

        db.session.commit()
        sell_book = models.SellBook(book_id, current_user.user_id, False)

        db.session.add(sell_book)
        db.session.commit()

        return 'ok upload'
    return render_template('upload_book.html', form=form)


@app.route('/h_search_book', methods=['GET', 'POST'])
@login_required
def h_search_book():
    if request.method == 'POST' and request.form['searching_book'] != "":
        searching_content = request.form['searching_book']
        page = request.args.get('page', 1, type=int)
        book_list = [i.book_id for i in models.SellBook.query.filter(models.SellBook.is_sold == False)]

        pagination = models.Book.query.filter(models.Book.book_id.in_(book_list)).filter(
            or_(models.Book.book_name.like("%" + searching_content + "%"),
                models.Book.content.like("%" + searching_content + "%"))
        ).order_by(
            models.Book.book_id).paginate(
            page, per_page=12, error_out=False)
        books = pagination.items

        return render_template('h_search_book.html', books=books, pagination=pagination)


    elif request.method == 'GET' and request.args.get('search_type') != "":
        searching_content = request.args.get('search_type')

        page = request.args.get('page', 1, type=int)
        book_list = [i.book_id for i in models.SellBook.query.filter(models.SellBook.is_sold == False)]

        pagination = models.Book.query.filter(models.Book.book_id.in_(book_list)).filter(
            or_(models.Book.book_type.like("%" + searching_content + "%"),
                models.Book.content.like("%" + searching_content + "%"))
        ).order_by(
            models.Book.book_id).paginate(
            page, per_page=12, error_out=False)
        books = pagination.items

        return render_template('h_search_book.html', books=books, pagination=pagination)

    else:
        page = request.args.get('page', 1, type=int)
        book_list = [i.book_id for i in models.SellBook.query.filter(models.SellBook.is_sold == False)]

        pagination = models.Book.query.filter(models.Book.book_id.in_(book_list)).order_by(
            models.Book.book_id).paginate(
            page, per_page=12, error_out=False)
        books = pagination.items

        return render_template('h_search_book.html', books=books, pagination=pagination)


@app.route('/search_book', methods=['GET', 'POST'])
@login_required
def search_book():
    if request.method == 'POST' and request.form['searching_book'] != "":
        searching_content = request.form['searching_book']
        page = request.args.get('page', 1, type=int)
        book_list = [i.book_id for i in models.SellBook.query.filter(models.SellBook.is_sold == False)]

        pagination = models.Book.query.filter(models.Book.book_id.in_(book_list)).filter(
            or_(models.Book.book_name.like("%" + searching_content + "%"),
                models.Book.content.like("%" + searching_content + "%"))
        ).order_by(
            models.Book.book_id).paginate(
            page, per_page=12, error_out=False)
        books = pagination.items

        return render_template('search_book.html', books=books, pagination=pagination)


    else:
        page = request.args.get('page', 1, type=int)
        book_list = [i.book_id for i in models.SellBook.query.filter(models.SellBook.is_sold == False)]

        pagination = models.Book.query.filter(models.Book.book_id.in_(book_list)).order_by(
            models.Book.book_id).paginate(
            page, per_page=12, error_out=False)
        books = pagination.items

        return render_template('search_book.html', books=books, pagination=pagination)


@app.route('/book_info', methods=['GET'])
@login_required
def book_info():
    """
    构造一个带有book-id的url
    :return: book: the Book class to the book_info.html
    :param book_id: from the url ? book_id=23
    :param
    """
    book_id = request.args.get('book_id')
    if len(book_id) == 0:
        return redirect(url_for('search_book'))
    book = models.Book.query.filter(models.Book.book_id == book_id).first()
    sell_book = models.SellBook.query.filter(models.SellBook.book_id == book_id).first()
    seller = models.User.query.filter(models.User.user_id == sell_book.seller_id).first()
    return render_template('h_book_info.html', book=book, seller=seller)


@app.route('/book_info_buyer', methods=['GET'])
@login_required
def book_info_buyer():
    """
    构造一个带有book-id的url
    :return: book: the Book class to the book_info.html
    :param book_id: from the url ? book_id=23
    :param
    """
    book_id = request.args.get('book_id')
    if len(book_id) == 0:
        return redirect(url_for('search_book'))
    book = models.Book.query.filter(models.Book.book_id == book_id).first()
    sell_book = models.SellBook.query.filter(models.SellBook.book_id == book_id).first()
    seller = models.User.query.filter(models.User.user_id == sell_book.seller_id).first()
    return render_template('h_book_info_for_buyer.html', book=book, seller=seller)


@app.route('/order', methods=['GET'])
def order():
    """
    :param book_id:
    :param type: 0->online 1->offline
    :return: order_list: contains the Order[]
    """
    if request.args.get('book_id'):
        book_id = request.args.get('book_id')
        _type = request.args.get('type')
        sold_book = models.SellBook.query.filter(models.SellBook.book_id == book_id).first()
        sold_book.is_sold = True
        seller_id = sold_book.seller_id
        db.session.commit()

        _book_info = models.Book.query.filter(models.Book.book_id == book_id).first()
        buyer_id = current_user.user_id
        buyer_name = current_user.name

        seller = models.User.query.filter(models.User.user_id == seller_id).first()
        paypal = seller.paypal

        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if _type == 'offline':
            selling_mode = 1
        else:
            selling_mode = 0

        _order = models.Orders(buyer_id, seller_id, book_id, buyer_name, _book_info.sell_price, _time,
                               current_user.phone, current_user.address, _book_info.book_name, _book_info.content,
                               _book_info.picture_url, paypal, selling_mode, False)
        db.session.add(_order)
        db.session.commit()
        return redirect(url_for("order"))

    buyer_id = current_user.user_id
    order_list = models.Orders.query.filter(models.Orders.buyer_id == buyer_id).order_by(models.Orders.book_id.desc())
    # order_list = models.Orders.query.all()

    return render_template('h_order.html', order_list=order_list)


# unfinished
@app.route('/confirm_receive', methods=['GET', 'POST'])
@login_required
def confirm_receive():
    if request.args.get('book_id'):
        book_id = request.args.get('book_id')
        _order = models.Orders.query.filter(models.Orders.book_id == book_id).first()
        _order.is_received = True
        db.session.commit()
    return redirect(url_for('order'))


@app.route('/seller_order', methods=['GET'])
@login_required
def seller_order():
    """
    :param book_id:
    :param type: 0->online 1->offline
    :return: order_list: contains the Order[]
    """

    seller_id = current_user.user_id
    order_list = models.Orders.query.filter(models.Orders.seller_id == seller_id).order_by(
        models.Orders.order_date.desc())

    return render_template('h_seller_order.html', order_list=order_list)


@app.route('/seek_book', methods=['GET', 'POST'])
@login_required
def seek_book():
    form = SeekBookForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'GET':
        return render_template('seek_book.html', form=form)
    elif request.method == 'POST' and form.validate():

        isbn = form.isbn.data if form.isbn.data != '' else 'None'
        book_name = form.book_name.data if form.book_name.data != '' else 'None'
        author = form.author.data if form.author.data != '' else 'None'
        publisher = form.publisher.data if form.publisher.data != '' else 'None'
        publish_date = form.publish_date.data if form.publish_date.data != '' else 'None'
        content = form.content.data if form.content.data != '' else 'None'
        book_type = form.book_type.data if form.book_type.data != '' else 'None'

        ini_price = form.ini_price.data if form.ini_price.data != '' else 0
        sell_price = form.sell_price.data if form.sell_price.data != '' else 0
        if form.picture.data:

            picture = form.picture.data
            picture_url = picture.filename

            filename = secure_filename(picture.filename)

            picture.save(os.path.join(
                IMAGE_PATH, filename
            ))
        else:
            picture_url = "-2.png"

        book = models.SeekBook(isbn, book_name, author, publisher, publish_date, content,
                               book_type, picture_url, ini_price, sell_price)
        db.session.add(book)
        db.session.flush()
        # book_id = book.book_id
        # print(book_id)
        # print(current_user.user_id)
        db.session.commit()

        return 'ok seek'
    return render_template('seek_book.html', form=form)


@app.route('/seek_book_list', methods=['GET'])
@login_required
def seek_book_list():
    page = request.args.get('page', 1, type=int)

    pagination = models.SeekBook.query.filter(models.SeekBook.book_id > 0).order_by(models.SeekBook.book_id).paginate(
        page, per_page=12, error_out=False)
    seek_book_list = pagination.items

    return render_template('seek_book_list.html', seek_book_list=seek_book_list, pagination=pagination)


@app.route('/h_seek_book_list', methods=['GET'])
@login_required
def h_seek_book_list():
    page = request.args.get('page', 1, type=int)

    pagination = models.SeekBook.query.filter(models.SeekBook.book_id > 0).order_by(models.SeekBook.book_id).paginate(
        page, per_page=12, error_out=False)
    seek_book_list = pagination.items

    return render_template('h_seek_book_list.html', seek_book_list=seek_book_list, pagination=pagination)


@app.route('/test', methods=['GET', 'POST'])
def test():
    # form = TestForm(CombinedMultiDict((request.files, request.form)))
    #
    # if request.method == 'GET':
    #     return render_template('seek_book.html', form=form)
    # elif request.method == 'POST' and form.validate():
    #     print(form.isbn.data != '')
    #     print(form.author.data == '')
    #     print(form.book_name.data == '')
    #     # return redirect(url_for('order', name='name'))
    return render_template('chat.html')


def get_chat_list(user_id):
    chat_dict = dict()
    a = set()
    chaters1 = models.Contact.query.filter(models.Contact.user_id == user_id)
    chaters2 = models.Contact.query.filter(models.Contact.receiver_id == user_id)
    for i in chaters1:
        a.add(i.receiver_id)
    for i in chaters2:
        a.add(i.receiver_id)
    for j in a:
        chat_dict[j] = models.User.query.filter(models.User.user_id == j).first().name
    return chat_dict


@app.route('/get_content', methods=['GET'])
def get_chat_content():
    user_id = current_user.get_id()
    if request.args.get('receiver_id'):
        receiver_id = request.args.get('receiver_id')
    else:
        receiver_id = 0
    chat_content = models.Contact.query.filter(or_(and_(models.Contact.user_id == user_id,
                                                        models.Contact.receiver_id == receiver_id),
                                                   and_(models.Contact.user_id == receiver_id,
                                                        models.Contact.receiver_id == user_id))).order_by(
        models.Contact.pri_id)
    result = []
    for i in chat_content:
        result.append(i.content)
    # return chat_content
    return result


@app.route('/chat', methods=['GET'])
@login_required
def chat():
    user_id = current_user.get_id()

    chaters = get_chat_list(user_id)
    chat_content = ['']
    print(chaters)
    return render_template('chat.html', chaters=chaters, chat_content=chat_content)
