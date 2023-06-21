function displayImage(imageURL, locX, locY) {
  const contentSection = document.querySelector(".map-image");

  const image = `<img src="${imageURL}" alt="Map Image" id="img">`;
  contentSection.innerHTML = image;

  const element = document.getElementById("map-image");
  const rect = element.getBoundingClientRect();
  const offsetX = rect.left;
  const offsetY = rect.top;
  const pin = `<div class="pin" style="left: ${offsetX + locX}px; top: ${offsetY + locY}px;"></div>`;
  contentSection.innerHTML += pin;
}
