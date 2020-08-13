from july_blog import app, db, Message, mail
from flask import render_template, request, redirect, url_for

# Import for Forms
from july_blog.forms import UserInfoForm, BlogPostForm, LoginForm

# Import for Models
from july_blog.models import User, Post, check_password_hash

# Import for Flask Login - login_required, login_user, current_user, logout_user
from flask_login import login_required, login_user, current_user, logout_user

# Home route
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template("home.html", posts=posts)

# Register route
@app.route('/register',  methods=['GET','POST'])
def register():
    form = UserInfoForm()
    if request.method == 'POST' and form.validate():
        # Get Information
        username = form.username.data
        password = form.password.data
        email = form.email.data
        print("\n", username, password, email)
        # Create an instance of User
        user = User(username,email,password)
        # Open and insert into database
        db.session.add(user)
        # Save info into database
        db.session.commit()

        # Flask Email Sender
        msg = Message(f'Thanks for signing up, {username}!', recipients=[email])
        msg.body = ('Congrats on signing up! Looking forward to your posts!')
        msg.html = ('<h1>Welcome to the July Blog!</h1>' '<p>This will be fun!</p>')

        # Sending the message
        mail.send(msg)
    return render_template("register.html", form = form)

# Creating post
@app.route('/create-a-post', methods=['GET','POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        user_id = current_user.id # This will work because we have "login_required" on this route - otherwise we would have a server error
        content = form.content.data
        print("\n", title, content)
        post = Post(title,content, user_id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('create_post'))
    return render_template("createposts.html", form=form)

# Retrieving Post - seeing details on a post
@app.route('/posts/<int:post_id>') # The wrapper here <> can pass into the function
@login_required
def post_detail(post_id):
    post = Post.query.get_or_404(post_id) # _or_404 throws a 404 error if the post doesn't exist
    return render_template('post_detail.html', post=post)

# Updating posts
@app.route('/posts/update/<int:post_id>', methods=['GET','POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    update_form = BlogPostForm()

    if request.method == 'POST' and update_form.validate():
        title = update_form.title.data
        content = update_form.content.data
        user_id = current_user.id
        
        # Update post with form info
        post.title = title
        post.content = content
        post.user_id = user_id

        # Commit change to db - don't need to add because we're just changing the data, not adding a new entry
        db.session.commit()
        return redirect(url_for('post_update', post_id=post.id))

    return render_template('post_update.html', update_form=update_form)

# Deleting posts
@app.route('/posts/delete/<int:post_id>', methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        logged_user = User.query.filter(User.email == email).first()
        if logged_user and check_password_hash(logged_user.password, password):
            login_user(logged_user)
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))