from flask import Flask
app = Flask(__name__)
app.config['DEBUG'] = True

import MySQLdb

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


_INSTANCE_NAME = 'junyu-data'
_DB_NAME = 'data' # or whatever name you choose

if (os.getenv('SERVER_SOFTWARE') and
    os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
    _DB = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db=_DB_NAME, user=_USER, charset='utf8')
else:
    _DB = MySQLdb.connect(host='127.0.0.1', port=3306, db=_DB_NAME, user=_USER, charset='utf8')


@app.route('/')
def index():
    template = JINJA_ENVIRONMENT.get_template('templates/index.html')

    cursor = _DB.cursor()
    cursor.execute('SHOW TABLES')
    
    logging.info(cursor.fetchall())

    return template.render()


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404