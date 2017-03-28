from flask import Flask, request
from deploy import update_k8s

app = Flask(__name__)

@app.route('/')
def index():
    return 'Up and running '

@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    if not request.json:
        abort(400)
    update_k8s(request.json)
    return 'Deployed OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)