from __future__ import annotations


def char_ngrams(text: str, n: int = 5) -> set[str]:
    if len(text) < n:
        return {text} if text else set()
    return {text[i : i + n] for i in range(len(text) - n + 1)}


def jaccard_similarity(a: str, b: str, n: int = 5) -> float:
    sa = char_ngrams(a, n=n)
    sb = char_ngrams(b, n=n)
    if not sa and not sb:
        return 1.0
    union = sa | sb
    if not union:
        return 0.0
    return len(sa & sb) / len(union)


def is_contaminated(candidate: str, references: list[str], threshold: float = 0.82) -> bool:
    return any(jaccard_similarity(candidate, ref) >= threshold for ref in references)
