from flask import Flask, render_template, request, redirect, url_for, session, g
import config
from db import BookStore
from login import login_required

app = Flask(__name__)
app.config.from_object(config)
BookStore = BookStore()


@app.route('/')
def index():
    books = BookStore.showBook()
    return render_template('index.html', books=books)


@app.route('/order')
@login_required
def order():
    username = g.username
    orders = BookStore.selectOrder(username)
    return render_template('order.html', orders=orders)


@app.route('/comments')
def comments():
    comments = BookStore.selectComment()
    complains = BookStore.selectComplain()
    return render_template('comments.html', comments=comments,  complains=complains)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if BookStore.verfiy_user(username, password):
            session['username'] = username
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'帐号或密码错误'


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if BookStore.select_user(username):
            return u'该用户已存在'
        else:
            BookStore.insert_user(username, password)
            return redirect(url_for('login'))


@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    books = BookStore.selectBook(keyword)
    return render_template('index.html', books=books)


@app.route('/buy/<ISBN>', methods=['GET','POST'])
@login_required
def buy(ISBN):
    if request.method == 'GET':
        book = BookStore.selectISBN(ISBN)
        return render_template('buy.html', book=book, ISBN=ISBN)
    else:
        username = g.username
        telephone = request.form.get('telephone')
        address = request.form.get('address')
        note = request.form.get('note')
        print('telephone')
        BookStore.insertOrder(ISBN,username,telephone,address,note)
        return redirect(url_for('order'))


# @app.route('/addOrder/<ISBN>')
# def addOrder(ISBN):
#     print('addOrder:', ISBN)
#     BookStore.insertOrder(ISBN, g.username)
#     return redirect(url_for('order'))


@app.before_request
def before_request():
    username = session.get('username')
    if username:
        username = BookStore.selectUser(username)
        if username:
            g.username = username


@app.context_processor
def content_processor():
    if hasattr(g, 'username'):
        return {'username': g.username}
    return {}


@app.route('/root')
def root():
    results = BookStore.selectRoot()
    return render_template('root.html', users=results)


@app.route('/bookRoot')
def bookRoot():
    results = BookStore.selectBookUser()
    return render_template('bookRoot.html', books=results)


@app.route('/commmentRoot')
def commentRoot():
    results = BookStore.selectComment()
    return render_template('commentRoot.html', comments=results)


@app.route('/complainRoot')
def complainRoot():
    results = BookStore.selectComplain()
    return render_template('complainRoot.html', complains=results)


@app.route('/fast')
def fast():
    results = BookStore.selectLogistics()
    return render_template('fast.html', logistics=results)

@app.errorhandler(404)
def error404(error_info):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
