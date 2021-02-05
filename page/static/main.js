'use strict';

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

document.addEventListener('DOMContentLoaded', toggle_visibility, false);
