import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo
import io
import base64
from typing import List, Dict
import numpy as np

# Resetear completamente la configuración de matplotlib
matplotlib.rcParams.clear()
plt.style.use('default')

# Configurar estilo moderno sin títulos
matplotlib.rcParams.update({
    'font.family': 'Arial',
    'font.size': 14,
    'axes.titlesize': 0,  # Desactivar títulos completamente
    'axes.labelsize': 14,
    'xtick.labelsize': 13,
    'ytick.labelsize': 13,
    'legend.fontsize': 13,
    'figure.titlesize': 0,  # Desactivar títulos de figura
    'axes.edgecolor': '#333333',
    'axes.facecolor': 'white',
    'figure.facecolor': 'white',
    'text.color': '#333333',
    'axes.labelcolor': '#333333',
    'xtick.color': '#333333',
    'ytick.color': '#333333',
    'grid.color': '#cccccc',
    'legend.framealpha': 0.8,
    'legend.facecolor': 'white',
    'legend.edgecolor': '#cccccc'
})

class AnalyticsVisualizer:
    def __init__(self):
        # Paleta de colores moderna
        self.colors = {
            'positive': '#00d4aa',      # Verde menta moderno
            'negative': '#ff4757',      # Rojo coral moderno  
            'neutral': '#747d8c'        # Gris azulado moderno
        }
    
    def create_sentiment_distribution_chart(self, sentiment_distribution: Dict[str, int]) -> str:
        """
        Crea un gráfico de barras para la distribución de sentimientos
        """
        labels = list(sentiment_distribution.keys())
        values = list(sentiment_distribution.values())
        colors = [self.colors.get(label, '#95a5a6') for label in labels]
        
        plt.figure(figsize=(6, 4.5), dpi=120, facecolor='white')
        ax = plt.gca()
        ax.set_facecolor('white')
        
        # Crear barras modernas
        bars = ax.bar(labels, values, color=colors, alpha=0.85, 
                     edgecolor='white', linewidth=1.2, width=0.6)
        
        # Añadir valores sobre las barras con estilo moderno
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + max(values)*0.03,
                   str(value), ha='center', va='bottom', fontweight='bold', 
                   fontsize=28, color='#333333')
        
        # Styling moderno
        ax.set_title('')  # Eliminar explícitamente cualquier título
        ax.set_xlabel('Sentimiento', fontsize=14, color='#333333', fontweight='500')
        ax.set_ylabel('Cantidad', fontsize=14, color='#333333', fontweight='500')
        ax.tick_params(colors='#333333', labelsize=13)
        ax.spines['bottom'].set_color('#cccccc')
        ax.spines['left'].set_color('#cccccc')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3, color='#cccccc', linestyle='--')
        
        plt.tight_layout(pad=1.2)
        
        # Guardar como base64
        return self._save_plot_as_base64()
    
    def create_sentiment_timeline(self, reviews_data: List[Dict]) -> str:
        """
        Crea un gráfico de línea mostrando el sentimiento a lo largo del tiempo
        """
        if not reviews_data:
            return self._create_empty_chart("No hay datos para mostrar")
        
        # Ordenar por fecha
        sorted_reviews = sorted(reviews_data, key=lambda x: x['created_at'])
        
        dates = [r['created_at'].strftime('%m/%d') for r in sorted_reviews]
        scores = [r['sentiment_score'] or 0 for r in sorted_reviews]
        
        plt.figure(figsize=(6, 4.5), dpi=120, facecolor='white')
        ax = plt.gca()
        ax.set_facecolor('white')
        
        # Línea moderna con gradiente
        ax.plot(dates, scores, marker='o', linewidth=2.5, markersize=5, 
                alpha=0.9, color='#00d4aa', markeredgecolor='white', 
                markeredgewidth=1.5, label='Sentimiento')
        
        # Línea de referencia moderna
        ax.axhline(y=0, color='#ff4757', linestyle='--', alpha=0.7, linewidth=1.5)
        
        # Área bajo la curva con gradiente
        ax.fill_between(dates, scores, 0, alpha=0.2, color='#00d4aa')
        
        # Styling moderno
        ax.set_title('')  # Eliminar explícitamente cualquier título
        ax.set_xlabel('Fecha', fontsize=14, color='#333333', fontweight='500')
        ax.set_ylabel('Puntuación', fontsize=14, color='#333333', fontweight='500')
        ax.tick_params(colors='#333333', labelsize=13)
        ax.spines['bottom'].set_color('#cccccc')
        ax.spines['left'].set_color('#cccccc')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3, color='#cccccc', linestyle='--')
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout(pad=1.2)
        
        return self._save_plot_as_base64()
    
    def create_sentiment_pie_chart(self, sentiment_distribution: Dict[str, int]) -> str:
        """
        Crea un gráfico de pastel para la distribución de sentimientos
        """
        labels = list(sentiment_distribution.keys())
        values = list(sentiment_distribution.values())
        colors = [self.colors.get(label, '#95a5a6') for label in labels]
        
        # Calcular porcentajes
        total = sum(values)
        if total == 0:
            return self._create_empty_chart("No hay datos para mostrar")
        
        plt.figure(figsize=(6, 4.5), dpi=120, facecolor='white')
        ax = plt.gca()
        ax.set_facecolor('white')
        
        # Pastel moderno con explode y sombra
        wedges, texts, autotexts = ax.pie(values, labels=labels, colors=colors, 
                                         autopct='%1.1f%%', startangle=90,
                                         explode=[0.08]*len(labels),
                                         shadow=True, pctdistance=0.75,
                                         textprops={'fontsize': 26, 'fontweight': '600'})
        
        # Personalizar texto moderno
        for autotext in autotexts:
            autotext.set_color('white')
        
        for text in texts:
            text.set_color('#333333')
            text.set_fontsize(13)
            text.set_fontweight('500')
        
        ax.set_title('')  # Eliminar explícitamente cualquier título
        plt.tight_layout(pad=1.2)
    
    def create_confidence_histogram(self, reviews_data: List[Dict]) -> str:
        """
        Crea un histograma de las puntuaciones de confianza
        """
        if not reviews_data:
            return self._create_empty_chart("No hay datos para mostrar")
        
        scores = [abs(r['sentiment_score'] or 0) for r in reviews_data]
        
        plt.figure(figsize=(6, 4.5), dpi=120, facecolor='white')
        ax = plt.gca()
        ax.set_facecolor('white')
        
        # Histograma moderno
        n, bins, patches = plt.hist(scores, bins=15, alpha=0.7, color='#00d4aa', 
                                   edgecolor='white', linewidth=1.2)
        
        # Colorear barras con gradiente
        for i, patch in enumerate(patches):
            patch.set_alpha(0.7 + 0.3 * (i / len(patches)))
        
        # Línea de promedio moderna
        mean_val = np.mean(scores)
        ax.axvline(mean_val, color='#ff4757', linestyle='--', alpha=0.8, 
                  linewidth=2, label=f'Prom: {mean_val:.2f}')
        
        # Styling moderno
        ax.set_title('')  # Eliminar explícitamente cualquier título
        ax.set_xlabel('Confianza', fontsize=14, color='#333333', fontweight='500')
        ax.set_ylabel('Frecuencia', fontsize=14, color='#333333', fontweight='500')
        ax.tick_params(colors='#333333', labelsize=13)
        ax.spines['bottom'].set_color('#cccccc')
        ax.spines['left'].set_color('#cccccc')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.grid(True, alpha=0.3, color='#cccccc', linestyle='--')
        
        # Leyenda moderna
        legend = ax.legend(facecolor='white', edgecolor='#cccccc', 
                          framealpha=0.9, fontsize=13)
        plt.setp(legend.get_texts(), color='#333333')
        
        plt.tight_layout(pad=1.2)
        
        return self._save_plot_as_base64()
    
    def _save_plot_as_base64(self) -> str:
        """
        Guarda el gráfico actual como string base64
        """
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close('all')  # Forzar cierre de todas las figuras
        buffer.close()
        return image_base64
    
    def _create_empty_chart(self, message: str) -> str:
        """
        Crea un gráfico vacío con un mensaje
        """
        plt.figure(figsize=(6, 4.5), dpi=120, facecolor='white')
        ax = plt.gca()
        ax.set_facecolor('white')
        ax.text(0.5, 0.5, message, ha='center', va='center', 
                fontsize=16, color='#333333', transform=ax.transAxes,
                fontweight='500')
        ax.axis('off')
        return self._save_plot_as_base64()

# Instancia global
analytics_visualizer = AnalyticsVisualizer()
