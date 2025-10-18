# 🚀 Deployment Guide

Guide pour déployer l'API Sentiment Analysis sur Render.

---

## 📋 Prérequis

- Compte GitHub avec accès au repository
- Compte Render.com
- GitHub repository : https://github.com/Skeeder1/Analyse_sentiment_API

---

## 🔧 Configuration initiale (Une seule fois)

### 1. Sur Render Dashboard

#### Créer le service Web

1. Va sur https://dashboard.render.com
2. Clique sur **New +** → **Web Service**
3. Connecte ton repository GitHub
4. Configure :
   - **Name** : `analyse-sentiment-api` (ou ton choix)
   - **Environment** : `Python 3`
   - **Build Command** : (laisser vide ou `pip install -r requirements.txt`)
   - **Start Command** : `./start.sh`
   - **Plan** : `Free` ou `Starter` selon tes besoins

#### Récupère les identifiants

5. Une fois créé, récupère :
   - **Service ID** : Visible dans l'URL ou dans Settings
   - Consulte les logs pour vérifier

---

### 2. Sur GitHub Secrets

#### Ajouter les secrets

1. Va sur https://github.com/Skeeder1/Analyse_sentiment_API/settings/secrets/actions
2. Crée 2 nouveaux secrets :

| Secret Name | Valeur |
|---|---|
| `RENDER_SERVICE_ID` | L'ID de ton service Render |
| `RENDER_API_KEY` | Clé API de Render (voir ci-dessous) |

#### Obtenir la Render API Key

1. Va sur https://dashboard.render.com/account/api-tokens
2. Crée une nouvelle clé API
3. Copie-la (elle s'affiche une seule fois !)
4. Colle-la dans GitHub Secrets

---

## 🔄 Workflow de Déploiement

### Déploiement automatique (recommandé)

```
git push main
    ↓
GitHub Actions vérifie (tests + NLTK)
    ↓ (si ✅)
Render API reçoit commande de redeploy
    ↓
Render redéploie l'application
    ↓
https://analyse-sentiment-api.onrender.com ✅
```

**Logs** :
- GitHub Actions : https://github.com/Skeeder1/Analyse_sentiment_API/actions
- Render Logs : https://dashboard.render.com/services → Select service → Logs

---

## 📝 Checklists de déploiement

### Avant de déployer

- [ ] Tests locaux passent : `pytest -v`
- [ ] Pas d'erreurs d'import
- [ ] Code formaté correctement
- [ ] README à jour si changements notables
- [ ] requirements.txt à jour

### Après commit/push

- [ ] Vérifier GitHub Actions run
- [ ] Tests passent (vert ✅)
- [ ] NLTK bootstrap réussit
- [ ] Render redeploy lancé
- [ ] Attendre 2-5 min pour redeploy complet
- [ ] Tester l'API :

```bash
python test_api_manual.py https://analyse-sentiment-api.onrender.com
```

---

## 🧪 Vérifier le déploiement

### Health Check

```bash
curl https://analyse-sentiment-api.onrender.com/health
```

Doit retourner :
```json
{
  "status": "ok",
  "model_loaded": true,
  "vectorizer_loaded": true
}
```

### Tester endpoint /predict

```bash
curl -X POST https://analyse-sentiment-api.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "J'\''adore ce produit!"}'
```

### Swagger Documentation

Accès via https://analyse-sentiment-api.onrender.com/docs

---

## 🐛 Troubleshooting

### 1. Render service won't start

**Logs** : Vérifie https://dashboard.render.com/services → Logs

**Causes courantes** :
- Python version incompatible → Vérifie `runtime.txt`
- Dépendances manquantes → Vérifie `requirements.txt`
- Port non bindé → Vérifie `start.sh`

**Solutions** :
```bash
# Vérifier la version Python
cat runtime.txt  # Doit être 3.11.x

# Vérifier les dépendances localement
pip install -r requirements.txt

# Tester le start command localement
./start.sh
```

### 2. NLTK LookupError on Render

**Cause** : Corpora NLTK non téléchargés au startup

**Vérification** : Regarde logs Render pour "ensure_nltk_data()"

**Solution** : Fichier `startup_nltk.py` devrait le faire auto. Si erreur persiste :
1. Redéploie manuellement depuis Render dashboard
2. Attends le bootstrap NLTK complet
3. Teste `/health` endpoint

### 3. Model version mismatch warning

**Symptôme** : Warning scikit-learn sur la version (1.4.2 vs 1.3.2)

**Solution** : `requirements.txt` doit avoir `scikit-learn==1.4.2`

```bash
pip install scikit-learn==1.4.2
pip freeze > requirements.txt
git add requirements.txt && git commit -m "fix: update scikit-learn" && git push
```

### 4. API endpoint returns 500 error

**Vérification** :
1. Regarde les logs Render
2. Teste `/health` endpoint en premier
3. Vérifiés que les modèles sont présents dans `api_artifacts/`

**Solutions** :
```bash
# Test local de l'endpoint
python test_api_manual.py http://127.0.0.1:8000

# Inspect les artifacts
ls -la api_artifacts/
```

### 5. GitHub Actions fails

**Raison** : Tests échouent ou dépendances manquent

**Debug** :
1. Va sur https://github.com/Skeeder1/Analyse_sentiment_API/actions
2. Clique sur le run échoué
3. Développe les logs pour voir l'erreur
4. Corrige localement et repousse

---

## 📊 Monitoring

### Logs Render

```
Dashboard → Services → analyse-sentiment-api → Logs
```

Voir :
- Gunicorn start logs
- API requests
- Erreurs de démarrage

### Métriques

```
Dashboard → Services → analyse-sentiment-api → Metrics
```

Voir :
- CPU usage
- Memory usage
- Network I/O

---

## 🔄 Redéploiement manuel

Si besoin de redéployer sans push :

1. Va sur Render Dashboard
2. Sélectionne ton service
3. Clique sur **Manual Deploy** → **Deploy latest commit**

Ou via CLI :
```bash
# Depuis local
curl -X POST \
  -H "Authorization: Bearer $RENDER_API_KEY" \
  "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys"
```

---

## 🔐 Security

- ✅ Ne commit jamais `.env` (utilise `.env.example`)
- ✅ Garde `RENDER_API_KEY` secret dans GitHub Secrets
- ✅ Utilise HTTPS pour tous les appels API
- ✅ Valide les inputs utilisateur (FastAPI le fait)

---

## 📞 Support

- Logs Render : https://dashboard.render.com/services
- GitHub Actions : https://github.com/Skeeder1/Analyse_sentiment_API/actions
- Render Status : https://status.render.com
- Render Docs : https://render.com/docs

---

**Version** : 1.0  
**Last Updated** : 2025-10-18
