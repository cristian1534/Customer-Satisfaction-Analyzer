# Customer Satisfaction Analyzer

Una aplicación completa de análisis de sentimientos de clientes con FastAPI backend y frontend React. Utiliza inteligencia artificial para analizar reseñas de clientes y proporcionar insights de negocio valiosos.

## 🚀 Características

### Backend (FastAPI + PostgreSQL)
- **📝 Análisis de Sentimientos**: Procesamiento de reseñas con IA (Ollama + Llama3.1)
- **🔐 Autenticación**: Sistema de login con JWT tokens
- **📊 Analytics**: Métricas y visualizaciones de satisfacción
- **🎯 Business Insights**: Análisis avanzado con recomendaciones
- **🗄️ Base de Datos**: PostgreSQL para almacenamiento persistente
- **🐳 Docker**: Contenerización para deploy fácil

### Frontend (React + TypeScript)
- **🎨 Diseño Moderno**: UI con gradientes y glassmorphism
- **📱 Responsive**: Adaptable a todos los dispositivos
- **🔐 Login**: Formulario de autenticación seguro
- **📝 Review Form**: Envío de reseñas con análisis instantáneo
- **📊 Analytics Dashboard**: Visualización de métricas en tiempo real
- **🎯 Business Insights**: Insights detallados con recomendaciones
- **🧭 Navegación**: Menu dinámico basado en autenticación

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI**: Framework API moderno y rápido
- **PostgreSQL**: Base de datos relacional robusta
- **SQLAlchemy**: ORM para manejo de base de datos
- **JWT**: Autenticación segura con tokens
- **Pydantic**: Validación de datos
- **Ollama**: Integración con Llama3.1 para análisis de IA
- **Uvicorn**: Servidor ASGI de alto rendimiento

### Frontend
- **React 18**: Framework de frontend moderno
- **TypeScript**: Tipado seguro
- **TailwindCSS**: Framework de CSS utilitario
- **Lucide React**: Iconos modernos
- **Next.js 13+**: App Router y Server Components

### Deploy
- **Docker**: Contenerización
- **Render.com**: Plataforma de deploy en la nube
- **GitHub**: Control de versiones y CI/CD

## 📁 Estructura del Proyecto

```
Satisfaction/
├── main_simple.py              # API FastAPI principal
├── database.py                 # Modelos y conexión a BD
├── schemas.py                  # Esquemas Pydantic
├── customer_satisfaction_analyzer.py  # Motor de IA
├── analytics_visualizer.py     # Procesamiento de analytics
├── requirements.txt            # Dependencias Python
├── Dockerfile                  # Configuración Docker
├── .env.example               # Variables de entorno ejemplo
└── .gitignore                 # Archivos ignorados

sentiment-saas-frontend/
├── src/
│   ├── app/
│   │   ├── page.tsx           # Página principal
│   │   ├── analytics/page.tsx # Dashboard de analytics
│   │   ├── login/page.tsx     # Página de login
│   │   └── business-insights/page.tsx  # Insights
│   └── components/
│       ├── ReviewForm.tsx      # Formulario de reseñas
│       ├── AnalyticsDashboard.tsx  # Dashboard
│       ├── BusinessInsights.tsx  # Insights
│       ├── LoginForm.tsx       # Login
│       └── Navigation.tsx      # Navegación
```

## 🚀 Quick Start

### Backend Local
```bash
# Clonar repositorio
git clone https://github.com/cristian1534/Customer-Satisfaction-Analyzer.git
cd Satisfaction

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tu configuración de base de datos

# Iniciar servidor
python3 main_simple.py
```

### Frontend Local
```bash
cd ../sentiment-saas-frontend
npm install
npm run dev
```

## 🌐 Deploy en Producción

### Render.com
1. **Conectar GitHub**: Conectar este repositorio a Render
2. **Variables de Entorno**:
   ```
   DATABASE_URL=postgresql://...
   JWT_SECRET_KEY=your-secret-key
   PORT=8000
   ```
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `uvicorn main_simple:app --host 0.0.0.0 --port $PORT`

