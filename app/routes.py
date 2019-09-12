from flask import render_template, url_for
from app import app
from app.models import Post

@app.route('/')
@app.route('/index')
def index():
    # thang = Post.query.first()
    posts = Post.query.order_by(Post.timestamp).all()
        # {
            # 'title': 'New Beats!',
            # 'body': 'This is a video of me staring through Alex\'s window at night',
            # 'link': 'https://www.youtube.com/embed/pZXUo_gf5Do'
        # },
        # {
            # 'title': 'Super-Duty-Tough Drums',
            # 'body': 'You can\'t fake this kinda punch, kadd',
            # 'link': 'https://www.youtube.com/embed/GVJYvwI1500'
        # }
    return render_template('index.html', title='Home', posts=posts )
