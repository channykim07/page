from ..common import logger, categories
from collections import defaultdict
from functools import lru_cache
from itertools import islice


class Team:
  def __init__(self, team_id="", admin_ids=None, member_ids=None):
    self.team_id = team_id
    self.admin_ids = admin_ids or []
    self.member_ids = member_ids or []

  @staticmethod
  @lru_cache
  def show_progress(team_id):
    from ..database import local_db, remote_db
    member_ids = remote_db.get("team", team_id).member_ids
    members = remote_db.get("member", member_ids)
    members.sort(key=lambda member: len(member.solved_problem_ids))
    html = '<div id="search-problem" onchange=toggle_visibility()>'
    html += 'bj_range=<input type="number" class="min_bj_level" value="1">~<input type="number" class="max_bj_level" value="10"><br>'

    for i, member in enumerate(reversed(members)):
      html += f'<input id="{member.id}" class="show_member_id" type="checkbox">{member.kr_name} {len(member.solved_problem_ids)} {member.baekjoon_id}</input><br>'
      member.solved_problem_ids = set(member.solved_problem_ids)

    problems = local_db.get_all("problem")
    problems = problems.values()
    cate2problems = defaultdict(list)
    for problem in problems:    # cache headers to problem for effeciency
      if problem.solution_link != "" and problem.problem_id.startswith("BJ"):
        cate2problems[f"{problem.category_id}"].append(problem)
    for category in categories:
      html += f"<h1>{category}</h1>"
      for problem in sorted(cate2problems[f"{category}"], key=lambda problem: problem.level):
        html += f'<table style="table-layout:fixed;">'
        html += f"<tr id='{problem.level}' class='bj_level'>"
        html += f"<td style='width:400px;'>{problem.link}</td>"
        html += f"<td style='width:70px;'>{problem.solution_link}</td>"
        html += " ".join([f"<td> <span id={member.id} class='{'' if problem.problem_id in member.solved_problem_ids else 'member_id'}' style='display:none;'>{member.kr_name}</span></td>" for member in members])
        html += f"</tr>"
      html += f"</table>"
    html += "</div>"
    return html
