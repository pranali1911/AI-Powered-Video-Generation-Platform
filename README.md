# 🎬 AI-Powered Video Generation Platform

Generate short AI videos from a simple text prompt — describe a scene, pick your options, and get a downloadable video in minutes.

> Example prompt: *"A luxury perfume bottle rotating on a black marble surface with golden lighting."*

---

## 📌 Objective

This project is a simple, full-stack web application that lets users type a text description and generate a short AI video from it. The platform handles the entire flow — taking the prompt, sending it to an AI video generation model, showing the result, and keeping a history of recent generations.

---

## ✨ Features

### Core Features
- **Prompt Input** — a clean text box where users describe the video they want, plus a **Generate** button to trigger creation.
- **AI Video Generation** — prompts are sent to an AI video generation model (via the **Fal AI** provider, using the `Wan-AI/Wan2.2-TI2V-5B` text-to-video model) to create the video.
- **Video Output Display** — the generated video is shown directly in the browser with playback controls, along with a **Download** button to save it locally.
- **History** — the app automatically stores and displays the **last 5 generated prompts and videos**, so users can revisit recent work without regenerating.
- **Error Handling** — the app shows clear, meaningful messages when:
  - the prompt field is left empty
  - the AI generation request fails
  - generation is taking too long

### Bonus Features
- **Multiple aspect ratios** — 16:9 (Landscape), 9:16 (Portrait), 1:1 (Square)
- **Video duration selection** — 5 seconds or 10 seconds
- **Style presets** — Cinematic 🎬, Realistic 📷, Anime 🎨, 3D 🧊
- **Negative prompts** — specify what to avoid (e.g. "blurry, low quality, distorted, watermark")
- **Progress/loading indicator** — animated spinner with status text while a video is being generated

> Not yet implemented: Login/Signup, and automatic prompt enhancement using an LLM. See [Roadmap](#-roadmap--ideas-for-improvement) below.

---

## 🧠 How It Works

1. The user opens the app and types a description of the video they want.
2. They choose optional settings — aspect ratio, duration, style, and negative prompt.
3. On clicking **Generate Video**, the frontend sends all this data to the backend server.
4. The backend combines the inputs into one detailed prompt and sends it to the AI video model through the Fal AI / Hugging Face Inference API.
5. Once the model returns the video, the backend saves it to disk and records the prompt + video path in the database.
6. The video is sent back to the browser and displayed, and the **Recent Videos** history is refreshed to include the new entry.

In short: **your prompt → backend → AI model → generated video → shown & saved.**

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + **FastAPI** |
| Frontend | HTML, CSS, JavaScript |
| Database | **SQLite** (lightweight, file-based) |
| AI Video Model | Hugging Face Inference API — `Wan-AI/Wan2.2-TI2V-5B` (via Fal AI provider) |
| Communication | REST APIs |
| Version Control | Git / GitHub |

---

## 📁 Project Structure

```
ai-video-generator/
│
├── frontend/
│   ├── index.html         # Prompt form, options, video display, history sidebar
│   ├── style.css           # Visual styling (glassmorphism dark theme)
│   └── script.js             # Handles form submission, API calls, rendering results
│
├── main.py                     # FastAPI app — routes and request handling
├── database.py                   # SQLite setup, saving & fetching history
├── video.py                        # Connects to the AI model and generates video
│
├── videos/                            # Generated .mp4 files are stored here
├── history.db                           # SQLite database (auto-created on first run)
├── .env                                    # Holds your API token (not committed to Git)
└── README.md                                # This file
```

---

## ✅ Requirements

- Python 3.9 or newer
- A Hugging Face account and API token ([huggingface.co](https://huggingface.co) → Settings → Access Tokens)
- pip for installing dependencies

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/ai-video-generator.git
cd ai-video-generator
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn python-dotenv huggingface_hub
```

### 4. Configure environment variables
Create a `.env` file in the project root:
```
HF_TOKEN=your_huggingface_token_here
```

### 5. Run the server
```bash
uvicorn main:app --reload
```

### 6. Open the app
Visit **http://127.0.0.1:8000** in your browser, enter a prompt, choose your options, and click **Generate Video**.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the main web page |
| `POST` | `/generate` | Generates a video from a prompt and options |
| `GET` | `/history` | Returns the last 5 generated videos |

**Example — Generate a video:**
```
POST /generate?prompt=a dragon flying over mountains&aspect_ratio=16:9&duration=5&style=Cinematic&negative_prompt=blurry
```

**Example response:**
```json
{
  "message": "Video generated successfully",
  "video": "videos/video_1.mp4",
  "prompt": "a dragon flying over mountains"
}
```

**Example error response (empty prompt):**
```json
{
  "error": "Please enter a prompt."
}
```

---

## ⚠️ Error Handling

| Scenario | Behavior |
|---|---|
| Empty prompt | Frontend blocks submission and shows "Please enter a video prompt." Backend also validates and rejects empty prompts. |
| AI generation fails | The error message from the model/API is caught and shown to the user instead of crashing the app. |
| Generation takes too long | A loading spinner with "This may take a few minutes" is shown while waiting. |

---

## 🗺️ Roadmap / Ideas for Improvement

- [ ] Add request timeout handling so users get a clear message if generation hangs
- [ ] Actually pass aspect ratio & duration as structured parameters to the model (currently embedded as text in the prompt)
- [ ] Add basic Login/Signup so history is per-user instead of global
- [ ] Use an LLM to automatically enhance short prompts into more detailed ones before generation
- [ ] Move from SQLite to MongoDB/PostgreSQL for multi-user, production use
- [ ] Migrate frontend to React/Next.js for a more scalable UI

---

## 🖼️ Screenshots

<img width="1918" height="968" alt="image" src="https://github.com/user-attachments/assets/e181ce99-022b-4790-a064-51d7c6bed5f1" />


## 🤝 Contributing

1. Fork this repository
2. Create a new branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m "Add some feature"`
4. Push: `git push origin feature-name`
5. Open a Pull Request

---

## 📄 License

This project is open source — feel free to use, modify, and share it. *(Add your preferred license, e.g. MIT.)*

---

**Built as part of an AI Video Generation Platform assignment. Enjoy creating! 🎥✨**
