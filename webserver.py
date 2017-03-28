from flask import Flask, request
from deploy import update_k8s

app = Flask(__name__)

@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    if not request.json:
        abort(400)
    update_k8s(request.json)
    return ''

if __name__ == "__main__":
    app.run()