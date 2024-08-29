from flask import Flask, request, jsonify,redirect

app=Flask(__name__)


@app.route('/get/<user>')
def home(user):
    user_data={
        'id':user,
        'b':'alls'
    }
    extra=request.args.get("extra")
    if extra:
        user_data['extra'] = extra
    print(extra)
    return jsonify(user_data), 200

if __name__=="__main__":
    app.run(debug=True)