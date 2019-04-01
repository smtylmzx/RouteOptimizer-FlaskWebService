from flask import Flask, request
from flask_cors import cross_origin
import routewebservice

app = Flask(__name__)

@app.route("/post", methods=['POST'])
@cross_origin()
def postData():
    data = request.form['data']
    demands = request.form['demands']
    return routewebservice.main(data, demands)

if __name__ == "__main__":
    app.run()
