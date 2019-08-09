function handleMissingImage(id) {
  var image = document.getElementById(id);
  image.src = "https://ideai.upc.edu/en/shared/pap/default.png"
}
function showMoreSummary(id, summary) {
  var summary = document.getElementById("summary"+id)
  var full_summary = document.getElementById("fullsummary"+id)
  summary.hidden = true;
  full_summary.hidden = false;
}
function showLessSummary(id, summary) {
  var summary = document.getElementById("summary"+id)
  var full_summary = document.getElementById("fullsummary"+id)
  summary.hidden = false;
  full_summary.hidden = true;
}
