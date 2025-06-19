// script.js
const dropArea = document.querySelector(".drag-area");
const fileInput = document.querySelector("#fileInput");
const previewImage = document.querySelector("#preview");

dropArea.addEventListener("click", () => fileInput.click());

dropArea.addEventListener("dragover", e => {
  e.preventDefault();
  dropArea.classList.add("dragover");
});

dropArea.addEventListener("dragleave", () => {
  dropArea.classList.remove("dragover");
});

dropArea.addEventListener("drop", e => {
  e.preventDefault();
  dropArea.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  fileInput.files = e.dataTransfer.files;
  preview(file);
});

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  preview(file);
});

function preview(file) {
  if (file && file.type.startsWith("image/")) {
    const reader = new FileReader();
    reader.onload = () => {
      previewImage.src = reader.result;
      previewImage.style.display = "block";
    };
    reader.readAsDataURL(file);
  } else {
    previewImage.style.display = "none";
  }
}
