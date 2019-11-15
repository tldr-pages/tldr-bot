#!/usr/bin/env python3

import os
import sys
import requests
from flask import Flask, request, make_response

app = Flask(__name__)

def post_comment(issue_id, body):
    url = '{}/repos/{}/issues/{}/comments'.format(GITHUB_API_URL, REPO_SLUG, issue_id)
    headers = {'Authorization': 'token ' + BOT_TOKEN}
    data = {'body': body}

    return requests.post(url, json=data, headers=headers)


def check_already_commented(issue_id):
    url = '{}/repos/{}/issues/{}/comments'.format(GITHUB_API_URL, REPO_SLUG, issue_id)
    resp = requests.get(url)

    if resp.status_code != 200:
        # GitHub API error, let's say True in this case to avoid problems.
        return True

    comments = resp.json()
    return any(c['user']['login'] == 'tldr-bot' for c in comments)


@app.route('/', methods=['POST']) # old route, to be removed
@app.route('/comment', methods=['POST'])
@app.route('/comment/once', methods=['POST'])
def comment():
    data = request.get_json()

    if data is None:
        return make_response('Invalid JSON or inappropriate Content-Type.', 400)

    pr_id = data.get('pr_id')
    comment_body = data.get('body')

    # Check if request is valid.
    if pr_id is None or comment_body is None:
        return make_response('Missing required JSON fields', 400)

    # If needed, check if already commented.
    if request.path == '/comment/once' and check_already_commented(pr_id):
        return make_response('already commented', 200)

    # Post comment.
    resp = post_comment(pr_id, comment_body)

    if resp.status_code != 201:
        return make_response(resp.text, 500)

    return make_response('success', 200)


@app.route('/status', methods=['GET'])
def status():
    # Health check entpoint for monitoring purposes.
    return make_response('ok', 200)


################################################################################

GITHUB_API_URL = 'https://api.github.com'
BOT_TOKEN = os.getenv('BOT_TOKEN')
REPO_SLUG = os.getenv('REPO_SLUG')

if BOT_TOKEN is None or REPO_SLUG is None:
  print('Needed environment variables are not set.')
  sys.exit(1)
