from flask import render_template, url_for, request
from string import Template
from app import app
from app.models import Post

@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
            page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('index', page=posts.next_num) \
            if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
            if posts.has_prev else None
    return render_template('index.html', title='Home', posts=posts.items,
                            next_url=next_url, prev_url=prev_url)

@app.route('/videos/<vid>')
def videos(vid):
    vidtemplate = Template("""
        <h2>
          Video link:
          <a href="https://www.youtube.com/watch?v=${youtube_id}">
            ${youtube_id}
          </a>
        </h2>

        <iframe src="https://www.youtube.com/embed/${youtube_id}" width="569" height="315" frameborder="2" allowfullscreen></iframe>
    """)

    # return vidtemplate.substitute(youtube_id=vid)
    return render_template('videos.html', title='Videos', content=vidtemplate.substitute(youtube_id=vid))
