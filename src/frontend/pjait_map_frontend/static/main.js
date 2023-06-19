function displayImage(imageURL, location) {
  const contentSection = document.querySelector(".map-image");
  const pinImage = `<img src="${imageURL}" alt="Map Image">
                    <div class="pin" style="left: ${location.x}px; top: ${location.y}px;"></div>`;
  contentSection.innerHTML = pinImage;
}

