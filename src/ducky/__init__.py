from .main import *

try:
    import nltk
    nltk.download('punkt', quiet=True)
except Exception:
    pass
