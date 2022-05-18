import os
#from .. import app
import secrets
from . import main
from .. import db
from ..models import Comment, Blog
from ..requests import get_random_quote
from .forms import BlogForm, UpdateProfile
from flask_login import current_user, login_required
from flask import render_template, flash, request, url_for, abort, redirect
from PIL import Image #pillow extension for images

@main.route('/')
@main.route('/home')
def index():
    quotes = get_random_quote()
    blogs = Blog.query.all()
    return render_template('index.html', quotes = quotes, blog = blogs, user = current_user)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/photos', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@main.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('Account has been updated.')

        return redirect(url_for('main.profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'photos/' + current_user.image_file)

    title = 'Blog App | Profile'
    return render_template('profile/profile.html', title = title, image_file = image_file, form = form)

@main.route('/blog/<int:blog_id>')
@login_required
def blog(blog_id):
    comments = Comment.query.filter_by(blog_id = blog_id).all()
    heading = 'comments'
    blog = Blog.query.get_or_404(blog_id)

    title = 'Blog App | Blog'
    return render_template('blog.html', title = title, blog = blog, comments = comments, heading = heading)

@main.route('/new_blog', methods = ['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(title = form.title.data, body = form.body.data, user = current_user)
        blog.save_blog()

        flash('Your blog has been uploaded.')

        return redirect(url_for('main.index'))
    title = 'Blog App | Blog'
    return render_template('newBlog.html', title = title, form = form)

@main.route('/blog/<int:blog_id>/update', methods = ['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.user  != current_user:

        abort(403)
    form = BlogForm()

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.body = form.body.data

        db.session.commit()

        flash('Blog has been uploaded.')

        return redirect(url_for('main.blog', blog_id = blog_id))

    elif request.method == 'GET':
        form.title.data = blog.title
        form.body.data = blog.body

    title = 'Blog App | Update'
    return render_template('blog/new_blog.html', title = title, form = form)

@main.route('/comment/<blog_id>', methods=['POST', 'GET'])
@login_required
def comment(blog_id):
    comment = request.form.get('new comment')

    new_comment = Comment(comment = comment, user_id = current_user._get_current_object().id, blog_id = blog_id)

    new_comment.save_comment()

    return redirect(url_for('main.blog', blog_id = blog_id))


@main.route("/blog/<int:blog_id>/delete", methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    if blog.user != current_user:
        abort(403)

    blog.delete_blog()

    flash('Post deleted', 'success')

    return redirect(url_for('main.index'))
