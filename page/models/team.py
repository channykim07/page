from ..common import logger
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
    headers = local_db.get("doc", "Python").headers
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
    h2problems = defaultdict(list)
    for problem in problems:    # cache headers to problem for effeciency
      if problem.gist_id != "" and problem.problem_id.startswith("BJ"):
        gist = local_db.get("gist", problem.gist_id)
        h2problems[f"{gist.h1}{gist.h2}{gist.h3}{gist.li}"].append(problem)
    print(h2problems)
    for h1 in headers:
      html += f"<h1>{h1}</h1>"
      for h2 in headers[h1]:
        html += f"<h2>{h2}</h2>"
        for h3 in headers[h1][h2]:
          html += f"<h3>{h3}</h3>"
          for li in headers[h1][h2][h3]:
            html += f'<li>{li}</li><table style="table-layout:fixed;">'
            for problem in sorted(h2problems[f"{h1}{h2}{h3}{li}"], key=lambda problem: problem.level):
              html += f"<tr id='{problem.level}' class='bj_level'>"
              html += f"<td style='width:300px;'>{problem.link}</td>"
              html += f"<td style='width:300px;'>{local_db.get('gist', problem.gist_id).link}</td>"
              html += " ".join([f"<td> <span id={member.id} class='{'' if problem.problem_id in member.solved_problem_ids else 'member_id'}' style='display:none;'>{member.kr_name}</span></td>" for member in members])
              html += f"</tr>"
            html += f"</table>"
    html += "</div>"
    return html
