from typing import List, Tuple

def longest_exact_substring_length(tokens_a: List[str], tokens_b: List[str]) -> int:
    """
    Tìm độ dài chuỗi con liên tiếp trùng khớp dài nhất bằng DP (tối ưu vét cạn).
    """
    m, n = len(tokens_a), len(tokens_b)
    max_len = 0
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if tokens_a[i - 1] == tokens_b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_len = max(max_len, dp[i][j])
            else:
                dp[i][j] = 0  # Reset cho substring liên tiếp

    return max_len

def similarity_brute(tokens_a: List[str], tokens_b: List[str]) -> Tuple[float, int]:
    """
    Tính độ tương đồng dựa trên longest exact substring.
    Trả về (similarity, max_length).
    """
    if not tokens_a or not tokens_b:
        return 0.0, 0
    max_len = longest_exact_substring_length(tokens_a, tokens_b)
    min_len = min(len(tokens_a), len(tokens_b))
    similarity = max_len / min_len if min_len > 0 else 0.0
    return round(similarity, 4), max_len
