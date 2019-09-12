from flask import render_template, url_for, request
from app import app
from app.models import Post

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
            if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
            if posts.has_prev else None
    return render_template('index.html', title='Home', posts=posts.items,
                            next_url=next_url, prev_url=prev_url)
