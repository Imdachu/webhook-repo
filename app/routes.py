from flask import Blueprint, request, jsonify, current_app, render_template
from app.extensions import mongo
from bson.json_util import dumps

main = Blueprint('main', __name__)

@main.route('/webhook/receiver', methods=['POST'])
def webhook_receiver():
    event_type = request.headers.get('X-GitHub-Event')
    payload = request.get_json()
    current_app.logger.info(f"Received event: {event_type}")
    current_app.logger.info(f"Payload: {payload}")

    if event_type == 'push':
        author = payload.get('pusher', {}).get('name')
        to_branch = payload.get('ref', '').split('/')[-1]
        timestamp = payload.get('head_commit', {}).get('timestamp')
        current_app.logger.info(f"Push event - author: {author}, to_branch: {to_branch}, timestamp: {timestamp}")

        # Store in MongoDB
        event_doc = {
            'action': 'PUSH',
            'author': author,
            'to_branch': to_branch,
            'timestamp': timestamp
        }
        mongo.db.actions.insert_one(event_doc)

    if event_type == 'pull_request':
        pr = payload.get('pull_request', {})
        action = payload.get('action')
        author = pr.get('user', {}).get('login')
        from_branch = pr.get('head', {}).get('ref')
        to_branch = pr.get('base', {}).get('ref')
        timestamp = pr.get('created_at')
        current_app.logger.info(f"Pull request event - author: {author}, from_branch: {from_branch}, to_branch: {to_branch}, timestamp: {timestamp}")

        # Detect merge event
        if action == 'closed' and pr.get('merged'):
            merged_at = pr.get('merged_at')
            current_app.logger.info(f"Merge event - author: {author}, from_branch: {from_branch}, to_branch: {to_branch}, timestamp: {merged_at}")

        # Store in MongoDB (for non-merge PR events)
        if action != 'closed' or not pr.get('merged'):
            event_doc = {
                'action': 'PULL_REQUEST',
                'author': author,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': timestamp
            }
            mongo.db.actions.insert_one(event_doc)

        # Store in MongoDB (for merge events)
        if action == 'closed' and pr.get('merged'):
            event_doc = {
                'action': 'MERGE',
                'author': author,
                'from_branch': from_branch,
                'to_branch': to_branch,
                'timestamp': merged_at
            }
            mongo.db.actions.insert_one(event_doc)

    return '', 204

@main.route('/api/actions', methods=['GET'])
def get_actions():
    # Fetch all events, sorted by timestamp descending
    events = list(mongo.db.actions.find().sort('timestamp', -1))
    # Convert MongoDB documents (with ObjectId) to JSON-serializable format
    return dumps(events), 200, {'Content-Type': 'application/json'}

@main.route('/')
def index():
    return render_template('index.html') 