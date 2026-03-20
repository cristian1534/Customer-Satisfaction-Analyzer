from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import requests
import os

from datetime import datetime
from database import get_db, create_tables, Review, User
from schemas import ReviewCreate, ReviewResponse, SentimentAnalysis, SentimentDistribution, LlamaAnalysisRequest, LoginRequest, LoginResponse
from customer_satisfaction_analyzer import customer_satisfaction_analyzer
from analytics_visualizer import analytics_visualizer

load_dotenv()

app = FastAPI(
    title="Customer Satisfaction Analysis API", 
    version="1.0.0",
    description="API for analyzing customer satisfaction and sentiment",
    tags_metadata=[
        {
            "name": "Reviews Routes",
            "description": "Operations for customer reviews and sentiment analysis"
        },
        {
            "name": "Health",
            "description": "Health check and system status"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Create tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

@app.post("/reviews", response_model=ReviewResponse, tags=["Reviews Routes"])
async def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """
    Save a review and analyze customer satisfaction
    """
    try:
        # Customer satisfaction analysis
        analysis_result = customer_satisfaction_analyzer(review.review)
        
        # Use values from analyzer directly
        satisfaction_label = analysis_result['sentiment_label']
        satisfaction_score = analysis_result['sentiment_score']
        
        # Create review record
        db_review = Review(
            review=review.review,
            sentiment_score=satisfaction_score,
            sentiment_label=satisfaction_label
        )
        
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        return db_review
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving review: {str(e)}")

@app.get("/reviews/analytics", response_model=SentimentAnalysis, tags=["Reviews Routes"])
async def get_reviews_analytics(db: Session = Depends(get_db)):
    """
    Get all reviews and generate customer satisfaction analysis
    """
    try:
        # Get all reviews
        reviews = db.query(Review).all()
        
        if not reviews:
            return SentimentAnalysis(
                total_reviews=0,
                average_sentiment=0.0,
                sentiment_distribution=SentimentDistribution(positive=0, negative=0, neutral=0),
                reviews=[]
            )
        
        # Calculate analytics
        total_reviews = len(reviews)
        sentiment_scores = [r.sentiment_score or 0.0 for r in reviews]
        average_sentiment = sum(sentiment_scores) / total_reviews if total_reviews > 0 else 0.0
        
        # Count sentiment labels
        sentiment_counts = {"positive": 0, "negative": 0, "neutral": 0}
        for review in reviews:
            if review.sentiment_label:
                sentiment_counts[review.sentiment_label] += 1
        
        sentiment_distribution = SentimentDistribution(**sentiment_counts)
        
        # Convert to response models
        review_responses = [
            ReviewResponse(
                id=r.id,
                review=r.review,
                created_at=r.created_at.isoformat(),
                sentiment_score=r.sentiment_score,
                sentiment_label=r.sentiment_label
            ) for r in reviews
        ]
        
        return SentimentAnalysis(
            total_reviews=total_reviews,
            average_sentiment=average_sentiment,
            sentiment_distribution=sentiment_distribution,
            reviews=review_responses
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analytics: {str(e)}")

@app.post("/reviews/detailed-analysis", tags=["Reviews Routes"])
async def detailed_analysis(review: ReviewCreate):
    """
    Perform detailed customer satisfaction analysis sentence by sentence
    """
    try:
        # Simple analysis since we don't have the complex analyzer anymore
        analysis_result = customer_satisfaction_analyzer(review.review)
        
        return {
            "original_review": review.review,
            "sentence_analysis": [{
                "sentence": review.review,
                "sentiment": analysis_result['sentiment_label'],
                "score": analysis_result['sentiment_score'],
                "confidence": analysis_result['confidence']
            }],
            "total_sentences": 1
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in detailed analysis: {str(e)}")

@app.get("/reviews/visualizations", tags=["Reviews Routes"])
async def get_visualizations(db: Session = Depends(get_db)):
    """
    Generate visualization charts for customer satisfaction analytics
    """
    try:
        # Get all reviews
        reviews = db.query(Review).all()
        
        if not reviews:
            return {
                "sentiment_distribution_chart": analytics_visualizer.create_empty_chart("No reviews available"),
                "sentiment_pie_chart": analytics_visualizer.create_empty_chart("No reviews available"),
                "sentiment_timeline": analytics_visualizer.create_empty_chart("No reviews available"),
                "confidence_histogram": analytics_visualizer.create_empty_chart("No reviews available")
            }
        
        # Calculate analytics
        sentiment_distribution = {"positive": 0, "negative": 0, "neutral": 0}
        reviews_data = []
        
        for review in reviews:
            if review.sentiment_label:
                sentiment_distribution[review.sentiment_label] += 1
            
            reviews_data.append({
                "created_at": review.created_at.isoformat(),
                "sentiment_score": review.sentiment_score
            })
        
        # Generate charts
        return {
            "sentiment_distribution_chart": analytics_visualizer.create_sentiment_distribution_chart(sentiment_distribution),
            "sentiment_pie_chart": analytics_visualizer.create_sentiment_pie_chart(sentiment_distribution),
            "sentiment_timeline": analytics_visualizer.create_sentiment_timeline(reviews_data),
            "confidence_histogram": analytics_visualizer.create_confidence_histogram(reviews_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating visualizations: {str(e)}")

@app.post("/analyze", tags=["Reviews Routes"])
async def analyze_with_llama(request: LlamaAnalysisRequest):
    """
    Analyze a review using Llama3.1 through Ollama with fallback
    """
    try:
        # Use the customer_satisfaction_analyzer which has fallback built-in
        analysis_result = customer_satisfaction_analyzer(request.review)
        
        # Convert to the expected format for this endpoint
        return {
            "sentiment": analysis_result['sentiment_label'],
            "score": analysis_result['sentiment_score'],
            "summary": analysis_result.get('explanation', 'Analysis completed'),
            "review": request.review
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in analysis: {str(e)}")

@app.post("/business-insights", tags=["Reviews Routes"])
async def analyze_business_insights(db: Session = Depends(get_db)):
    """
    Analyze all reviews from DB to generate business insights and improvement proposals
    """
    try:
        # Get all reviews from database
        reviews = db.query(Review).all()
        print(f"Total reviews found: {len(reviews)}")
        
        if not reviews:
            return {
                "insights": "No reviews available for analysis",
                "improvements": [],
                "total_reviews": 0
            }
        
        # Process in batches of 10 reviews to avoid timeouts
        batch_size = 10
        all_insights = []
        
        for i in range(0, len(reviews), batch_size):
            batch_reviews = reviews[i:i + batch_size]
            
            # Prepare text with batch of reviews
            reviews_text = "\n".join([f"- {r.review}" for r in batch_reviews])
            
            payload = {
                "model": "llama3.1",
                "prompt": f"""
            Analyze this batch of customer reviews and generate specific insights:

            Reviews:
            {reviews_text}

            Respond in JSON format:
            {{
              "batch_insights": "analysis of this specific batch",
              "key_themes": ["theme 1", "theme 2"],
              "sentiment_trend": "positive/negative/mixed"
            }}
            """,
                "stream": False
            }

            response = requests.post(os.getenv("OLLAMA_URL", "http://localhost:11435/api/generate"), json=payload, timeout=120)
            response.raise_for_status()
            
            # Extract and parse response
            data = response.json()
            llm_response = data.get("response", "")
            
            # Try to parse JSON
            try:
                import json
                import re
                
                json_match = re.search(r'\{.*\}', llm_response, re.DOTALL)
                if json_match:
                    batch_data = json.loads(json_match.group())
                    all_insights.append(batch_data)
                else:
                    all_insights.append({
                        "batch_insights": "Could not process this batch",
                        "key_themes": [],
                        "sentiment_trend": "neutral"
                    })
            except:
                all_insights.append({
                    "batch_insights": "Error in analysis",
                    "key_themes": [],
                    "sentiment_trend": "neutral"
                })
        
        # Consolidate all batch insights
        total_sentiments = [insight.get("sentiment_trend", "neutral") for insight in all_insights]
        all_themes = []
        for insight in all_insights:
            all_themes.extend(insight.get("key_themes", []))
        
        # Determine overall sentiment
        positive_count = total_sentiments.count("positive")
        negative_count = total_sentiments.count("negative")
        if positive_count > negative_count:
            overall_sentiment = "positive"
        elif negative_count > positive_count:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "mixed"
        
        # Generate consolidated insights
        consolidated_insights = f"Analysis of {len(reviews)} reviews in {len(all_insights)} batches. " + " ".join([insight.get("batch_insights", "") for insight in all_insights])
        
        # Identify critical areas (most repeated)
        from collections import Counter
        theme_counts = Counter(all_themes)
        critical_areas = [theme for theme, count in theme_counts.most_common(5)]
        
        # Generate improvement proposals based on critical areas
        improvements = []
        for area in critical_areas[:3]:
            improvements.append(f"Improve {area} based on recurring feedback")
        
        # Determine action priority
        if negative_count > len(all_insights) / 2:
            action_priority = "high"
        elif negative_count > 0:
            action_priority = "medium"
        else:
            action_priority = "low"
        
        return {
            "insights": consolidated_insights[:500] + "..." if len(consolidated_insights) > 500 else consolidated_insights,
            "improvements": improvements,
            "overall_sentiment": overall_sentiment,
            "critical_areas": critical_areas,
            "action_priority": action_priority,
            "total_reviews": len(reviews),
            "batches_processed": len(all_insights),
            "analysis_date": "2026-03-19"
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Llama3.1: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in business analysis: {str(e)}")

@app.post("/login", response_model=LoginResponse, tags=["Reviews Routes"])
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return token
    """
    try:
        # Find user by username
        user = db.query(User).filter(User.username == request.username).first()
        
        if not user or user.password != request.password:
            raise HTTPException(status_code=401, detail="Invalid username or password")
        
        # Generate simple token (in production, use JWT)
        from jose import jwt
        import os
        from datetime import datetime, timedelta
        
        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=24)},
            "your-secret-key",  # In production, use environment variable
            algorithm="HS256"
        )
        
        return LoginResponse(
            message="Login successful",
            token=token,
            user={"id": user.id, "username": user.username}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login error: {str(e)}")

@app.post("/create-admin", tags=["Reviews Routes"])
async def create_admin_user(db: Session = Depends(get_db)):
    """
    Create admin user (admin/admin123)
    """
    try:
        # Check if admin user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            return {"message": "Admin user already exists"}
        
        # Create admin user
        admin_user = User(
            username="admin",
            password="admin123"  # In production, hash this password
        )
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        return {
            "message": "Admin user created successfully",
            "username": "admin",
            "password": "admin123"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating admin user: {str(e)}")

@app.delete("/reviews", tags=["Reviews Routes"])
async def delete_all_reviews(db: Session = Depends(get_db)):
    """
    Delete all reviews from the database
    """
    try:
        # Count reviews before deletion
        total_reviews = db.query(Review).count()
        
        if total_reviews == 0:
            return {
                "message": "No reviews found to delete",
                "deleted_count": 0
            }
        
        # Delete all reviews
        db.query(Review).delete()
        db.commit()
        
        return {
            "message": f"Successfully deleted {total_reviews} reviews",
            "deleted_count": total_reviews
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting reviews: {str(e)}")

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for Render deployment"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/", tags=["Root"])
async def root():
    """
    Health check endpoint to verify the API is running
    """
    return {"message": "Reviews API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
