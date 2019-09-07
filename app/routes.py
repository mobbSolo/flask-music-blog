from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Markie'}
    posts = [
        {
            'title': 'New Beats!',
            'body': 'This is a video of me staring through Alex\'s window at night',
            'link': 'https://www.youtube.com/embed/pZXUo_gf5Do'
        },
        {
            'title': 'Super-Duty-Tough Drums',
            'body': 'You can\'t fake this kinda punch, kadd',
            'link': 'https://www.youtube.com/embed/GVJYvwI1500'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
