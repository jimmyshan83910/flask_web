from flask import Flask, Blueprint, request, jsonify

app2 = Blueprint('app2', __name__)

@app2.route('/meal', methods = ['POST'])
def index_p():
    certification = request.get_json()['Certification']

    return certification
    # return jsonify({'result:': 'OK!'})