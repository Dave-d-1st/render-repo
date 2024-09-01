from flask import Flask,request,session,jsonify
import sqlite3
from flask_socketio import SocketIO,emit
import flask_socketio as fs
app=Flask(__name__)
sio=SocketIO(app)

online={}

@app.route('/register',methods=['POST'])
def register():
    data=request.get_json()
    with sqlite3.connect("client.db") as conn:
        c=conn.cursor()
        c.execute("SELECT username FROM users ")
        usernames=c.fetchall()
        print(usernames)
        if( data["username"],) in usernames:
            return "Username in Use", 208
        else:
            c.execute("INSERT INTO users VALUES (:username, :password);",data)
            conn.commit()
    return "Posted", 201

@app.route('/access')
def access():
    username=request.args.get("username")
    password=request.args.get("password")
    print(username,"requested access")
    with sqlite3.connect("client.db") as conn:
        c=conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? and password=?",(username,password))
        dat=c.fetchall()
        conn.commit()
    if dat==[]:
        return "Wrong Username or password", 401
    elif username in online.keys():
        return "User already Online", 401
    else:
        return "Access", 200
    
@sio.on('connect')
def connect():
    name=request.headers["Name"]
    print("Data",name)
    online[name] = request.sid
    session['name'] = name  
    emit('connected',name,broadcast=True,include_self=False)

@sio.on('disconnect')
def disconnect():
    print(online)
    emit('disconnected',session['name'],broadcast=True,include_self=False)
    del online[session['name']]  
    print(online)


@sio.on('broadcast')
def broadcast(data):
    data={"Sender":session['name'],"msg":data}
    print(data)
    emit('response',data,broadcast=True,include_self=False)

@app.route('/online')
def send_online():
    return jsonify(list(online.keys()))

if __name__=="__main__":
    sio.run(app,port=5000,debug=True)