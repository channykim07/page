import requests
import json
import os
import re

from itertools import islice

from bs4 import BeautifulSoup
from .models.gist import Gist
from .models.team import Team
from .models.member import Member
from .common import PATH, logger, oauth_credential, git_credential
from .database import remote_db, local_db
from collections import defaultdict
from livereload import Server
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient


def create_app():
  app = Flask(__name__)
  app.secret_key = "page"
  app.config["DEBUG"] = True

  def display_p(p):
    if "# " in p:
      left, right = p.rsplit("#", 1)
      return f'<span class="left">{left}</span><span class="right"># {right}</span>'
    elif p.startswith("> "):
      return f"<blockquote>{p[2:]}</blockquote>"
    else:
      return p

  def display_gist(gist_id):
    result = requests.get(f'https://gist.github.com/{gist_id}.js', headers=git_credential)

    # update with regex
    result = result.text.replace("\\n", "\n")  # .replace("[NEW_LINE]", "\\n").replace("  ", u'\xa0').replace("<pre>")
    result = re.sub(r"\\(/|&|\$|<|`|\"|\\|')", r"\1", result)
    result = result.replace("<tr", "<pre><tr").replace("</tr>", "</tr></pre>")
    result = result.split("document.write('")[-1][:-3]

    bs = BeautifulSoup(result, "html.parser")

    for tag in bs.find_all(class_="gist"):
      file_box = tag.find(class_="file-box")
      root = tag.find(class_="file-box")
      toggle_div = bs.new_tag('div', attrs={"class": "gist-meta"})

      for i, d in enumerate(tag.find_all(class_="file")):
        d["class"] = f"file gist-id-{gist_id}"
        if i != 0:
          file_box.append(d)  # combine to first table

      for d in tag.find_all(class_="gist-meta"):
        siblings = list(d.next_elements)
        file_id, file_name = siblings[4].attrs["href"].split("#")[-1], siblings[5]
        toggle_a = bs.new_tag('a', attrs={"id": file_id, "class": f"gist-toggler gist-id-{gist_id}", "onclick": f"toggle('gist-id-{gist_id}', '{file_id}')", "style": "padding: 0 18px"})
        toggle_a.append(file_name)
        toggle_div.append(toggle_a)
        d.extract()  # remove bottom nav
      edit_gist = bs.new_tag('a', attrs={"class": f"edit-gist", "href": f"https://gist.github.com/{gist_id}", "style": "float: right"})
      edit_gist.append("edit")
      toggle_div.append(edit_gist)

      root.insert(0, toggle_div)
      for d in islice(tag.find_all(class_="gist-file"), 1, None):
        d.extract()  # remove except first
    return str(bs)

    gist = local_db.get("gist", gist_id)
    if current_user.is_anonymous:
      return "<p> You must log in to see content of gist </p> <br>"
    elif current_user.team_id == "":
      if gist.problem_id:
        return "<p> Must be premium member to see problem </p> <br>"
      else:
        return gist.html
    elif current_user.is_admin:
      return gist.html
    else:
      if gist.problem_id not in current_user.solved_problem_ids:
        return f"<p> Must solve {gist.problem_id} to view answer</p> <br>"
      else:
        return gist.html

  app.jinja_env.globals.update(display_p=display_p)
  app.jinja_env.globals.update(display_gist=display_gist)

  login_manager = LoginManager()
  login_manager.init_app(app)

  GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

  @app.route("/practice", methods=["GET"])
  def practice():
    return render_template("practice.html")

  @app.context_processor
  def inject_global():
    logger.debug("inject_global")
    headers = {doc.doc_id: doc.headers for doc in local_db.get_all("doc").values()}
    return dict(headers=headers)

  @login_manager.user_loader
  def load_user(user_id):
    return remote_db.get("member", user_id)

  @app.route("/admin/<string:team_id>", methods=["POST", "GET"])
  def admin(team_id):
    return render_template("admin.html", progress_overview_html=Team.show_progress(team_id))

  @app.route("/premium", methods=["POST", "GET"])
  def premium():
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

  @app.route("/login/<string:id>")
  def login(id):
    logger.debug(f"login")
    if id != "sofialee7979" or id != "channykim1030":
      return redirect(url_for("index"))

    member = remote_db.get("member", id)
    login_user(member, remember=True)
    return redirect(url_for("index"))

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
    member = remote_db.get("member", userinfo_response["email"].split('@')[0])

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
