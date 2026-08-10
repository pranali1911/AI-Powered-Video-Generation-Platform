const button = document.getElementById("generateBtn");

// Add click event listener to the generate button
button.addEventListener("click", generateVideo);

// Function to generate video based on user input
async function generateVideo() {
    // Get user inputs
    const prompt = document.getElementById("prompt").value.trim();
    const aspectRatio = document.getElementById("aspectRatio").value;
    const duration = document.getElementById("duration").value;
    const style = document.getElementById("style").value;
    const negativePrompt = document.getElementById("negativePrompt").value.trim();

    const message = document.getElementById("message");
    const videoSection = document.getElementById("videoSection");

    // Validate prompt input
    if (!prompt) {
        message.innerHTML = "Please enter a video prompt.";
        return;
    }

    // Disable button while processing
    button.disabled = true;

    // Show loading state
    message.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <b>Generating your video...</b>
            <p>This may take a few minutes.</p>
        </div>
    `;

    // Clear previous result
    videoSection.innerHTML = "";

    // Construct request URL with query parameters
    const url =
        `/generate?prompt=${encodeURIComponent(prompt)}` +
        `&aspect_ratio=${encodeURIComponent(aspectRatio)}` +
        `&duration=${duration}` +
        `&style=${encodeURIComponent(style)}` +
        `&negative_prompt=${encodeURIComponent(negativePrompt)}`;

    try {
        // Send request to backend
        const response = await fetch(url, {
            method: "POST"
        });

        const data = await response.json();

        // Handle API errors
        if (data.error) {
            message.innerHTML = ` ${data.error}`;
            button.disabled = false;
            return;
        }

        // Success message
        message.innerHTML = " Video generated successfully!";

        // Display generated video
        videoSection.innerHTML = `
            <div class="result-card">
                <h2>Generated Video</h2>

                <video controls>
                    <source src="/${data.video}" type="video/mp4">
                </video>

                <a
                    href="/${data.video}"
                    download
                    class="download">
                    ⬇ Download Video
                </a>
            </div>
        `;

        // Refresh history section
        loadHistory();

    } catch (error) {
        // Handle connection errors
        message.innerHTML = " Unable to connect to server.";
    }

    // Re-enable button
    button.disabled = false;
}

async function loadHistory() {
    const historySection = document.getElementById("historySection");

    try {
        // Fetch generated video history
        const response = await fetch("/history");
        const data = await response.json();

        // Show empty state
        if (data.history.length === 0) {
            historySection.innerHTML = "<p>No videos yet.</p>";
            return;
        }

        // Clear existing history
        historySection.innerHTML = "";

        // Render history items
        data.history.forEach(item => {
            historySection.innerHTML += `
                <div class="history-card">
                    <video controls>
                        <source src="/${item.video}" type="video/mp4">
                    </video>
                    <p>${item.prompt}</p>
                    <small>${item.created_at}</small>
                </div>
            `;
        });

    } catch (error) {
        // Handle history loading errors
        historySection.innerHTML = "Unable to load history.";
    }
}

// Load history when page opens
loadHistory();