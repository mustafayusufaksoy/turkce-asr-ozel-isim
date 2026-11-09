"""Turkish proper name correction for Whisper and WhisperX transcripts."""
from .core import (Lexicon, apply_candidates, correct, find_candidates, select_candidates,
                   spelling_key, turkish_lower)

__version__ = "0.1.0"
__all__ = ["Lexicon", "apply_candidates", "correct", "find_candidates", "select_candidates",
           "spelling_key", "turkish_lower"]
