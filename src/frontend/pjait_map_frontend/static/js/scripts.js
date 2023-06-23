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



function deleteActivity(scheduleId) {
  // Send a DELETE request to the server to delete the schedule
  fetch(`/timetable/${scheduleId}`, {
    method: 'DELETE',
  })
  .then(response => {
    if (response.ok) {
      // Refresh the page after successful deletion
      location.reload();
    } else {
      // Handle error response
      console.error('Failed to delete schedule:', response.statusText);
    }
  })
  .catch(error => {
    // Handle network or other errors
    console.error('An error occurred while deleting the schedule:', error);
  });
}