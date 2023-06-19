document.addEventListener("DOMContentLoaded", function() {
  // Retrieve the subject list from the backend API
  fetch("/api/subjects")
    .then(response => response.json())
    .then(subjects => {
      const subjectList = document.getElementById("subject-list");
      subjects.forEach(subject => {
        const listItem = document.createElement("li");
        listItem.textContent = subject.name;
        listItem.addEventListener("click", () => {
          // Fetch and display the image corresponding to the selected subject
          fetch(`/api/subject/${subject.id}/file`)
            .then(response => response.blob())
            .then(blob => {
              const imageURL = URL.createObjectURL(blob);
              displayImage(imageURL);
            });
        });
        subjectList.appendChild(listItem);
      });
    })
    .catch(error => console.error("Error fetching subjects:", error));

  // Function to display the image in the content section
  function displayImage(imageURL) {
    const contentSection = document.querySelector(".content");
    contentSection.innerHTML = `<img src="${imageURL}" alt="Map Image">`;
  }
});

