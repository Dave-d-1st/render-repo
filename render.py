from flask import Flask,request,session,jsonify

app=Flask(__name__)

@app.route('/')
def reg():
    return "Posted", 201


if __name__=="__main__":
    app.run()