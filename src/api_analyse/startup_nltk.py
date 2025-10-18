import os
import nltk
from pathlib import Path

# Paquets NLTK requis par le prétraitement
_PKGS = ["wordnet", "omw-1.4", "stopwords", "punkt"]

def _paths():
    # Honore NLTK_DATA si présent, sinon dossier du projet
    base = os.getenv("NLTK_DATA", str(Path(__file__).resolve().parents[1] / "nltk_data"))
    Path(base).mkdir(parents=True, exist_ok=True)
    # Injecte le chemin en tête
    if base not in nltk.data.path:
        nltk.data.path.insert(0, base)
    return base

def _exists(pkg: str) -> bool:
    # punkt est un tokenizer, les autres sont des corpora
    key = f"tokenizers/{pkg}" if pkg == "punkt" else f"corpora/{pkg}"
    try:
        nltk.data.find(key)
        return True
    except LookupError:
        return False

def ensure_nltk_data() -> None:
    _paths()
    for pkg in _PKGS:
        if not _exists(pkg):
            nltk.download(pkg, quiet=True)
