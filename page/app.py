import requests
import json

from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient

from .user import User
from .common import PATH, get_logger, get_oauth_credential
from .api.student import enroll_class, get_students
from .api.doc import get_header, get_post
from .api.gist import display_gist
from .api.problem import display_problem, get_problems

from livereload import Server

app = Flask(__name__)
app.jinja_env.globals.update(display_gist=display_gist)  # use python function inside jinja
app.jinja_env.globals.update(display_problem=display_problem)


@app.route("/", methods=["GET"])
def index():
  h0, h1, h2, h3 = "Python", "Syntax", "IO", "Print"
  posts = get_post(h0, h1, h2, h3)

  return render_template("index.html", headers=get_header(), h0=h0, h1=h1, posts=posts, debug=True)


@app.route("/signin", methods=["GET"])
def signin():
  headers = get_header()["Python"]
  html = ""
  students = get_students("prake")
  for student in students:
    student["solved"] = set(student["solved"])

  for h1 in ["Syntax", "Algorithm"]:
    html += f"<h1>{h1}</h1>"
    for h2 in headers[h1]:
      html += f"<h2>{h2}</h2>"
      for h3 in headers[h1][h2]:
        html += f"<h3>{h3}</h3>"
        for problem in get_problems(h1, h2, h3):
          problem["unsolved_by"] = []
          for student in studeets:
            if "kr_name" in student and problem.get("id", "") not in student["solved"]:
              problem["unsolved_by"].append(student["kr_name"])
          html += display_problem(problem)

  return render_template("admin.html", progress_overview_html=html)


server = Server(app.wsgi_app)
server.serve(debug=True)
