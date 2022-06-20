#!flask/bin/python
from app import app
from nebula_communication.communication_with_nebula import connection_pool

app.run(debug=True)
connection_pool.close()
