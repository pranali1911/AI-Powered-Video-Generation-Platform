import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is missing in .env")

client = InferenceClient(
    provider="fal-ai",
    api_key=HF_TOKEN
)

MODEL = "Wan-AI/Wan2.2-TI2V-5B"


def generate_video(prompt):
    print("Starting video generation...")

    video = client.text_to_video(
        prompt=prompt,
        model=MODEL
    )

    print("Video generated successfully.")

    return video