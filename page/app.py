import requests
import json
import os

from .models.member import Member
from .common import PATH, logger, oauth_credential
from .database import remote_db, local_db
from livereload import Server
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient


def create_app():
  app = Flask(__name__)
  app.secret_key = "page"

  login_manager = LoginManager()
  login_manager.init_app(app)

  GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

  @app.context_processor
  def inject_global():
    logger.debug("inject_global")
    headers = {doc.doc_id: doc.headers for doc in local_db.get("doc")}
    return dict(headers=headers)

  @login_manager.user_loader
  def load_user(user_id):
    return remote_db.get("member", user_id)

  @app.route("/admin/<string:team_id>", methods=["POST", "GET"])
  def admin(team_id):
    headers = local_db.get("doc", "Python").headers
    html = ""
    member_ids = remote_db.get("team", team_id).member_ids
    members = remote_db.get("member", member_ids)
    members.sort(key=lambda member: len(member.solved_problem_ids))

    problems = local_db.get("problem")
    for h1 in ["Syntax", "Algorithm"]:
      html += f"<h1>{h1}</h1>"
      for h2 in headers[h1]:
        html += f"<h2>{h2}</h2>"
        for h3 in headers[h1][h2]:
          html += f"<h3>{h3}</h3>"
          for problem in problems:
            if problem.gist_id == "":
              continue
            gist = local_db.get("gist", problem.gist_id)
            if gist.h1 == h1 and gist.h2 == h2 and gist.h3 == h3:
              html += problem.link
              html += " ".join([member.kr_name for member in members if problem.problem_id not in member.solved_problem_ids])
              html += "<br>"

    return render_template("admin.html", progress_overview_html=html)

  @app.route("/premium", methods=["POST", "GET"])
  def premium(team_id):
    if request.method == 'POST':
      current_user.team_id = request.form["team_id"]
      remote_db.add("memeber", current_user)
      return redirect(url_for("index"))
    return render_template("premium.html")

  @app.route("/", methods=["GET"])
  @app.route("/page/", methods=["GET"])
  @app.route("/page/<string:cur_doc_id>/", methods=["GET"])
  @app.route("/page/<string:cur_doc_id>/<string:cur_h1>/", methods=["GET"])
  @app.route("/page/<string:cur_doc_id>/<string:cur_h1>/<string:cur_h2>", methods=["GET"])
  @app.route("/page/<string:cur_doc_id>/<string:cur_h1>/<string:cur_h2>/<string:cur_h3>", methods=["GET"])
  def index(cur_doc_id="Python", cur_h1="", cur_h2="", cur_h3=""):
    logger.debug(f"index({cur_doc_id}, {cur_h1}, {cur_h2}, {cur_h3})")
    doc = local_db.get("doc", cur_doc_id)
    if cur_h1 == "":
      cur_h1 = next(iter(doc.headers))
      return redirect(f"/page/{cur_doc_id}/{cur_h1}")
    contents = filter(lambda content: content["h1"] == cur_h1 and content["h2"] == cur_h2 and content["h3"] == cur_h3, doc.contents)

    return render_template("index.html", cur_doc_id=cur_doc_id, cur_h1=cur_h1, contents=contents)

  @app.route("/signin", methods=["POST", "GET"])
  def signin():
    logger.debug("signin()")
    client = WebApplicationClient(oauth_credential["client_id"])
    authorization_endpoint = requests.get(GOOGLE_DISCOVERY_URL).json()["authorization_endpoint"]
    request_uri = client.prepare_request_uri(authorization_endpoint, redirect_uri=request.base_url + "/callback", scope=["openid", "email", "profile"],)
    logger.debug(request_uri)
    return redirect(request_uri)

  @app.route("/signin/callback")
  def callback():
    logger.debug("callback()")
    code = request.args.get("code")
    client = WebApplicationClient(oauth_credential["client_id"])

    token_endpoint = requests.get(GOOGLE_DISCOVERY_URL).json()["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(token_endpoint, authorization_response=request.url, redirect_url=request.base_url, code=code)
    token_response = requests.post(token_url, headers=headers, data=body, auth=(oauth_credential["client_id"], oauth_credential["client_secret"]))
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = requests.get(GOOGLE_DISCOVERY_URL).json()["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    uri = uri.replace("http:", "https:")

    userinfo_response = requests.get(uri, headers=headers, data=body).json()

    logger.debug(userinfo_response)
    member = Member(member_id=userinfo_response["email"].split('@')[0], en_name=userinfo_response["name"])

    login_user(member, remember=True)
    return redirect(url_for("index"))

  @app.route("/signout", methods=["POST", "GET"])
  def signout():
    logger.debug("signout()")
    logout_user()
    return redirect(url_for("index"))

  return app


if __name__ == "__main__":
  app = create_app()
  server = Server(app.wsgi_app)
  server.serve(debug=True)
