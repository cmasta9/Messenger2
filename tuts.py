from flask import Flask, render_template
from flask_socketio import SocketIO
import json
import auth

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY=auth.getSec())
sock = SocketIO(app)

@app.route('/')
def index():
    return render_template('base.html')

app.add_url_rule('/','index')
app.register_blueprint(auth.bp)

@sock.on('connect')
def conn():
    sock.emit('serverConn')

@sock.on('message')
def mess(d):
    j = json.loads(d)
    print(f'received a message: {j}')
    sock.emit('response',json.dumps({'user':j['user'],'message':j['message']}))
        
    
if __name__ == '__main__':
    sock.run(app,debug=True)