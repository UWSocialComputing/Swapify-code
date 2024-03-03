from flask import Flask, session, render_template, request, flash, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, logout_user
import uuid


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_nancy.db'
app.config["SECRET_KEY"] = "abc"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def loader_user(user_id):
    return createAccount.query.get(user_id)

class createAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    auth_token = db.Column(db.String(200))
    def __repr__(self):
        return f'<createAccount {self.firstName}>'

class SonnyItems(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    series = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    mrk_value = db.Column(db.Float, nullable=False)
    images = db.Column(db.String(200), nullable=False)
    favorite = db.Column(db.Boolean, default=0)
    def __repr__(self):
        return f'<SonnyItems {self.name}>'

class Socials(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_media = db.Column(db.String(200), nullable=False)
    social_link = db.Column(db.String(200), nullable=False)
    social_username = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return f'<createAccount {self.social_media}>'


@app.route('/')
def index():
     return render_template('index.html')

@app.route('/profile')
def profile():
    sonny_items = SonnyItems.query.all()
    socials = Socials.query.all()
    auth_token = request.cookies.get('auth_token')
    if auth_token:
        user = createAccount.query.filter_by(auth_token=auth_token).first()
        if user:
            return render_template('profile.html', items=sonny_items, media=socials, user=user)

@app.route('/form')
def form():
    return render_template('form.html',)

@app.route('/common')
def common():
    # query through all sonny items
    # only grab the items with common category
    sonny_items = SonnyItems.query.filter(SonnyItems.category.ilike('Common')).all()
    return render_template('common.html', items=sonny_items)

@app.route('/limited')
def limited():
    # query through all sonny items
    # only grab the items with common category
    sonny_items = SonnyItems.query.filter(SonnyItems.category.ilike('Limited')).all()
    return render_template('limited.html', items=sonny_items)


@app.route('/discontinued')
def discontinued():
    # query through all sonny items
    # only grab the items with common category
    sonny_items = SonnyItems.query.filter(SonnyItems.category.ilike('Discontinued')).all()
    return render_template('discontinued.html', items=sonny_items)


@app.route('/secrets')
def secrets():
    # query through all sonny items
    # only grab the items with common category
    sonny_items = SonnyItems.query.filter(SonnyItems.category.ilike('Secret')).all()
    return render_template('secrets.html', items=sonny_items)


@app.route('/robbie')
def robbie():
    # query through all sonny items
    # only grab the items with common category
    sonny_items = SonnyItems.query.filter(SonnyItems.category.ilike('Robby')).all()
    return render_template('robbie.html', items=sonny_items)

@app.route('/favorites')
def favorites():
    return render_template('favorites.html')

@app.route('/add_inventory', methods=['POST'])
def add_inventory():
    if request.method == 'POST':
        name = request.form['name']
        series = request.form['series']
        category = request.form['category']
        mrk_value = request.form['mrk_value']
        images = request.form['images']
        favorite = True if request.form.get('favorite') == 'true' else False

        try:
            db.session.add(SonnyItems(name=name, series=series, category=category, mrk_value=mrk_value, images=images, favorite=favorite))
            db.session.commit()
            flash('Inventory item added successfully!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            print("Exception:", e) # for debugging
            flash('There was an issue adding one of your inputs.', 'error')
            return redirect(url_for('profile'))

@app.route('/socials')
def socials():
    return render_template('socials.html')

@app.route('/socials_link', methods=['POST', 'GET'])
def socials_link():
    if request.method == 'POST':
        platform = request.form['platform']
        link = request.form['link']
        username = request.form['username']

        try:
            db.session.add(Socials(social_media=platform, social_link=link, social_username=username))
            db.session.commit()
            flash('Social media added successfully!', 'success')
            return redirect(url_for('profile'))
        except:
            flash('There was an issue adding one of your inputs.', 'error')
            return redirect(url_for('profile'))

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        first = request.form['first-text']
        last = request.form['last']
        user = request.form['user-text']
        em = request.form['email-text']
        passw = request.form['pass-text']

        userExists = createAccount.query.filter_by(username=user).first() is not None
        emailExists = createAccount.query.filter_by(email=em).first() is not None
        if userExists:
            flash("Username already exists.", 'error')
            return redirect(url_for('create'))
        elif emailExists:
            flash("Email already exists.", 'error')
            return redirect(url_for('create'))
        else:
            try:
                auth_token = str(uuid.uuid4())
                new_account = createAccount(firstName=first, lastName=last, username=user, email=em, password=passw, auth_token=auth_token)
                db.session.add(new_account)
                db.session.commit()
                response = make_response(redirect(url_for('index')))
                response.set_cookie('auth_token', auth_token)
                flash('You signed up!', 'info')
                return response
            except:
                flash('There was an issue adding your account.', 'error')
                return redirect(url_for('create'))
    else:
        return render_template('create-account.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            logemail = request.form['email-text']
            logpassw = request.form['pass-text']
            combo = createAccount.query.filter_by(email=logemail, password=logpassw).first()

            if combo:
                auth_token = str(uuid.uuid4())
                combo.auth_token = auth_token
                db.session.commit()
                response = make_response(redirect(url_for('index')))
                response.set_cookie('auth_token', auth_token)
                flash('You are logged in!', 'info')
                return response
            else:
                flash('Wrong username and password combination. Please try again', 'error')
                return redirect(url_for('login'))
        except:
            flash('Something went wrong on the server. Please try again', 'error')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    logout_user()
    flash('You have successfully logged yourself out.')
    return render_template('login.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)