# Reviews API with FastAPI

Backend API para gestionar reviews con análisis de sentimiento usando IA.

## Endpoints

### POST /reviews
Guarda una review en la base de datos PostgreSQL y analiza su sentimiento.

**Request Body:**
```json
{
  "review": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "review": "string",
  "created_at": "2024-01-01T00:00:00",
  "sentiment_score": 0.8,
  "sentiment_label": "positive"
}
```

### GET /reviews/analytics
Trae todas las reviews con análisis de sentimiento y estadísticas.

**Response:**
```json
{
  "total_reviews": 10,
  "average_sentiment": 0.3,
  "sentiment_distribution": {
    "positive": 4,
    "negative": 2,
    "neutral": 4
  },
  "reviews": [...]
}
```

## Configuración

1. Copiar `.env.example` a `.env`
2. Configurar la URL de PostgreSQL:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/reviews_db
   ```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

La API correrá en `http://localhost:8000`
