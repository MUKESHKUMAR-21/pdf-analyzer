import os
import json
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv  # type: ignore

# Load environment variables (mostly GEMINI_API_KEY)
load_dotenv()

def get_api_key():
    return os.getenv("GEMINI_API_KEY")

async def generate_questions(text_content: str, num_questions: int = 5, difficulty: str = "Medium"):
    """
    Use Gemini to generate study questions based on the provided text.
    Returns a structured format.
    """
    api_key = get_api_key()
    if not api_key or api_key == "your_google_gemini_api_key_here":
        raise ValueError("GEMINI_API_KEY is not set in the .env file. Please add your API key to backend/.env!")
        
    genai.configure(api_key=api_key)
        
    # Initialize the model (using 2.5-flash for speed and large context)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    truncated_content = text_content[:40000]  # type: ignore
    prompt = f"""
    You are an expert tutor and academic assistant. I am providing you with extracted text from a study material (PDF).
    Your task is to analyze the content, identify the general topic, and generate relevant, important study questions that will help a student master this material.
    
    Please structure your response AS A STRICT JSON OBJECT with the following format:
    {{
        "topic": "A brief, clear statement of the general topic or main subject of the document",
        "questions": [
            {{
                "type": "mcq",
                "question": "The multiple choice question text",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "answer": "The correct option exactly as written above"
            }},
            {{
                "type": "short",
                "question": "A short answer question text",
                "options": null,
                "answer": "A brief explanation of the expected answer"
            }}
        ]
    }}
    
    Generate exactly {num_questions} high-quality questions. Mix MCQ and short answer types. 
    The difficulty level should be {difficulty}. Adjust the complexity of the questions and options to match this specific difficulty level.
    Make sure they accurately reflect the provided text.
    Output ONLY valid JSON and nothing else. Do not use markdown blocks for the JSON (like ```json), just the plain JSON object.
    
    Study Material Content:
    {truncated_content}
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean up potential markdown formatting just in case the model ignores instructions
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        result_data = json.loads(response_text)
        return result_data
    except json.JSONDecodeError:
        print(f"Failed to parse JSON. Raw response: {response.text}")
        raise ValueError("The AI model returned an invalid format. Please try again.")
    except Exception as e:
        print(f"Error calling Gemini AI: {e}")
        raise ValueError(f"Failed to communicate with the AI model: {str(e)}")