### Docker
```bash
# Build
docker build -t customer-satisfaction-analyzer .

# Run
docker run -p 8000:8000 -e DATABASE_URL=postgresql://... customer-satisfaction-analyzer
```

## 📊 API Endpoints

### Autenticación
- `POST /login` - Login de usuario
- `POST /create-admin` - Crear usuario admin

### Reviews
- `POST /reviews` - Crear nueva reseña
- `GET /reviews/analytics` - Obtener analytics
- `DELETE /reviews/delete-all` - Eliminar todas las reseñas

### Insights
- `POST /business-insights` - Generar insights de negocio

### Health
- `GET /health` - Health check para monitoring

## 🎨 Características del Frontend

### Diseño Moderno
- **Gradientes**: Esquema de colores vibrantes
- **Glassmorphism**: Efectos de transparencia y blur
- **Responsive**: Adaptación perfecta a móviles
- **Animaciones**: Transiciones suaves y micro-interacciones

### Experiencia de Usuario
- **Login Seguro**: Autenticación con JWT
- **Feedback Instantáneo**: Análisis en tiempo real
- **Navegación Intuitiva**: Menu contextual basado en auth
- **Visualización de Datos**: Charts y métricas claras

## 🔐 Seguridad

- **JWT Tokens**: Autenticación segura y sin estado
- **Password Hashing**: bcrypt para almacenamiento seguro
- **CORS**: Configuración segura de recursos cruzados
- **Environment Variables**: Configuración sensible protegida

## 📈 Analytics y Métricas

### Métricas Principales
- **Total de Reviews**: Conteo total de reseñas
- **Sentiment Score**: Puntuación promedio de satisfacción
- **Distribución**: Positivos, Negativos, Neutrales
- **Tendencias**: Evolución temporal del sentimiento

### Business Insights
- **Áreas Críticas**: Identificación automática de problemas
- **Recomendaciones**: Sugerencias de mejora basadas en IA
- **Prioridades**: Clasificación de acciones por impacto
- **Análisis Batch**: Procesamiento eficiente de grandes volúmenes

## 🤖 Inteligencia Artificial

### Motor de Análisis
- **Modelo**: Llama3.1 via Ollama
- **Batch Processing**: Procesamiento eficiente de múltiples reviews
- **JSON Parsing**: Extracción robusta de respuestas
- **Timeout Handling**: Gestión de peticiones largas

### Características
- **Análisis de Sentimiento**: Clasificación precisa (positive/negative/neutral)
- **Score de Confianza**: Métrica de fiabilidad del análisis
- **Insights Automáticos**: Generación de recomendaciones
- **Procesamiento Paralelo**: Optimización de rendimiento

## 🔄 Flujo de Trabajo

1. **Usuario** envía reseña → **Frontend** muestra formulario
2. **Frontend** envía a API → **Backend** procesa con IA
3. **Backend** almacena en BD → **PostgreSQL** persiste datos
4. **Frontend** muestra análisis → **Usuario** ve resultados
5. **Analytics** actualizados → **Dashboard** refleja cambios

## 🧰 Desarrollo

### Scripts Útiles
```bash
# Backend development
python3 main_simple.py

# Verificar health
curl http://localhost:8000/health

# Test endpoints
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Debugging
- **Logs**: Verificar logs de Uvicorn
- **Database**: Conectar a PostgreSQL para verificar datos
- **Health Check**: `/health` endpoint para monitoreo

## 📝 Notas de Deploy

### Variables de Entorno Requeridas
- `DATABASE_URL`: Cadena de conexión PostgreSQL
- `JWT_SECRET_KEY`: Clave secreta para tokens
- `PORT`: Puerto del servidor (usualmente 8000)

### Consideraciones
- **Ollama**: Necesario para análisis de sentimientos
- **PostgreSQL**: Requiere configuración de conexión
- **Memory**: Considerar RAM para procesamiento batch

## 🤝 Contribuciones

1. Fork del repositorio
2. Feature branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a branch (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 👨‍💻 Autor

**Cristian Machuca** - *Desarrollo Full Stack* - [GitHub](https://github.com/cristian1534)

---

🚀 **Listo para deploy en producción con Render.com!**
