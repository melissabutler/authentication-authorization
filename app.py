from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback

from forms import RegisterUserForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


debug = DebugToolbarExtension(app)

app.app_context().push()
connect_db(app)
db.create_all()


@app.route('/home')
def render_list():
    """ Show list of users """
    users = User.query.all()

    return render_template('home.html', users=users)

@app.route('/')
def redirect_to_register():
    """ Redirects to registry page """
    return redirect('/register')

@app.route('/register', methods=['POST', 'GET'])
def register_page():
    """Renders and handles registration form"""
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        session["username"] = new_user.username

        return redirect(f'/users/{new_user.username}')

    return render_template('form.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login_page():
    """Renders and handles login form"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password"]
    return render_template('login.html', form=form)

@app.route('/secret')
def secret_page():
    """ Renders secret page"""
    if 'username' not in session:
        flash("You must be logged in to view this page.")
        return redirect('/')

    return render_template('secret.html')

@app.route('/logout')
def logout():
    """ Logs out user"""
    session.pop('username')

    return redirect('/')

################################ USER ########################################

@app.route("/users/<username>", methods=['POST', 'GET'])
def show_user_profile(username):
    """Shows logged-in user profile"""
    if 'username' not in session or username != session['username']:
        flash("You must be logged in to view this profile")
        return redirect('/')
    else:
        user = User.query.get(username) 
        feedback = Feedback.query.filter(Feedback.username == username).all()

        return render_template('user_profile.html', user=user, feedback=feedback)
    
@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
     """ Deletes user """
     if 'username' not in session or username != session['username']:
        flash("You must be logged in to view this profile")
        return redirect('/')
     else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        flash(f"User {username} deleted") 
        return redirect('/')
     
###################### FEEDBACK ###############################

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def feedback_form(username):
    """ Renders feedback form and handles submission"""
    

    if 'username' not in session or username != session['username']:
        flash("You must be logged in to view this profile")
        return redirect('/')
    
    form = FeedbackForm()

    if form.validate_on_submit():

        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{new_feedback.username}')
    else:
        return render_template('feedback_form.html', form=form)
            
        
@app.route('/feedback/<int:feedback_id>/update', methods=["POST", "GET"])
def edit_feedback(feedback_id):
    post = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or post.username != session['username']:
        flash("You must be logged in to view this profile")
        return redirect('/')
    
    form = FeedbackForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data

        db.session.add(post)
        db.session.commit()
        return redirect(f'/users/{post.username}')
    return render_template('feedback_edit.html', form=form, post=post)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    post = Feedback.query.get_or_404(feedback_id)

    if 'username' not in session or post.username != session['username']:
        flash("You must be logged in to alter this profile")
        return redirect('/')
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.username}')