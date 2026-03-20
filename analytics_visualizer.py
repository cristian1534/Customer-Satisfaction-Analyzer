from typing import Dict, List

def analytics_visualizer(reviews: List[Dict]):
    """
    Generate analytics insights from reviews data
    Simple implementation without heavy dependencies
    """
    if not reviews:
        return {
            "total_reviews": 0,
            "average_sentiment": 0.0,
            "sentiment_distribution": {
                "positive": 0,
                "negative": 0,
                "neutral": 0
            },
            "recommendations": [],
            "critical_areas": [],
            "action_priority": "low"
        }
    
    # Calculate basic metrics
    total_reviews = len(reviews)
    sentiment_scores = [review.get('sentiment_score', 0) for review in reviews]
    average_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    
    # Count sentiment distribution
    positive_count = sum(1 for review in reviews if review.get('sentiment_label') == 'positive')
    negative_count = sum(1 for review in reviews if review.get('sentiment_label') == 'negative')
    neutral_count = sum(1 for review in reviews if review.get('sentiment_label') == 'neutral')
    
    # Generate simple recommendations
    recommendations = []
    critical_areas = []
    
    if negative_count > positive_count:
        recommendations.append("Focus on improving customer satisfaction - negative reviews exceed positive ones")
        critical_areas.append("Customer service quality")
        action_priority = "high"
    elif average_sentiment < 0:
        recommendations.append("Overall sentiment is negative - immediate action required")
        critical_areas.append("Product/Service quality")
        action_priority = "high"
    elif average_sentiment < 0.3:
        recommendations.append("Sentiment is below average - consider customer feedback surveys")
        action_priority = "medium"
    else:
        recommendations.append("Maintain current customer satisfaction levels")
        action_priority = "low"
    
    if neutral_count > total_reviews * 0.5:
        recommendations.append("Many neutral reviews - encourage more detailed feedback")
        critical_areas.append("Customer engagement")
    
    return {
        "total_reviews": total_reviews,
        "average_sentiment": round(average_sentiment, 3),
        "sentiment_distribution": {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count
        },
        "recommendations": recommendations,
        "critical_areas": critical_areas,
        "action_priority": action_priority,
        "batches_processed": 1,
        "analysis_date": "2024-01-01",
        "insights": f"Analysis of {total_reviews} reviews shows {action_priority} priority for improvements"
    }
