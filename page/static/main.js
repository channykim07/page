function toggle(id){
  document.querySelectorAll(".file").forEach(function(el) {
    el.style.display="none";
  })
  document.querySelectorAll(".gist-toggle").forEach(function(el) {
    el.classList.remove("current");
  })
  document.querySelector(`a#${id}`).classList.add("current");
  document.querySelector(`div#${id}`).style.display = "block";
}