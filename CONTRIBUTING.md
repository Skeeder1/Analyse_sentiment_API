# 🤝 Contributing Guide

Merci de contribuer au projet Sentiment Analysis API !

---

## 📝 Avant de commencer

- Lis le [README.md](./README.md) pour comprendre l'architecture
- Crée un [virtual environment](#virtual-environment)
- Consulte ce guide pour les conventions

---

## 🔧 Setup développement

### Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Linux / macOS
source venv/bin/activate
```

### Installation dépendances

```bash
pip install -r requirements.txt
```

### Lancer les tests

```bash
pytest -v
```

### Lancer l'API localement

```bash
uvicorn src.api_analyse.main:app --reload
```

---

## 📋 Workflow Git

### 1. Créer une branche

```bash
git checkout -b feature/ma-feature
# ou
git checkout -b fix/mon-bug
```

### 2. Faire des commits clairs

```bash
git commit -m "feat: ajouter nouvelle fonctionnalité"
git commit -m "fix: corriger bug X"
git commit -m "docs: mettre à jour README"
git commit -m "test: ajouter tests pour Y"
```

**Format** : `<type>: <description courte>`

Types acceptés :
- `feat` : Nouvelle fonctionnalité
- `fix` : Correction de bug
- `docs` : Documentation
- `test` : Tests
- `refactor` : Refactoring code
- `perf` : Amélioration performance
- `chore` : Maintenance, dépendances

### 3. Push et Pull Request

```bash
git push origin feature/ma-feature
```

Crée une PR sur GitHub avec :
- Description claire du changement
- Références aux issues liées (ex: "Closes #42")
- Tests passants (`pytest -v`)

---

## 🧪 Tests

### Lancer tous les tests

```bash
pytest -v
```

### Tester un endpoint spécifique

```bash
pytest tests/test_api.py::test_predict -v
```

### Vérifier la couverture

```bash
pytest --cov=src tests/ -v
```

**Obligation** : Tous les nouveaux code doit avoir un test !

---

## 💻 Code Style

### Format Python

Respect :
- **PEP 8** pour le style
- **Line length** : max 120 caractères
- **Docstrings** : format standard Python

Exemple :
```python
def predict(text: str) -> dict:
    """
    Predict sentiment of input text.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        dict: {sentiment, confidence, probability_positive, probability_negative}
        
    Raises:
        ValueError: If text is empty
    """
    if not text.strip():
        raise ValueError("Text cannot be empty")
    
    # Implementation...
```

### Imports

Organisation :
```python
# 1. Standard library
import json
from pathlib import Path

# 2. Third-party
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# 3. Local
from src.api_analyse.preprocess import preprocess_text
```

---

## 📦 Ajouter une dépendance

### Installation locale

```bash
pip install nom_package==version
```

### Update requirements.txt

```bash
pip freeze > requirements.txt
```

### Commit

```bash
git add requirements.txt
git commit -m "feat: add nom_package==version"
```

---

## 🚀 Déploiement

Une fois la PR merged sur `main` :

1. **GitHub Actions** exécute les tests
2. **Si tests ✅** → déclenche redéploiement Render
3. **Render** redéploie automatiquement

Logs accessibles :
- GitHub : https://github.com/Skeeder1/Analyse_sentiment_API/actions
- Render : https://dashboard.render.com/services

---

## 📖 Documentation

### Mettre à jour le README

Si tu ajoutes/modifies une fonctionnalité :
- Mets à jour la section pertinente du [README.md](./README.md)
- Ajoute des exemples de code si applicable

### Docstrings de code

Tous les fonctions/classes publiques doivent avoir une docstring :

```python
def ma_fonction(param1: str, param2: int) -> bool:
    """
    Description courte.
    
    Description longue si nécessaire (optionnel).
    
    Args:
        param1: Description du paramètre
        param2: Description du paramètre
        
    Returns:
        Description de la valeur retournée
        
    Raises:
        ExceptionType: Description quand levée
    """
    pass
```

---

## 🐛 Reporting Bugs

Ouvre une GitHub issue avec :
- **Titre clair** : "Bug: description"
- **Description** : Problème rencontré
- **Reproduction** : Étapes pour reproduire
- **Logs/Screenshots** : Si applicable

---

## ❓ Questions ?

- Ouvre une [Discussion](https://github.com/Skeeder1/Analyse_sentiment_API/discussions)
- Consulte la section [Troubleshooting](./README.md#-troubleshooting) du README

---

Merci pour ta contribution ! 🎉
