import os
import json
from typing import Dict
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from .preprocess import preprocess_text

ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'api_artifacts')
ARTIFACTS_DIR = os.path.abspath(ARTIFACTS_DIR)

# Load resources
_emojis = {}
_stopwords = []

try:
    with open(os.path.join(ARTIFACTS_DIR, "emoji_dict.json"), encoding="utf-8") as f:
        _emojis = json.load(f)
except Exception:
    _emojis = {}

try:
    with open(os.path.join(ARTIFACTS_DIR, "stopwords_list.json"), encoding="utf-8") as f:
        _stopwords = json.load(f)
except Exception:
    _stopwords = []

# Load model and vectorizer
model = None
vectorizer = None
try:
    model = joblib.load(os.path.join(ARTIFACTS_DIR, "sentiment_model.joblib"))
    vectorizer = joblib.load(os.path.join(ARTIFACTS_DIR, "tfidf_vectorizer.joblib"))
except Exception as e:
    # keep None and handle in endpoints
    print(f"Warning: could not load model/vectorizer: {e}")

app = FastAPI(title="Sentiment Analysis API")


class TweetRequest(BaseModel):
    text: str


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None, "vectorizer_loaded": vectorizer is not None}


@app.post("/predict")
def predict(request: TweetRequest):
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Model not loaded")
    cleaned_text = preprocess_text(request.text, emojis=_emojis, stopwords_list=_stopwords)
    X = vectorizer.transform([cleaned_text])
    proba = model.predict_proba(X)[0]
    sentiment = "positive" if proba[1] >= proba[0] else "negative"
    confidence = float(max(proba))
    return {"sentiment": sentiment, "confidence": confidence, "probability_positive": float(proba[1]), "probability_negative": float(proba[0])}


@app.post("/explain")
def explain(request: TweetRequest):
    # Try to use LIME; if unavailable, provide a simple fallback explanation
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Model not loaded")
    cleaned_text = preprocess_text(request.text, emojis=_emojis, stopwords_list=_stopwords)
    if len(cleaned_text.strip().split()) < 2:
        return {"sentiment": "neutral", "explanation": [], "html_explanation": "<div style=\"font-family: Arial, sans-serif; color: #ff9800;\"><p>⚠️ Le texte est trop court pour générer une explication. Veuillez entrer au moins 2 mots.</p></div>", "warning": True}

    try:
        # Lazy import to keep startup light
        from lime.lime_text import LimeTextExplainer

        class_names = ["negative", "positive"]
        explainer = LimeTextExplainer(class_names=class_names)

        def predict_proba_lime(texts):
            X = vectorizer.transform([preprocess_text(t, emojis=_emojis, stopwords_list=_stopwords) for t in texts])
            return model.predict_proba(X)

        exp = explainer.explain_instance(cleaned_text, predict_proba_lime, num_features=10)
        html_exp = exp.as_html()
        sentiment = "positive" if model.predict(vectorizer.transform([cleaned_text]))[0] == 1 else "negative"
        return {"sentiment": sentiment, "explanation": exp.as_list(), "html_explanation": html_exp}

    except Exception:
        # Fallback explanation: use linear model coefficients and TF-IDF weights
        try:
            X = vectorizer.transform([cleaned_text])
            feature_names = None
            try:
                feature_names = list(vectorizer.get_feature_names_out())
            except Exception:
                # older vectorizer
                try:
                    feature_names = list(vectorizer.get_feature_names())
                except Exception:
                    feature_names = None

            contribs = []
            if feature_names is not None and hasattr(model, "coef_"):
                coef = model.coef_[0]
                xarr = X.toarray()[0]
                # compute token contributions (coef * tfidf)
                for idx, val in enumerate(xarr):
                    if val != 0 and idx < len(coef):
                        contribs.append((feature_names[idx], float(coef[idx] * val)))

            # Pick top positive and negative contributions
            contribs_sorted = sorted(contribs, key=lambda x: -abs(x[1]))[:10]
            explanation = [(w, float(score)) for w, score in contribs_sorted]

            # Build a simple HTML snippet with grey styling for improved visibility
            html_lines = [
                "<div style=\"font-family: Arial, sans-serif; color: #6b7280; background: transparent;\">",
                "<h3 style=\"color: #374151; margin: 0 0 8px 0;\">Explanation (fallback)</h3>",
                "<ul style=\"color: #6b7280; padding-left: 18px; margin: 0 0 8px 0;\">",
            ]

            for w, s in explanation:
                # Use grey shades for token and score so everything is visible on light/dark backgrounds
                html_lines.append(
                    f"<li style=\"margin-bottom:6px;\"><b style=\"color:#374151;\">{w}</b> : <span style=\"color:#6b7280;\">{s:.4f}</span></li>"
                )

            html_lines.append("</ul>")
            html_lines.append("</div>")
            html_exp = "\n".join(html_lines)

            sentiment = "positive" if model.predict(vectorizer.transform([cleaned_text]))[0] == 1 else "negative"
            return {"sentiment": sentiment, "explanation": explanation, "html_explanation": html_exp}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Could not generate explanation: {e}")


@app.get("/", response_class=HTMLResponse)
def root():
    html_content = """
    <html>
        <head>
            <title>Sentiment Analysis API</title>
            <style>
                body { font-family: Arial, sans-serif; background-color: #f0f8f5; color: #333; padding: 40px; }
                h1 { color: #20a08d; }
                p { font-size: 18px; }
                ul { font-size: 16px; }
                code { background-color: #e0f7f2; padding: 2px 4px; border-radius: 4px; }
            </style>
        </head>
        <body>
            <h1>Bienvenue sur l'API Sentiment Analysis</h1>
            <p>Cette API vous permet de :</p>
            <ul>
                <li>Obtenir la prédiction de sentiment pour un texte via <code>/predict</code></li>
                <li>Obtenir une explication LIME du modèle via <code>/explain</code></li>
                <li>Vérifier l'état de santé de l'API via <code>/health</code></li>
            </ul>
            <p>La documentation interactive est disponible sur <a href="/docs">Swagger UI</a>.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
