
from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import login_required, current_user
from .models import Post
from .import db
import json 

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        post = request.form.get('post')

        if len(post) < 1:
            flash('Post is too short!', category='error')
        else:
            new_post = Post(data=post, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post added!', category='success')


    return render_template("home.html", user=current_user)

@views.route('/delete-post', methods=['POST'])
def delete_post():
    post = json.loads(request.data)
    postId = post['postId']
    post = Post.query.get(postId)
    if post:
        if post.user_id == current_user.id:
            db.session.delete(post)
            db.session.commit() 


    return jsonify({}) 