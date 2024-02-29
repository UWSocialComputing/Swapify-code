from flask import Flask, session, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, logout_user

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
    def __repr__(self):
        return f'<createAccount {self.username}>'

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/profile')
def profile():
    sonny_items = SonnyItems.query.all()
    return render_template('profile.html', items=sonny_items)


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
    sonny_items = SonnyItems.query.filter(SonnyItems.category.ilike('Robbie')).all()
    return render_template('robbie.html', item=sonny_items)


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


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        first = request.form['first-text']
        last = request.form['last']
        user = request.form['user-text']
        em = request.form['email-text']
        passw = request.form['pass-text']

        userExists = db.session.query(createAccount.id).filter_by(username=user).first() is not None
        emailExists = db.session.query(createAccount.id).filter_by(email=em).first() is not None
        if userExists:
            flash("Username already exists.", 'error')
            return redirect(url_for('create'))
        elif emailExists:
            flash("Email already exists.", 'error')
            return redirect(url_for('create'))
        else:
            try:
                db.session.add(createAccount(firstName=first, lastName=last, username=user, email=em, password=passw))
                db.session.commit()
                flash('You signed up!', 'info')
                return redirect(url_for('index'))
            except:
                flash('There was an issue adding one of your inputs.', 'error')
                return redirect(url_for('create'))

    else:
        return render_template('create-account.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            logemail = request.form['email-text']
            logpassw = request.form['pass-text']

            combo = db.session.query(createAccount).filter_by(email=logemail, password=logpassw).first()

            if combo:
                flash('You are logged in!', 'info')
                return redirect(url_for('index'))
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