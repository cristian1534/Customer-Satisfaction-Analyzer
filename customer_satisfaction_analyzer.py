import json
import os
from typing import Dict

def customer_satisfaction_analyzer(review: str):
    """
    Analyze customer satisfaction using Ollama Llama3.1 model
    Returns sentiment score and label
    """
    try:
        # Try to use Ollama if available
        import requests
        
        # Ollama API endpoint from environment variable
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11435/api/generate")
        
        print(f"DEBUG: Using Ollama URL: {ollama_url}")
        
        # Prompt for sentiment analysis
        prompt = f"""
        Analyze the sentiment of this customer review and respond with ONLY a JSON object:
        
        Review: "{review}"
        
        Return format: {{"sentiment": "positive/negative/neutral", "confidence": 0.0-1.0, "explanation": "brief explanation in English"}}
        """
        
        payload = {
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "max_tokens": 100
            }
        }
        
        print(f"DEBUG: Sending payload: {payload}")
        
        response = requests.post(ollama_url, json=payload, timeout=120)
        
        print(f"DEBUG: Ollama response status: {response.status_code}")
        print(f"DEBUG: Ollama response text: {response.text[:200]}...")
        
        # Check if response is successful
        if response.status_code != 200:
            raise Exception(f"Ollama returned status {response.status_code}")
        
        response.raise_for_status()
        
        result = response.json()
        response_text = result.get("response", "")
        
        print(f"DEBUG: Extracted response_text: {response_text}")
        
        # Extract JSON from response
        try:
            # Find JSON in the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            
            print(f"DEBUG: JSON bounds: {start_idx} to {end_idx}")
            
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx]
                print(f"DEBUG: Extracted JSON: {json_str}")
                analysis = json.loads(json_str)
                print(f"DEBUG: Parsed analysis: {analysis}")
                
                return {
                    "sentiment_score": 0.8 if analysis.get("sentiment") == "positive" else -0.8 if analysis.get("sentiment") == "negative" else 0.0,
                    "sentiment_label": analysis.get("sentiment", "neutral"),
                    "confidence": analysis.get("confidence", 0.5),
                    "explanation": analysis.get("explanation", "")
                }
            else:
                print("DEBUG: No JSON bounds found")
                raise Exception("No JSON found in response")
                
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON decode error: {e}")
            raise Exception(f"JSON decode error: {e}")
        
    except Exception as e:
        print(f"DEBUG: Exception occurred: {e}")
        # For now, raise the exception instead of using fallback
        raise Exception(f"Analysis failed: {str(e)}")

def fallback_sentiment_analysis(review: str) -> Dict:
    """
    Simple rule-based sentiment analysis as fallback
    """
    # Simple keyword-based analysis
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'perfect', 'best', 'awesome', 'brilliant', 'outstanding', 'happy', 'satisfied', 'pleased', 'delighted']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst', 'disgusting', 'disappointing', 'poor', 'useless', 'broken', 'failed', 'unhappy', 'dissatisfied', 'angry', 'frustrated']
    
    review_lower = review.lower()
    
    positive_count = sum(1 for word in positive_words if word in review_lower)
    negative_count = sum(1 for word in negative_words if word in review_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        score = min(0.8, 0.5 + (positive_count - negative_count) * 0.1)
    elif negative_count > positive_count:
        sentiment = "negative"
        score = max(-0.8, -0.5 - (negative_count - positive_count) * 0.1)
    else:
        sentiment = "neutral"
        score = 0.0
    
    return {
        "sentiment_score": score,
        "sentiment_label": sentiment,
        "confidence": 0.6,
        "explanation": "Rule-based analysis (fallback)"
    }
