import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Usar backend no interactivo
import io
import base64
from typing import List, Dict
from nltk.tokenize import sent_tokenize
import nltk

# Descargar recursos de NLTK
try:
    nltk.download('punkt_tab', quiet=True)
except Exception:
    pass

# Initialize customer satisfaction model (exactly as in Google Colab)
multilanguage_model = None

def load_model():
    global multilanguage_model
    try:
        from transformers import pipeline
        # Use the exact model you use in Google Colab
        multilanguage_model = pipeline('sentiment-analysis')
        print("✅ Customer Satisfaction model loaded successfully (Google Colab configuration)")
        return True
    except Exception as e:
        print(f"❌ Error loading customer satisfaction model: {e}")
        multilanguage_model = None
        return False

# Try to load the model when importing
load_model()

class CustomerSatisfactionAnalyzer:
    def __init__(self):
        self.model = multilanguage_model
        self.colors = {
            'POS': '#22c55e',  # green
            'NEG': '#ef4444',  # red  
            'NEU': '#6b7280'   # gray
        }
    
    def analyze_review(self, review: str, show_details: bool = False) -> Dict:
        """
        Analyze a review using the customer satisfaction model (exactly as in Google Colab)
        """
        if not self.model:
            # Try to load the model if not available
            if load_model():
                self.model = multilanguage_model
            else:
                raise Exception("Customer Satisfaction model not available")
        
        try:
            # Analysis exactly as in Google Colab
            pred_multi = self.model(review)[0]
            
            # Convert model labels to our format
            label_mapping = {
                'POSITIVE': 'positive',
                'NEGATIVE': 'negative', 
                'NEUTRAL': 'neutral'
            }
            
            satisfaction_label = label_mapping.get(pred_multi['label'], 'neutral')
            confidence = pred_multi['score']
            
            # For negatives, convert to negative score
            if satisfaction_label == 'negative':
                satisfaction_score = -confidence
            else:
                satisfaction_score = confidence
            
            result = {
                'general_sentiment': {
                    'label': pred_multi['label'],
                    'confidence': confidence,
                    'satisfaction_label': satisfaction_label,
                    'satisfaction_score': satisfaction_score
                },
                'review': review,
                'confidence': confidence,
                'model_used': 'customer_satisfaction'
            }
            
            if show_details:
                print(f"Review: {review}")
                print('-' * 100)
                print(f"Satisfaction: {pred_multi['label']} ({pred_multi['score']:.3f})")
                print(f"Result: {pred_multi['label']} (confidence: {pred_multi['score']:.3f})")
                print("\n")
            
            return result
            
        except Exception as e:
            print(f"Error analyzing customer satisfaction: {e}")
            return {
                'general_sentiment': {
                    'label': 'NEUTRAL',
                    'confidence': 0.5,
                    'satisfaction_label': 'neutral',
                    'satisfaction_score': 0.0
                },
                'review': review,
                'confidence': 0.5,
                'model_used': 'customer_satisfaction',
                'error': str(e)
            }
    
    def analyze_sentences(self, review: str, show_details: bool = False) -> List[Dict]:
        """
        Analyze a review sentence by sentence for customer satisfaction
        """
        try:
            sentences = sent_tokenize(review)
            results = []
            
            for sentence in sentences:
                result = self.analyze_review(sentence, show_details)
                results.append(result)
                if show_details:
                    print("\n")
            
            return results
            
        except Exception as e:
            print(f"Error analyzing satisfaction sentences: {e}")
            return []
    
    def create_confidence_chart(self, review: str) -> str:
        """
        Create a confidence chart for customer satisfaction analysis
        """
        if not self.model:
            return self._create_empty_chart("Satisfaction model not available")
        
        try:
            pred_multi = self.model(review)[0]
            confidence = pred_multi['score']
            label = pred_multi['label']
            
            # Configure style
            plt.style.use('default')
            matplotlib.rcParams.update({
                'font.family': 'Arial',
                'font.size': 12,
                'axes.titlesize': 0,
                'axes.labelsize': 10,
                'xtick.labelsize': 9,
                'ytick.labelsize': 9,
                'legend.fontsize': 9,
                'figure.titlesize': 0,
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
            
            plt.figure(figsize=(4, 2), dpi=120, facecolor='white')
            ax = plt.gca()
            ax.set_facecolor('white')
            
            # Color by satisfaction level
            color = self.colors.get(label, '#6b7280')
            
            # Create bar
            ax.bar(['Customer Satisfaction'], [confidence], color=color, alpha=0.8, 
                   edgecolor='white', linewidth=1)
            
            # Styling
            ax.set_title('')  # No title to avoid duplication
            ax.set_xlabel('Model', fontsize=10, color='#333333')
            ax.set_ylabel('Satisfaction Score', fontsize=10, color='#333333')
            ax.tick_params(colors='#333333', labelsize=9)
            ax.set_ylim(0, 1)
            ax.spines['bottom'].set_color('#cccccc')
            ax.spines['left'].set_color('#cccccc')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.grid(True, alpha=0.3, color='#cccccc', linestyle='--')
            
            # Add value above bar
            ax.text(0, confidence + 0.02, f'{confidence:.3f}', 
                   ha='center', va='bottom', fontweight='bold', 
                   fontsize=10, color='#333333')
            
            plt.tight_layout(pad=1.2)
            
            return self._save_plot_as_base64()
            
        except Exception as e:
            print(f"Error creating satisfaction chart: {e}")
            return self._create_empty_chart("Error generating satisfaction chart")
    
    def _save_plot_as_base64(self) -> str:
        """
        Save the current plot as base64 string
        """
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=120, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close('all')  # Force close all figures
        buffer.close()
        return image_base64
    
    def _create_empty_chart(self, message: str) -> str:
        """
        Create an empty chart with a message
        """
        plt.figure(figsize=(4, 2), dpi=120, facecolor='white')
        ax = plt.gca()
        ax.set_facecolor('white')
        ax.text(0.5, 0.5, message, ha='center', va='center', 
                fontsize=12, color='#333333', transform=ax.transAxes,
                fontweight='500')
        ax.axis('off')
        return self._save_plot_as_base64()

# Global instance
customer_satisfaction_analyzer = CustomerSatisfactionAnalyzer()
