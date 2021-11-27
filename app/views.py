from flask import request
from app import app
from datetime import datetime
from app import communication_with_nebula


@app.route('/server-add')
def server_add():
    # if key doesn't exist, returns a 400, bad request error
    cpu = request.args.get('cpu')

    # if key doesn't exist, returns a 400, bad request error
    ram = request.args['ram']

    # if key doesn't exist, returns None
    mem = request.args.get('mem')

    owner = request.args.get('owner')

    date = datetime.now()

    # template of usage: http://127.0.0.1:5000/server-add?cpu=4&ram=4&mem=50&owner=Tulin.D.I
    return '''
              <h1>The cpu value is: {}</h1>
              <h1>The ram value is: {}</h1>
              <h1>The mem value is: {}</h1>
              <h1>The owner value is: {}</h1>
              <h1>The date value is: {}'''.format(cpu, ram, mem, owner, date)


@app.route('/query-example')
def query_example():
    # http://127.0.0.1:5000/query-example?language=Python&framework=Flask&website=DigitalOcean
    # if key doesn't exist, returns None
    language = request.args.get('language')

    # if key doesn't exist, returns a 400, bad request error
    framework = request.args['framework']

    # if key doesn't exist, returns None
    website = request.args.get('website')

    return '''
              <h1>The language value is: {}</h1>
              <h1>The framework value is: {}</h1>
              <h1>The website value is: {}'''.format(language, framework, website)
