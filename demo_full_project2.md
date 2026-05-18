# Demo Script – Project 2: Multi-Agent Search (CS 188)

---

## Q1 – Reflex Agent (4 điểm)

```bash
# Chạy thử tay trước
python pacman.py

# Xem Reflex Agent chơi
python pacman.py -p ReflexAgent

# Test trên layout đơn giản
python pacman.py -p ReflexAgent -l testClassic

# Test với 1 ma và 2 ma
python pacman.py --frameTime 0 -p ReflexAgent -k 1
python pacman.py --frameTime 0 -p ReflexAgent -k 2

# Chạy autograder (10 ván trên openClassic)
python autograder.py -q q1 --no-graphics
```

**Kết quả kỳ vọng:**
- Thắng ít nhất 5/10 ván → 1đ | Thắng 10/10 → 2đ
- Điểm trung bình > 500 → +1đ | > 1000 → +2đ

---

## Q2 – Minimax (5 điểm)

```bash
# Xem minimax chơi với depth 2 (mặc định)
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=2

# Kiểm tra giá trị minimax ở các depth khác nhau
# Depth 1→9, Depth 2→8, Depth 3→7, Depth 4→-492
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4

# Demo Pacman tự lao vào ma khi biết mình thua chắc
python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3

# Chạy autograder
python autograder.py -q q2 --no-graphics
```

**Điểm đáng chú ý:** Ở depth=4 trên minimaxClassic, Pacman sẽ chủ động lao vào ma gần nhất
vì nó nhận ra cái chết là không thể tránh và muốn kết thúc nhanh (tránh mất điểm sống).

---

## Q3 – Alpha-Beta Pruning (5 điểm)

```bash
# So sánh tốc độ: Alpha-Beta depth=3 nhanh tương đương Minimax depth=2
python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic

# Chạy autograder
python autograder.py -q q3 --no-graphics
```

**Kết quả kỳ vọng:** Cùng kết quả với Minimax nhưng nhanh hơn đáng kể.

---

## Q4 – Expectimax (5 điểm)

```bash
# Xem Expectimax chơi
python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3

# === DEMO SO SÁNH ẤN TƯỢNG NHẤT ===
# AlphaBeta: luôn thua vì coi ma là đối thủ tối ưu
python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10

# Expectimax: thắng ~50% vì biết ma đi ngẫu nhiên
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10

# Chạy autograder
python autograder.py -q q4 --no-graphics
```

**Kết quả kỳ vọng:** AlphaBeta thua 10/10, Expectimax thắng ~5/10.

---

## Q5 – Better Evaluation Function (6 điểm)

```bash
# Xem agent chơi với hàm đánh giá tốt hơn
python pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n 10

# Chạy autograder
python autograder.py -q q5 --no-graphics
```

**Kết quả kỳ vọng:**
- Thắng ít nhất 5/10 ván → +1đ | Thắng 10/10 → +2đ
- Điểm TB > 500 → +1đ | > 1000 → +2đ
- Mỗi ván < 30 giây → +1đ

---

## Thứ tự demo đề xuất cho buổi thuyết trình

| Bước | Lệnh | Mục đích |
|------|------|----------|
| 1 | `ReflexAgent -l testClassic` | Baseline đơn giản |
| 2 | `MinimaxAgent -l minimaxClassic -a depth=4` | Thấy Pacman "biết mình thua" |
| 3 | `AlphaBetaAgent -l trappedClassic -n 10` | AlphaBeta luôn thua |
| 4 | `ExpectimaxAgent -l trappedClassic -n 10` | Expectimax thắng ~50% ← điểm nhấn |
| 5 | `autograder.py -q q5 --no-graphics` | Kết quả điểm cuối |
