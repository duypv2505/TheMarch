"""
This script runs the TheMarch application using a development server.
"""

from os import environ
from TheMarch import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'https://themarch.herokuapp.com/')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST)
