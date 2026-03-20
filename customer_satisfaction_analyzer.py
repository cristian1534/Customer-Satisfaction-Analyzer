import json
from typing import Dict

def customer_satisfaction_analyzer(review: str):
    """
    Analyze customer satisfaction using Ollama Llama3.1 model
    Returns sentiment score and label
    """
    try:
        # Try to use Ollama if available
        import requests
        
        # Ollama API endpoint
        ollama_url = "https://299c-91-197-19-120.ngrok-free.app/generate"
        
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
        
        response = requests.post(ollama_url, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            
            # Extract JSON from response
            try:
                # Find JSON in the response
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}") + 1
                
                if start_idx != -1 and end_idx != -1:
                    json_str = response_text[start_idx:end_idx]
                    analysis = json.loads(json_str)
                    
                    return {
                        "sentiment_score": 0.8 if analysis.get("sentiment") == "positive" else -0.8 if analysis.get("sentiment") == "negative" else 0.0,
                        "sentiment_label": analysis.get("sentiment", "neutral"),
                        "confidence": analysis.get("confidence", 0.5),
                        "explanation": analysis.get("explanation", "")
                    }
            except json.JSONDecodeError:
                pass
        
        # Fallback if Ollama fails
        return fallback_sentiment_analysis(review)
        
    except Exception:
        # Fallback for any errors (Ollama not available, network issues, etc.)
        return fallback_sentiment_analysis(review)

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
