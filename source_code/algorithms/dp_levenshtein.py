from typing import List, Tuple

def levenshtein_distance(tokens_a: List[str], tokens_b: List[str]) -> int:
    """
    Tính khoảng cách Levenshtein (Edit Distance) trên tokens bằng quy hoạch động.
    """
    m, n = len(tokens_a), len(tokens_b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if tokens_a[i - 1] == tokens_b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # Xóa
                dp[i][j - 1] + 1,      # Chèn
                dp[i - 1][j - 1] + cost  # Thay thế/Giữ nguyên
            )

    return dp[m][n]

def similarity_dp(tokens_a: List[str], tokens_b: List[str]) -> Tuple[float, int]:
    """
    Tính độ tương đồng dựa trên Levenshtein (0.0 đến 1.0).
    Trả về (similarity, distance).
    """
    if not tokens_a and not tokens_b:
        return 1.0, 0
    distance = levenshtein_distance(tokens_a, tokens_b)
    max_len = max(len(tokens_a), len(tokens_b))
    similarity = 1.0 - (distance / max_len) if max_len > 0 else 1.0
    return round(similarity, 4), distance
