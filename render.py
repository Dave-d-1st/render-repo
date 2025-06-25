from flask import Flask,send_file,request

app=Flask(__name__)

@app.route('/',methods = ["POST"])
def reg():
    with open("s.txt",'w') as f:
        f.write("Butter")
    return "Balls", 200
@app.route('/')
def ge():
    with open("s.txt") as f:
        return f.read(),200

if __name__=="__main__":
    app.run(debug=True,port=35586)