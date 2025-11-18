"""
AI Service - LM Studio Integration
File: utils/ai_service.py
Author: Dominik Szewczyk
"""

import requests
import json

# LM Studio Configuration
LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

def generate_medicine_info(medicine_name):
    """
    Use LM Studio AI to generate medicine information
    
    Args:
        medicine_name (str): Name of the medicine to research
        
    Returns:
        dict: Medicine information or None if failed
    """
    
    # Create simple, clear prompt for AI
    prompt = f"""You are helping someone who just bought {medicine_name} from a pharmacy and wants to understand it better.

Write information that a 16-year-old can easily understand. Use simple words, short sentences, and be very clear.

IMPORTANT FORMAT RULES:
- For "advice" and "warning": Write as plain text with each bullet point on a NEW LINE
- Use • at the start of each point
- Put a line break after each bullet point

Respond ONLY with this JSON format (no extra text):
{{
    "name": "{medicine_name.title()}",
    "description": "Write about 50 words (3-4 sentences) explaining: What is this medicine? What conditions does it treat? How does it work in the body? Keep language simple and friendly.",
    "advice": "• First piece of advice here\\n• Second piece of advice here\\n• Third piece of advice here\\n• Fourth piece of advice here",
    "warning": "• First warning here\\n• Second warning here\\n• Third warning here\\n• Fourth warning here",
    "pubmed_link": "https://pubmed.ncbi.nlm.nih.gov/?term={medicine_name.replace(' ', '+')}"
}}

EXAMPLE of correct format:
"advice": "• Take with a full glass of water\\n• Take at the same time each day\\n• Don't skip doses\\n• Finish the full course"

Each bullet point should be one clear, short sentence. Focus on the most important practical information."""

    try:
        print(f"🤖 Calling LM Studio for: {medicine_name}")
        
        # Call LM Studio API
        response = requests.post(
            LM_STUDIO_URL,
            json={
                "model": "local-model",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful pharmacy assistant. Explain medicines in very simple terms that a 16-year-old can understand. Use short sentences, simple words, and bullet points. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 1000,
            },
            timeout=180
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data['choices'][0]['message']['content']
            
            print(f"📥 AI Response received (length: {len(ai_response)} chars)")
            
            # Parse JSON from response
            medicine_info = parse_medicine_json(ai_response)
            
            if medicine_info:
                print(f"✅ Successfully parsed medicine info")
                print(f"📦 Type: {type(medicine_info)}")
                print(f"📝 Keys: {list(medicine_info.keys())}")
                print(f"🏥 Name: {medicine_info.get('name')}")
                return medicine_info
            else:
                print("❌ Failed to parse AI response as JSON")
                return None
        else:
            print(f"❌ LM Studio API error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to LM Studio. Make sure it's running on http://localhost:1234")
        return None
    except requests.exceptions.Timeout:
        print("❌ Error: LM Studio request timed out")
        return None
    except Exception as e:
        print(f"❌ Error calling LM Studio: {str(e)}")
        return None


def parse_medicine_json(ai_response):
    """
    Parse JSON from AI response (handles markdown code blocks)
    
    Args:
        ai_response (str): Raw response from AI
        
    Returns:
        dict: Parsed medicine info or None
    """
    try:
        # Remove markdown code blocks if present
        cleaned = ai_response.strip()
        
        # Remove ```json and ``` if present
        if cleaned.startswith('```json'):
            cleaned = cleaned[7:]
        elif cleaned.startswith('```'):
            cleaned = cleaned[3:]
            
        if cleaned.endswith('```'):
            cleaned = cleaned[:-3]
        
        cleaned = cleaned.strip()
        
        print(f"🧹 Cleaned response (first 200 chars): {cleaned[:200]}...")
        
        # Parse JSON
        medicine_info = json.loads(cleaned)
        
        # Validate required fields
        required_fields = ['name', 'description', 'advice', 'warning', 'pubmed_link']
        missing_fields = [f for f in required_fields if f not in medicine_info]
        
        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return None
        
        # Convert arrays to text with line breaks if needed
        if isinstance(medicine_info['advice'], list):
            medicine_info['advice'] = '\n'.join(medicine_info['advice'])
        
        if isinstance(medicine_info['warning'], list):
            medicine_info['warning'] = '\n'.join(medicine_info['warning'])
        
        # Clean up quotes and brackets
        medicine_info['advice'] = medicine_info['advice'].replace("['", "").replace("']", "").replace("', '", "\n")
        medicine_info['warning'] = medicine_info['warning'].replace("['", "").replace("']", "").replace("', '", "\n")
        
        print(f"✅ Parsed successfully! Type: {type(medicine_info)}")
        return medicine_info
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}")
        print(f"Raw AI response: {ai_response[:500]}...")
        return None
    except Exception as e:
        print(f"❌ Unexpected error in parse_medicine_json: {e}")
        return None


def test_lm_studio_connection():
    """
    Test if LM Studio is running and accessible
    
    Returns:
        bool: True if LM Studio is accessible
    """
    try:
        response = requests.post(
            LM_STUDIO_URL,
            json={
                "model": "local-model",
                "messages": [
                    {"role": "user", "content": "Hello"}
                ],
                "max_tokens": 10
            },
            timeout=5
        )
        return response.status_code == 200
    except:
        return False


# For testing purposes
if __name__ == "__main__":
    print("🧪 Testing LM Studio connection...")
    if test_lm_studio_connection():
        print("✓ LM Studio is running!")
        
        print("\n🧪 Testing medicine info generation...")
        result = generate_medicine_info("aspirin")
        
        if result:
            print("\n✅ Successfully generated medicine info:")
            print(f"Type: {type(result)}")
            print(json.dumps(result, indent=2))
        else:
            print("\n❌ Failed to generate medicine info")
    else:
        print("❌ Cannot connect to LM Studio. Make sure it's running on http://localhost:1234")