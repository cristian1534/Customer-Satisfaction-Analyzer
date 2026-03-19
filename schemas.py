from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class LlamaAnalysisRequest(BaseModel):
    review: str = Field(..., min_length=1, description="Review text to analyze with Llama3.1")

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="Username for login")
    password: str = Field(..., min_length=1, description="Password for login")

class LoginResponse(BaseModel):
    message: str = Field(..., description="Login response message")
    token: Optional[str] = Field(None, description="Authentication token")
    user: Optional[dict] = Field(None, description="User information")

class ReviewCreate(BaseModel):
    review: str = Field(..., min_length=1, description="The review text to analyze for customer satisfaction")

class ReviewResponse(BaseModel):
    id: int
    review: str
    created_at: datetime
    sentiment_score: Optional[float] = Field(None, description="Customer satisfaction score from -1 to 1")
    sentiment_label: Optional[str] = Field(None, description="Satisfaction level: positive, negative, or neutral")
    
    class Config:
        from_attributes = True

class SentimentDistribution(BaseModel):
    positive: int = Field(0, ge=0, description="Number of satisfied reviews")
    negative: int = Field(0, ge=0, description="Number of dissatisfied reviews") 
    neutral: int = Field(0, ge=0, description="Number of neutral reviews")

class SentimentAnalysis(BaseModel):
    total_reviews: int = Field(..., ge=0, description="Total number of reviews analyzed")
    average_sentiment: float = Field(..., description="Average customer satisfaction score")
    sentiment_distribution: SentimentDistribution = Field(..., description="Distribution of satisfaction levels")
    reviews: List[ReviewResponse] = Field(..., description="List of reviews with satisfaction analysis")
