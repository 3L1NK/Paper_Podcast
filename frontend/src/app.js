const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fileInput");
const audioContainer = document.getElementById("audioContainer");
const audioPlayer = document.getElementById("audioPlayer");
const downloadLink = document.getElementById("downloadLink");
const themeToggle = document.getElementById("themeToggle");
const ttsSelect = document.getElementById("ttsService");

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

// Upload file to the backend
async function uploadFile(file) {
    dropzone.innerHTML = "<p>Processing your file... Please wait.</p>";

    const formData = new FormData();
    formData.append("file", file);

    const ttsService = ttsSelect.value;
    formData.append("tts_service", ttsService);

    try {
        const response = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();
        console.log("Backend Response:", data);

        if (!data.audio_url) {
            throw new Error("Audio URL not returned by backend.");
        }

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

// File input event listeners
dropzone.addEventListener("click", () => fileInput.click());
fileInput.addEventListener("change", () => {
    const file = fileInput.files[0];
    if (file) {
        uploadFile(file);
    }
});
