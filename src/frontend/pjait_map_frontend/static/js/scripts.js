// static/scripts.js
function openPopup() {
document.getElementById("popup").style.display = "block";
}


function closePopup() {
  const popup = document.getElementById("popup");
  popup.style.display = "none";
}

function addActivity(dayId) {
  openPopup("add");
  document.getElementById("weekday").value = dayId;
}


function deleteActivity(studentId, scheduleId) {
  if (confirm("Are you sure you want to delete this class?")) {

  }
}

