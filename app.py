#
#  example Flask app that uses flask-track-usage and MongoEngine
#
from flask import (
    Flask,
    render_template,
    g
)
import mongoengine as me
from flask_track_usage import TrackUsage
from flask_track_usage.storage.mongo import MongoEngineStorage
from flask_track_usage.summarization import sumUrl, sumUserAgent

#########################
#
#  SETUP FLASK and JINJA2
#
#########################
app = Flask(__name__)

def datetimeformat(value, format='%Y-%m-%d %H:%M'):
    return value.strftime(format)
app.jinja_env.filters['datetime'] = datetimeformat

#########################
#
#  SETUP MONGOENGINE
#
#########################

me.connect("example_website")

#########################
#
#  SETUP FLASK_TRACK_USAGE
#
#########################

app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'exclude'

traffic_storage = MongoEngineStorage(hooks=[sumUrl, sumUserAgent])
t = TrackUsage(app, [traffic_storage])

#########################
#
#  PUBLIC ROUTES
#
#########################

@app.route('/')
def index():
    g.track_var["something"] = 99
    return render_template('index.html')

@app.route('/page1')
def page_one():
    g.track_var["something"] = 34
    return render_template('other_page.html', page_number=1)

@app.route('/page2')
def page_two():
    return render_template('other_page.html', page_number=2)

##########################
#
#  ADMIN ROUTES
#
##########################

@t.exclude
@app.route('/admin/last20.html')
def last_twenty():
    visits = traffic_storage.get_usage(limit=20)
    return render_template('last20.html', visits=visits)

@t.exclude
@app.route('/admin/last_url.html')
def last_url():
    stats = traffic_storage.get_sum(sumUrl, limit=30, target="http://127.0.0.1:5000/page1")
    return render_template('last_url.html', stats=stats)

@t.exclude
@app.route('/admin/last_useragent.html')
def last_useragent():
    stats = traffic_storage.get_sum(sumUserAgent, limit=40)
    return render_template('last_useragent.html', stats=stats)
