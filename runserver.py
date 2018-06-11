"""
This script runs the TheMarch application using a development server.
"""

from os import environ
from TheMarch import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'themarch.herokuapp.com')
    try:
        PORT = int(environ.get('SERVER_PORT', '5000'))
    except ValueError:
        PORT = 5000
    app.run(host='0.0.0.0', port=PORT, debug=True) 
