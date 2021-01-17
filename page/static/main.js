function toggle(gist_id, file_id) {
  console.log(gist_id);
  console.log(file_id);
  document.querySelectorAll(`.file.${gist_id}`).forEach(function (el) {
    el.style.display = "none";
  })
  document.querySelectorAll(".gist-toggle").forEach(function (el) {
    el.classList.remove("current");
  })
  document.querySelector(`a.gist-toggle#${file_id}`).classList.add("current");
  document.querySelector(`div.${gist_id}#${file_id}`).style.display = "block";
}