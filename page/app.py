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

  login_manager = LoginManager()
  login_manager.init_app(app)

  GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

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
  return app

  @app.route('/resume')
  def download_resume():
    return send_file("/resume.pdf", as_attachment=True)


if __name__ == "__main__":
  app = create_app()
  server = Server(app.wsgi_app)
  server.serve(debug=True)
