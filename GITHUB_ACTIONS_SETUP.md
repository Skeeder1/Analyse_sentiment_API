# 🔐 Configuration des Secrets GitHub Actions

Pour que le workflow de déploiement automatique fonctionne, tu dois ajouter deux secrets dans GitHub :

## Étapes de configuration :

### 1. Obtenir les clés depuis Render

**Pour `RENDER_SERVICE_ID` :**
- Va sur https://dashboard.render.com
- Sélectionne ton service "analyse-sentiment-api"
- L'ID du service est visible dans l'URL : `https://dashboard.render.com/services/<SERVICE_ID>`
- Ou dans l'onglet "Settings" → "ID"

**Pour `RENDER_API_KEY` :**
- Va sur https://dashboard.render.com/account/api-tokens
- Crée une nouvelle clé API ("New API Key")
- Copie la clé (elle ne s'affichera qu'une seule fois!)

### 2. Ajouter les secrets GitHub

1. Va sur ton repository : https://github.com/Skeeder1/Analyse_sentiment_API
2. Clique sur **Settings** → **Secrets and variables** → **Actions**
3. Clique sur **New repository secret**
4. Ajoute les deux secrets :

| Secret Name | Valeur |
|---|---|
| `RENDER_SERVICE_ID` | L'ID de ton service Render |
| `RENDER_API_KEY` | Ta clé API Render |

### 3. Vérifier la configuration

Une fois les secrets ajoutés :
- Va à l'onglet **Actions** de ton repo
- Tu verras le workflow "CI/CD - Test & Deploy to Render"
- À chaque `git push` sur `main`, le workflow va :
  1. ✅ Exécuter les tests (pytest)
  2. ✅ Vérifier le bootstrap NLTK
  3. ✅ Déclencher le redéploiement sur Render
  4. ✅ Vérifier que le serveur répond

### 4. Tester le déploiement automatique

Fais un simple commit et push :
```powershell
git add .
git commit -m "test: trigger GitHub Actions workflow"
git push
```

Regarde les logs dans l'onglet **Actions** pour voir le déploiement en action ! 🚀

---

## 📊 Structure du Workflow

```
┌─────────────────────────────────────────┐
│  Git Push to 'main'                     │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  JOB: test (ubuntu-latest)              │
│  - Install Python 3.11                  │
│  - pip install -r requirements.txt      │
│  - pytest -v                            │
│  - python tests/test_nltk_boot.py       │
└──────────────┬──────────────────────────┘
               │
               ▼ (si tests ✅)
┌─────────────────────────────────────────┐
│  JOB: deploy                            │
│  - curl → Render API                    │
│  - Trigger redeploy                     │
│  - Wait 10s                             │
│  - Check health endpoint (retry 30x)    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  ✅ Render redeploy triggered           │
│  API updated automatically              │
└─────────────────────────────────────────┘
```

---

## 🛠️ Dépannage

**Le workflow n'est pas déclenché ?**
- Vérifie que tu pushes sur la branche `main`
- Va à l'onglet **Actions** et regarde les logs

**Le déploiement échoue avec erreur API ?**
- Vérifie que `RENDER_SERVICE_ID` et `RENDER_API_KEY` sont corrects
- La clé API doit être valide et non expirée

**Les tests échouent ?**
- Le déploiement ne sera pas déclenché si les tests échouent
- Corrige les tests d'abord avant de repousser

**Le redéploiement ne se termine pas ?**
- Render peut prendre 2-5 minutes pour redéployer
- Le workflow attend jusqu'à 150 secondes (30 tentatives × 5s)
