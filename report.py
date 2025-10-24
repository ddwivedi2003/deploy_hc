import easyocr
import requests
import ss

API_KEY = ss.k
ENDPOINT = ss.ep

try:
    reader = easyocr.Reader(['en']) 
except Exception as e:
    print(f"Error initializing EasyOCR: {e}")
    reader = None

def analyze_report(uploaded_file):
    """
    Analyzes a medical report by extracting text with EasyOCR 
    and sending it to Azure GPT-4.
    """
    if reader is None:
        return None, "EasyOCR model failed to load."

    try:
        image_bytes = uploaded_file.read()
        results = reader.readtext(image_bytes, detail=0, paragraph=True)
        extracted_text = "\n".join(results)


        if not extracted_text.strip():
            return None, "No text could be extracted from the image."
        headers = {
            "Content-Type": "application/json",
            "api-key": API_KEY,
        }

        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps people analyze medical reports."
                },
                {
                    "role": "user",
                    "content": f"Diagnose the report:\n\n{extracted_text}"
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }

        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()

        if "choices" in response_data:
            diagnosis = response_data['choices'][0]['message']['content']
            return diagnosis, None
        else:
            return None, "No valid response from GPT-4."

    except Exception as e:
        if "Invalid" in str(e) or "PIL" in str(e):
             return None, "Failed to process: The file is not a valid image."
        return None, f"Failed to process the image or request. Error: {str(e)}"
