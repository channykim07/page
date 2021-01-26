'use strict';

const app = document.querySelector('.side-content');
const client = algoliasearch("36HZ0DWIJ7", "a487cc220850ce1901b5e60aa51e9aaf");
const index = client.initIndex("page")

var toggle = (gist_id, file_id) => {
  document.querySelectorAll(`.gist-toggler.${gist_id}`).forEach((el) => {
    el.classList.remove("current");
  })
  document.querySelector(`a.gist-toggler#${file_id}`).classList.add("current");
  update_gist();
}

var update_gist = () => {
  document.querySelectorAll(".gist-file").forEach(gist => {
    gist.querySelectorAll('.file').forEach(file => {
      if (gist.querySelector(`.gist-toggler.${file.classList[1]}#${file.id}`).classList.length == 3) {
        file.style.display = "inline"
      }
      else {
        file.style.display = "none"
      }
    })
  })
}

var search = () => {
  var search_word = document.querySelector(`#search-input`).value
  if (search_word.length == 0) {
    default_headers();
  }
  else {
    var cur_doc_id = window.location.pathname.split("/")[2]
    index.search(search_word, { filters: `doc_id:${cur_doc_id}` }).then(result => {
      var hits = result.hits;
      var visible_ids = hits.map(hit => hit.objectID.split('-').slice(0, -1).join('-'));
      document.querySelectorAll("a.side-item").forEach(dom => {
        if (visible_ids.includes(dom.id)) {
          dom.style.display = "block"
        } else {
          dom.style.display = "none"
        }
      })
    })
  }
}

var default_headers = () => {
  // highlight current left menu
  var cur_section = window.location.pathname.split("/").slice(2).join("-")
  if (cur_section.split("-").length == 3) {
    cur_section += "-"
  }
  console.log(cur_section);
  document.querySelector(`[id='${cur_section}']`).classList.add("current"); // [id=''] for h2 with space

  document.querySelectorAll("a.side-item").forEach(dom => {
    dom.style.display = 'block'
  })
}

var default_gist = () => {
  var domain2exts = {
    "Python": ["py"],
    "Javascript": ["js"],
    "Java": ["java"],
    "C++": ["cpp"]
  }
  var current_exts = domain2exts[window.location.pathname.split("/")[2]];

  document.querySelectorAll(".gist-file").forEach(gist => {
    var focus_i = 0;
    gist.querySelectorAll(".gist-toggler").forEach((dom, i) => {
      for (var current_ext of current_exts) {
        if (dom.id.endsWith(current_ext)) {
          focus_i = i;
        }
      }
    })
    gist.querySelectorAll(".gist-toggler")[focus_i].classList.add("current");
  })
  update_gist();
}


function toggle_visibility() {
  document.querySelectorAll(".member_id").forEach(e => {
    e.style.display = $(`.show_member_id#${e.id}`)[0].checked ? 'inline-block' : 'none';
  })
  var total = 0;
  document.querySelectorAll(".show_member_id").forEach(e => {
    if (e.checked) {
      total += 1;
    }
  })
  document.querySelectorAll(".bj_level").forEach(e => {
    var visible = 0;
    e.querySelectorAll(".member_id").forEach(e => {
      if (e.style.display == "inline-block") {
        visible++;
      }
    })
    if (total == visible) {
      e.style.backgroundColor = 'yellow'
    }
    else {
      e.style.backgroundColor = 'white'
    }
  })

  const min_level = parseFloat(document.querySelector(".min_bj_level").value);
  const max_level = parseFloat(document.querySelector(".max_bj_level").value);
  document.querySelectorAll(".bj_level").forEach(e => {
    e.style.display = (min_level <= parseFloat(e.id) && parseFloat(e.id) <= max_level ? 'line-block' : 'none')
  })

}

if (window.location.href.includes("/admin/")) {
  document.addEventListener('DOMContentLoaded', toggle_visibility, false);
}
else {
  document.addEventListener('DOMContentLoaded', default_headers, false);
}
document.addEventListener('DOMContentLoaded', default_gist, false);
