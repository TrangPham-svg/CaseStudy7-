import os
import time
from datetime import datetime
from itertools import combinations
from typing import Dict, Any, List

# Import các thuật toán
from algorithms.preprocessing import preprocess_text
from algorithms.dp_levenshtein import similarity_dp
from algorithms.dc_shingling import similarity_shingling
from algorithms.bf_substring import similarity_brute

# ===================== CẤU HÌNH =====================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_FOLDER = os.path.join(CURRENT_DIR, "..", "data_test", "input")
OUTPUT_FOLDER = os.path.join(CURRENT_DIR, "..", "data_test", "output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

K_SHINGLE = 5  # Chuẩn công nghiệp cho văn bản tiếng Việt

# ===================== HÀM KẾT LUẬN ĐẠO VĂN =====================
def ket_luan_dao_van(shingling_percent: float, levenshtein_percent: float) -> str:
    """Tự động phán có đạo văn hay không - siêu trực quan khi demo"""
    if shingling_percent >= 70:
        return "ĐẠO VĂN RẤT NẶNG"
    elif shingling_percent >= 40:
        return "ĐẠO VĂN NẶNG"
    elif shingling_percent >= 20 or levenshtein_percent >= 40:
        return "CÓ DẤU HIỆU ĐẠO VĂO VĂN"
    elif shingling_percent >= 8 or levenshtein_percent >= 25:
        return "ĐẠO VĂN NHẸ"
    else:
        return "KHÔNG ĐẠO VĂN"

# ===================== ĐỌC TÀI LIỆU =====================
def load_documents() -> Dict[str, List[str]]:
    docs = {}
    if not os.path.exists(INPUT_FOLDER):
        print(f"LỖI: Không tìm thấy thư mục {INPUT_FOLDER}")
        return docs

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith('.txt'):
            path = os.path.join(INPUT_FOLDER, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    raw = f.read().strip()
                    tokens = preprocess_text(raw)
                    if len(tokens) > 0:
                        docs[filename] = tokens
                        print(f"Đã tải: {filename} ({len(tokens)} từ)")
                    else:
                        print(f"Cảnh báo: {filename} rỗng sau tiền xử lý")
            except Exception as e:
                print(f"Lỗi đọc {filename}: {e}")
    return docs

# ===================== CHẠY SO SÁNH MỘT CẶP =====================
def run_comparison(tokens_a: List[str], tokens_b: List[str], pair_name: str) -> Dict[str, Any]:
    print(f"\n{pair_name}")
    print("   " + "─" * 50)

    # 1. Quy hoạch động
    start = time.time()
    sim_dp, _ = similarity_dp(tokens_a, tokens_b)
    time_dp = time.time() - start

    # 2. Chia để trị
    start = time.time()
    sim_shingle, _ = similarity_shingling(tokens_a, tokens_b, K_SHINGLE)
    time_shingle = time.time() - start

    # 3. Vét cạn
    start = time.time()
    sim_bf, _ = similarity_brute(tokens_a, tokens_b)
    time_bf = time.time() - start

    # In kết quả đẹp
    print(f"   Quy hoạch động (Levenshtein)   : {sim_dp*100:6.2f}%  ({time_dp:.4f}s)")
    print(f"   Chia để trị (Shingling k={K_SHINGLE})     : {sim_shingle*100:6.2f}%  ({time_shingle:.4f}s)")
    print(f"   Vét cạn (Exact Substring)     : {sim_bf*100:6.2f}%  ({time_bf:.4f}s)")

    # TỰ ĐỘNG KẾT LUẬN
    ketluan = ket_luan_dao_van(sim_shingle*100, sim_dp*100)
    if "RẤT NẶNG" in ketluan:
        print(f"   KẾT LUẬN: {ketluan}")
    elif "NẶNG" in ketluan:
        print(f"   KẾT LUẬN: {ketluan}")
    elif "DẤU HIỆU" in ketluan or "NHẸ" in ketluan:
        print(f"   KẾT LUẬN: {ketluan}")
    else:
        print(f"   KẾT LUẬN: {ketluan}")

    print("   " + "─" * 50)
    return {
        "pair": pair_name,
        "levenshtein": sim_dp*100,
        "shingling": sim_shingle*100,
        "substring": sim_bf*100,
        "conclusion": ketluan,
        "times": [time_dp, time_shingle, time_bf]
    }

# ===================== MAIN =====================
def main():
    print("=" * 80)
    print("       PHÁT HIỆN ĐẠO VĂN THÔNG MINH - NHÓM X")
    print("   3 Chiến lược • Tự động kết luận • Hỗ trợ tiếng Việt")
    print("=" * 80)

    documents = load_documents()
    if len(documents) < 2:
        print("Cảnh báo: Cần ít nhất 2 file .txt trong thư mục data_test/input/")
        return

    print(f"\nTìm thấy {len(documents)} tài liệu. Bắt đầu so sánh mọi cặp...\n")

    all_results = []
    all_results.append("BÁO CÁO KẾT QUẢ PHÁT HIỆN ĐẠO VĂN")
    all_results.append(f"Thời gian chạy: {datetime.now().strftime('%d/%m/%Y lúc %H:%M:%S')}")
    all_results.append(f"Số tài liệu: {len(documents)}")
    all_results.append("="*80 + "\n")

    for (name1, tokens1), (name2, tokens2) in combinations(documents.items(), 2):
        pair_name = f"{name1} ↔ {name2}"
        result = run_comparison(tokens1, tokens2, pair_name)
        # Ghi vào file Markdown
        all_results.append(f"### {pair_name}")
        all_results.append(f"- Quy hoạch động: `{result['levenshtein']:.2f}%`")
        all_results.append(f"- Shingling + Jaccard: `{result['shingling']:.2f}%`")
        all_results.append(f"- Longest Exact Substring: `{result['substring']:.2f}%`")
        all_results.append(f"**Kết luận**: {result['conclusion']}")
        all_results.append("")

    # Ghi file output đẹp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(OUTPUT_FOLDER, f"BAOCAO_DAOVAN_{timestamp}.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(all_results))

    print("\n" + "="*80)
    print(f"HOÀN TẤT")
    print(f"Đã lưu báo cáo chi tiết tại:")
    print(f"   → {output_file}")
    print("="*80)

if __name__ == "__main__":
    main()
