from os import environ
from TheMarch import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    #app.run(HOST, PORT)
    app.run(debug=True, use_reloader=True)
    