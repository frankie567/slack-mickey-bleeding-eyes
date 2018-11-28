from flask import abort, Flask, request
import hashlib
import hmac
import os

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

app = Flask(__name__)

def verify_signature(timestamp, signature):
    req = str.encode('v0:' + str(timestamp) + ':') + request.data
    request_hash = 'v0=' + hmac.new(
        str.encode(SLACK_SIGNING_SECRET),
        req, hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(request_hash, signature)

@app.route('/', methods=['POST'])
def mickey_bleeding_eyes_command():
    req_timestamp = request.headers.get('X-Slack-Request-Timestamp')
    req_signature = request.headers.get('X-Slack-Signature')
    if req_timestamp is None or req_signature is None or not verify_signature(req_timestamp, req_signature):
        return abort(401)

    return 'https://media1.tenor.com/images/1f23440dadb7f1d30749d0f41706bd48/tenor.gif?itemid=9801173', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')
