function displayImage(imageURL) {
    const contentSection = document.querySelector(".map-image");
    contentSection.innerHTML = `<img src="${imageURL}" alt="Map Image">`;
}
