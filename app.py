from flask import Flask, session, render_template, request, flash, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, logout_user, current_user, login_user, login_required
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///swapify.db'
app.config["SECRET_KEY"] = "abc"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class SonnyItems(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    series = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    mrk_value = db.Column(db.Float, nullable=False)
    images = relationship("ItemImage", back_populates="item")
    favorite = db.Column(db.Boolean, default=0)

    def __repr__(self):
        return f'<SonnyItems {self.name}>'


class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_id = db.Column(db.Integer, db.ForeignKey('sonny_items.id'))
    url = db.Column(db.String(200), nullable=False)
    item = relationship("SonnyItems", back_populates="images")

    def __repr__(self):
        return f'<ItemImage {self.id}>'

class Socials(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_media = db.Column(db.String(200), nullable=False)
    social_link = db.Column(db.String(200), nullable=False)
    social_username = db.Column(db.String(200), nullable=False)
    user = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<createAccount {self.social_media}>'


@app.route('/')
def start():
    sonny_items = SonnyItems.query.order_by(SonnyItems.id).all()
    return render_template('index.html', items=sonny_items)


@app.route('/index')
def index():
    sonny_items = SonnyItems.query.order_by(SonnyItems.id).all()
    return render_template('index.html', items=sonny_items)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        try:
            input_ = request.form['email-text']
            password_ = request.form['pass-text']

            email_pass = db.session.query(createAccount).filter_by(email=input_, password=password_).first()
            user_pass = db.session.query(createAccount).filter_by(username=input_, password=password_).first()

            if email_pass:
                login_user(email_pass)
                flash('You are logged in!', 'info')
                return redirect(url_for('index'))
            elif user_pass:
                login_user(user_pass)
                flash('You are logged in!', 'info')
                return redirect(url_for('index'))
            else:
                flash('Wrong username and password combination. Please try again', 'error')
                return redirect(url_for('login'))
        except Exception as e:
            flash('Something went wrong on the server. Please try again', 'error')
            print("Exception caught " + str(e))
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@login_manager.user_loader
def load_user(user_id):
    return createAccount.query.get(user_id)


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
            user = createAccount(firstName=first, lastName=last, username=user, email=em, password=passw)
            try:
                db.session.add(user)
                db.session.commit()
                flash('You signed up!', 'info')
                login_user(user)
                flash(f'You signed up and are now logged in as {current_user.username}', 'info')
                return redirect(url_for('index'))
            except Exception as e:
                print("Exception:", e)
                flash('There was an issue adding one of your inputs.', 'error')
                return redirect(url_for('create'))

    else:
        return render_template('create-account.html')


class createAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200), nullable=False)
    lastName = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<createAccount {self.firstName}>'


@app.route('/logout')
def logout():
    session.pop('username', None)
    logout_user()
    flash('You have successfully logged yourself out.')
    return render_template('login.html')


@app.route('/profile')
def profile():
    if current_user.is_authenticated:
        sonny_items = SonnyItems.query.filter_by(user=current_user.username).order_by(SonnyItems.id).all()
        social_links = Socials.query.filter_by(user=current_user.username).all()
        user = createAccount.query.filter_by(username=current_user.username).first()
        return render_template('profile.html', items=sonny_items, user=user, media=social_links)
    else:
        return render_template('login.html')


@app.route('/user/<username>')
def user_profile(username):
    user_ = createAccount.query.filter_by(username=username).first()
    socials_ = Socials.query.filter_by(user=username).all()
    users_sonny = SonnyItems.query.filter_by(user=username).all()
    if user_ is None:
        return render_template('index.html')
    return render_template('user_profile.html', items=users_sonny, username=user_.username, first=user_.firstName, last=user_.lastName, socials=socials_)


@app.route('/form')
def form():
    if current_user.is_authenticated:
        return render_template('form.html',)
    else:
        return render_template('login.html')


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
        try:
            name = request.form['name']
            series = request.form['series']
            category = request.form['category']
            mrk_value = request.form['mrk_value']
            images = request.form.getlist('images')  # Get list of all image URLs
            favorite = True if request.form.get('favorite') == 'on' else False

            # Save inventory item with multiple images
            inventory_item = SonnyItems(user=current_user.username, name=name, series=series, category=category, mrk_value=mrk_value, favorite=favorite)
            db.session.add(inventory_item)

            # Add multiple images
            for img_url in images:
                image = ItemImage(url=img_url, item=inventory_item)
                db.session.add(image)

            db.session.commit()
            flash('Inventory item added successfully!', 'success')
            return redirect(url_for('profile'))
        except Exception as e:
            print("Exception:", e)
            flash('Error: Failed to add inventory item. Please try again.', 'error')
            return redirect(url_for('profile'))


@app.route('/edit_inventory/<int:item_id>', methods=['POST'])
def edit_inventory(item_id):
    if request.method == 'POST':
        item = SonnyItems.query.get_or_404(item_id)

        item.name = request.form['name']
        item.series = request.form['series']
        item.category = request.form['category']
        item.mrk_value = request.form['mrk_value']
        item.images = request.form.getlist('images')  # Get list of all image URLs

        item.favorite = True if request.form.get('favorite') == 'true' else False

        # saving information with information.
        inventory_item = SonnyItems(user=current_user.username, name=item.name, series=item.series, category=item.category, mrk_value=item.mrk_value, favorite=item.favorite)

        # upadting multiple images
        for img_url in item.images:
                image = ItemImage(url=img_url, item=inventory_item)
                db.session.add(image)

        try:
            db.session.commit()
            flash('Item has been successfully updated.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error updating item: ' + str(e), 'error')

        return redirect(url_for('profile'))


@app.route('/socials')
def socials():
    return render_template('socials.html', user=current_user)


@app.route('/socials_link', methods=['POST', 'GET'])
def socials_link():
    if request.method == 'POST':
        platform = request.form['platform']
        link = request.form['link']
        username = request.form['username']
        user_ = current_user.username

        try:
            db.session.add(Socials(social_media=platform, social_link=link, social_username=username, user=user_))
            db.session.commit()
            flash('Social media added successfully!', 'success')
            return redirect(url_for('profile'))
        except:
            flash('There was an issue adding one of your inputs.', 'error')
            return redirect(url_for('profile'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)