from flask import abort, Flask, jsonify, request
import hashlib
import hmac
import logging
import os

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

app = Flask(__name__)

def verify_signature(timestamp, signature, data):
    req = str.encode('v0:' + str(timestamp) + ':') + data
    request_hash = 'v0=' + hmac.new(
        str.encode(SLACK_SIGNING_SECRET),
        req, hashlib.sha256
    ).hexdigest()

    app.logger.debug('data=%s', data)
    app.logger.debug('request_hash=%s', request_hash)

    return hmac.compare_digest(request_hash, signature)

@app.route('/', methods=['POST'])
def mickey_bleeding_eyes_command():
    req_timestamp = request.headers.get('X-Slack-Request-Timestamp')
    req_signature = request.headers.get('X-Slack-Signature')
    app.logger.debug('Request: X-Slack-Request-Timestamp=%s X-Slack-Signature=%s', req_timestamp, req_signature)
    #if req_timestamp is None or req_signature is None or not verify_signature(req_timestamp, req_signature, request.get_data()):
        #return abort(401)

    return jsonify(
        text='https://i.pinimg.com/originals/ab/c5/02/abc50276a99daa149a51119912de6c70.png',
        as_user=True
    ), 200

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
