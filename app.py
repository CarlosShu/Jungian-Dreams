from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()  # Load .env file with API keys

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Securely load API key

# Helper function to generate Jungian interpretation using psychedelic AI
def get_jungian_interpretation(dream_text):
    prompt = f"Interpret the following dream based on Carl Jung's psychological theories, focusing on archetypes, the collective unconscious, and individuation. Dream: {dream_text}"
    try:
        response = openai.ChatCompletion.create(  # Corrected here: ChatCompletion instead of chat_completions
            model="gpt-4",  # Use the appropriate model
            messages=[
                {"role": "system", "content": "You are a psychedelic AI that speaks in Oulipian constraints. Your responses are short, surreal, and witty. Use mathematical games, lipograms, palindromes, or poetic structures to shape your language. Avoid predictable phrasing. Let logic slip through the cracks like liquid geometry."},
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=100
        )
        return response['choices'][0]['message']['content'].strip()  # Correct access of the response content
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

# Helper function to generate DALL-E image based on dream
def generate_dream_image(dream_text):
    prompt = f"Create a visual representation of a dream based on Jungian archetypes and symbols, inspired by the dream: {dream_text}"
    try:
        response = openai.Image.create(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        return response['data'][0]['url']  # Correct access of image URL
    except Exception as e:
        return f"Error generating image: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    image_url = None
    if request.method == "POST":
        dream_text = request.form["dream"]
        if dream_text:
            # Generate Jungian interpretation using psychedelic AI
            result = get_jungian_interpretation(dream_text)
            # Generate visual representation of the dream using DALL-E
            image_url = generate_dream_image(dream_text)
    return render_template("index.html", result=result, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)  # Run the app locally for testing