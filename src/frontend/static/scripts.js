// static/scripts.js
function openPopup(action, data) {
  const popup = document.getElementById("popup");
  const popupTitle = document.getElementById("popup-title");
  const popupForm = document.getElementById("popup-form");

  if (action === "add") {
    popupTitle.textContent = "Add Activity";
    popupForm.setAttribute("action", "/add_activity");
  } else if (action === "edit") {
    popupTitle.textContent = "Edit Activity";
    popupForm.setAttribute("action", "/edit_activity");
  }

  // Set values in form fields for editing
  if (data) {
    document.getElementById("activity-id").value = data.id;
    document.getElementById("activity-name").value = data.name;
  } else {
    // Reset form fields for adding
    popupForm.reset();
  }

  popup.style.display = "block";
}

function closePopup() {
  const popup = document.getElementById("popup");
  popup.style.display = "none";
}

function addActivity(dayId) {
  openPopup("add");
  document.getElementById("day-id").value = dayId;
}

function editActivity(activityId) {
  // Fetch activity data using activityId and pass it to openPopup function
  // Then open the popup for editing
  const data = fetch(`/get_activity/${activityId}`)
    .then((response) => response.json())
    .then((data) => {
      openPopup("edit", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

function deleteActivity(activityId) {
  if (confirm("Are you sure you want to delete this activity?")) {
    // Send delete request using activityId
    fetch(`/delete_activity/${activityId}`, {
      method: "DELETE",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        // Refresh the page or remove the deleted activity from the DOM
        location.reload();
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}

