# services/embedding_model.py

from sentence_transformers import SentenceTransformer

_model = None

def get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(
            r"C:\Users\mykoffe\.cache\huggingface\hub\models--intfloat--multilingual-e5-small\snapshots\614241f622f53c4eeff9890bdc4f31cfecc418b3"
        )
    return _model
