/* Now we can play the games on any sized device and full screen on a tv. */

function setZoom() {
  var scale = window.innerWidth / 560;

  const vscale = window.innerHeight/ 420;
  if (vscale < scale) {
    scale = vscale;
  }

  document.body.style.zoom = scale;
  document.body.style.display = "flex";
}

function setStatus(text) {
  document.getElementsByClassName("footerstatus")[0].textContent = text;
}

window.addEventListener('load',setZoom);
window.addEventListener('resize', setZoom);
