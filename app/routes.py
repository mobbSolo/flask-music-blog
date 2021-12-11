from flask import render_template, url_for, request, redirect, flash
from string import Template
from app import app
from app.models import Post, User
from app.forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required

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


@app.route('/mapper')
def mapper():
    return render_template('map-shit.html', title="Sandpaper's Guide to Austin")


#  @app.route('/videos/<vid>')
#  def videos(vid):
    #  vidtemplate = Template("""
        #  <h2>
          #  Video link:
          #  <a href="https://www.youtube.com/watch?v=${youtube_id}">
            #  ${youtube_id}
          #  </a>
        #  </h2>
#
        #  <iframe src="https://www.youtube.com/embed/${youtube_id}" width="569" height="315" frameborder="2" allowfullscreen></iframe>
    #  """)
#
    #  return render_template('videos.html', title='Videos', content=vidtemplate.substitute(youtube_id=vid))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('admin.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
# @login_required
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    logout_user()
    return 'Logged Out'
