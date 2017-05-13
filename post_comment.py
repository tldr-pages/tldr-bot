from flask import Flask, request, make_response
import requests
import os
import sys

app = Flask(__name__)

GITHUB_URL = os.getenv("GITHUB_URL", None)
BOT_TOKEN = os.getenv("BOT_TOKEN", None)
REPO_SLUG = os.getenv("REPO_SLUG", None)

if GITHUB_URL == None or BOT_TOKEN == None or REPO_SLUG == None:
  print "Environment variables are not set"
  sys.exit(1)

@app.route('/', methods=['POST'])
def post_comment():
  pr_data = request.get_json()
  if pr_data is None:
    return make_response("Mimetype is not set to application/json", 500)
  pr_id = pr_data["pr_id"]
  url = '{api_url}/repos/{slug}/issues/{number}/comments'.format(api_url=GITHUB_URL, slug=REPO_SLUG, number=pr_id)
  json_data = {'body' : pr_data['body']}
  auth_token = 'token ' + BOT_TOKEN
  headers = {'Authorization': auth_token}
  r = requests.post(url, json=json_data, headers=headers)

  #Send response back to github
  return_code = r.status_code
  if return_code == 201:
    return_string = 'success'
    status_code = 200
  else:
    return_string = r.text
    status_code = 500
  return make_response(return_string, status_code)

@app.route('/test', methods=["GET"])
def test_path():
  return make_response("OK", 200)
