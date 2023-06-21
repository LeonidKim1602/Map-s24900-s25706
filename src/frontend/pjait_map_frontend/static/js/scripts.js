// static/scripts.js
function openPopup() {
document.getElementById("popup").style.display = "block";
}

function submitForm(event) {
	event.preventDefault(); // Prevent form submission

	// Get input values
	var start = document.getElementById("start").value;
	var end = document.getElementById("end").value;
	var room = document.getElementById("room").value;
	var subject = document.getElementById("subject").value;

	// Create JSON object
	var data = {
	start: start,
	end: end,
	room: room,
	subject: subject
	};

	// Send data as JSON (example: display in console)
	console.log(JSON.stringify(data));

	// Reset form and close popup
	document.getElementById("start").value = "";
	document.getElementById("end").value = "";
	document.getElementById("room").value = "";
	document.getElementById("subject").value = "";
	document.getElementById("popup").style.display = "none";
}

function closePopup() {
  const popup = document.getElementById("popup");
  popup.style.display = "none";
}

function addActivity(studentId) {
  openPopup("add");
  document.getElementById("day-id").value = dayId;
}

function editActivity() {
  // Fetch activity data using activityId and pass it to openPopup function
  // Then open the popup for editing
  const data = fetch(`http://127.0.0.1:8001/schedule/`, {
      method: "PUT",
    })
    .then((data) => {
      openPopup("edit", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function deleteActivity(studentId, scheduleId) {
  if (confirm("Are you sure you want to delete this class?")) {
    // Send delete request using activityId
    fetch(`http://127.0.0.1:8001/schedule/${studentId}/${scheduleId}`, {
      method: "DELETE",
    }).then(r => location.reload());
  }
}

