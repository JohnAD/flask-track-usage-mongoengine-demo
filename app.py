#
#  example Flask app that uses flask-track-usage and MongoEngine
#
from flask import (
    Flask,
    render_template,
)
import mongoengine as me
from flask_track_usage import TrackUsage
from flask_track_usage.storage.mongo import MongoEngineStorage
from flask_track_usage.summarization import sumUrl
from flask_track_usage.summarization.mongoenginestorage import UsageTrackerSumUrlHourly


app = Flask(__name__)

me.connect("example_website")

app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'exclude'

traffic_storage = MongoEngineStorage(hooks=[sumUrl])
t = TrackUsage(app, [traffic_storage])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/page1')
def page_one():
    return render_template('other_page.html', page_number=1)

@app.route('/page2')
def page_two():
    return render_template('other_page.html', page_number=2)

@t.exclude
@app.route('/admin/last20.html')
def last_twenty():
    visits = traffic_storage.get_usage(limit=20)
    return render_template('last20.html', visits=visits)

@t.exclude
@app.route('/admin/last_url.html')
def last_url():
    stats = {}
    stats['hourly'] = UsageTrackerSumUrlHourly.objects[:24]
    return render_template('last_url.html', stats=stats)
