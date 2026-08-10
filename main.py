import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from database import create_database, save_history, get_history
from video import generate_video

load_dotenv()

app = FastAPI(title="AI Video Generator")

# Create videos directory if it doesn't exist
os.makedirs("videos", exist_ok=True)

# Mount static and generated video folders
app.mount("/static", StaticFiles(directory="frontend"), name="static")
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# Initialize database
create_database()

@app.get("/")
def home():
    return FileResponse("frontend/index.html")

# API endpoint to generate video based on user input
@app.post("/generate")
def generate(
    prompt: str,
    aspect_ratio: str = "16:9",
    duration: int = 5,
    style: str = "Cinematic",
    negative_prompt: str = ""
):
    # Validate prompt
    if not prompt.strip():
        return {"error": "Please enter a prompt."}

    # Available style presets
    styles = {
        "Cinematic": "cinematic lighting, cinematic camera movement, professional film look",
        "Anime": "anime style, detailed animation, vibrant colors",
        "Realistic": "photorealistic, natural lighting, realistic details",
        "3D": "high quality 3D animation, detailed 3D environment"
    }

    # Get selected style description
    style_prompt = styles.get(style, "")

    # Build final prompt
    final_prompt = f"""
    {prompt}.
    Style: {style_prompt}.
    Aspect ratio: {aspect_ratio}.
    Duration: {duration} seconds.
    """

    # Add negative prompt if provided
    if negative_prompt.strip():
        final_prompt += f"""
        Avoid: {negative_prompt}."""

    try:
        # Generate video
        print("Generating video...")
        print("Prompt:", final_prompt)

        video = generate_video(final_prompt)

        # Create unique video filename
        video_id = len(get_history()) + 1
        video_path = f"videos/video_{video_id}.mp4"

        # Save video file
        with open(video_path, "wb") as file:
            file.write(video)

        # Store generation history
        save_history(prompt, video_path)

        return {
            "message": "Video generated successfully",
            "video": video_path,
            "prompt": prompt
        }

    except Exception as error:
        print("Error:", error)

        return {
            "error": str(error)
        }

@app.get("/history")
def history():
    # Fetch all saved records
    records = get_history()

    result = []

    # Format history response
    for record in records:
        result.append({
            "id": record[0],
            "prompt": record[1],
            "video": record[2],
            "created_at": record[3]
        })

    return {
        "history": result
    }