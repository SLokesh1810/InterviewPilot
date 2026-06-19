import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load API key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not set in .env")

# Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
WORKING_MODEL = "gemini-2.5-flash-lite"

def llm_generation(prompt, temperature=0.5, max_output_tokens=150, top_p=0.8, top_k=40):
    """
    Helper function to generate content using the Gemini model.
    """
    try:
        model = genai.GenerativeModel(WORKING_MODEL)

        response = model.generate_content(
            [prompt],
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_p=top_p,
                top_k=top_k
            )
        )
    
    except Exception as e:
        print(f"Error initializing the model: {e}")
        return ""

    return response.output_text.strip()
