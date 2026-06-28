import json
from groq import Groq

# Function to detect bugs in python code using Groq API.
def detect_bugs(code: str, api_key: str) -> list:
    """
    Analyzes python code for bugs using Groq and returns a list of detected bugs.
    
    Parameters:
        code (str): The Python code content to analyze.
        api_key (str): The Groq API key to authenticate requests.
        
    Returns:
        list: A list of dicts with keys line_number, bug_type, description, and severity.
    """
    print("[DEBUG] Initializing Groq client...")
    try:
        client = Groq(api_key=api_key)
        
        system_prompt = "You are a senior Python code reviewer."
        
        user_message = (
            "Review this Python code and return ONLY a \n"
            "valid JSON array. No explanation. No markdown.\n"
            "Each item must have exactly these keys:\n"
            "line_number, bug_type, description, severity\n"
            "Severity must be: high, medium, or low\n\n"
            f"{code}"
        )
        
        print("[DEBUG] Sending request to Groq (model: llama-3.1-8b-instant)...")
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        
        print("[DEBUG] Response received. Extracting text content...")
        response_text = response.choices[0].message.content.strip()
        
        print("[DEBUG] Cleaning markdown code block tags if present...")
        cleaned_text = response_text
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:].strip()
            if cleaned_text.lower().startswith("json"):
                cleaned_text = cleaned_text[4:].strip()
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3].strip()
            
        print("[DEBUG] Parsing clean JSON content...")
        parsed_list = json.loads(cleaned_text)
        
        print("[DEBUG] Successfully parsed code review results.")
        return parsed_list
        
    except Exception as e:
        print(f"[DEBUG] Error occurred during bug detection: {e}")
        return []
