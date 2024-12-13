// Select DOM elements
const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const audioContainer = document.getElementById("audioContainer");
const audioPlayer = document.getElementById("audioPlayer");
const downloadLink = document.getElementById("downloadLink");
const themeToggle = document.getElementById("themeToggle");

// Load theme preference from local storage
const savedTheme = localStorage.getItem("theme");
if (savedTheme) {
  document.documentElement.classList.add(savedTheme);
}

// Toggle theme on button click
themeToggle.addEventListener("click", () => {
  const isDarkMode = document.documentElement.classList.toggle("dark");
  localStorage.setItem("theme", isDarkMode ? "dark" : "light");
});

// Handle drag-and-drop file upload
dropzone.addEventListener("click", () => fileInput.click());

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("border-blue-400");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("border-blue-400");
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("border-blue-400");
  const file = e.dataTransfer.files[0];
  if (file) {
    uploadFile(file);
  }
});

fileInput.addEventListener("change", () => {
  const file = fileInput.files[0];
  if (file) {
    uploadFile(file);
  }
});

// Upload file to the backend
async function uploadFile(file) {
  // Show loading state
  dropzone.innerHTML = "<p class='text-gray-600'>Processing your file... Please wait.</p>";

  const formData = new FormData();
  formData.append("file", file);

  try {
    // Send file to the backend
    const response = await fetch("http://localhost:8000/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to process the file. Please try again.");
    }

    const data = await response.json();

    // Display the audio player with the processed podcast
    showAudio(data.audio_url);
  } catch (error) {
    dropzone.innerHTML = `<p class='text-red-500'>Error: ${error.message}</p>`;
  }
}

// Display the audio and download link
function showAudio(audioUrl) {
  dropzone.classList.add("hidden");
  audioContainer.classList.remove("hidden");

  audioPlayer.src = audioUrl;
  downloadLink.href = audioUrl;
}
