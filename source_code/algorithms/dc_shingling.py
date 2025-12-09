from typing import List, Set, Tuple

def create_shingles(tokens: List[str], k: int = 5) -> Set[int]:
    """
    Tạo tập hợp hash của shingles (k-từ liên tiếp).
    k=5 là giá trị mặc định phù hợp cho văn bản ngắn/dài.
    """
    if len(tokens) < k:
        return set()
    shingles_hash = set()
    for i in range(len(tokens) - k + 1):
        shingle = tuple(tokens[i:i + k])
        shingles_hash.add(hash(shingle))
    return shingles_hash

def jaccard_similarity(shingles_a: Set[int], shingles_b: Set[int]) -> float:
    """
    Tính Jaccard Similarity: |intersection| / |union|.
    """
    if not shingles_a and not shingles_b:
        return 1.0
    intersection = len(shingles_a.intersection(shingles_b))
    union = len(shingles_a.union(shingles_b))
    return round(intersection / union if union > 0 else 0.0, 4)

def similarity_shingling(tokens_a: List[str], tokens_b: List[str], k: int = 5) -> Tuple[float, str]:
    """
    Tính độ tương đồng Shingling + Jaccard.
    Trả về (similarity, metric info).
    """
    shingles_a = create_shingles(tokens_a, k)
    shingles_b = create_shingles(tokens_b, k)
    sim = jaccard_similarity(shingles_a, shingles_b)
    return sim, f"Shingle k={k}"
