"""
PERBANDINGAN ALGORITMA PENCARIAN (SEARCH ALGORITHM)
Mata Kuliah : Kecerdasan Buatan

Masalah : mencari jalur dari S (start) ke G (goal) pada labirin grid.
          '#' = dinding, '~' = rawa (biaya 5), '.' = jalan biasa (biaya 1)

Algoritma:
  Uninformed : BFS, DFS, UCS (Uniform Cost Search)
  Informed   : Greedy Best-First Search, A* (heuristik Manhattan)
"""

import heapq
import time
from collections import deque

# ---------------------------------------------------------------
# 1. DEFINISI MASALAH (state space)
# ---------------------------------------------------------------
LABIRIN = [
    "S...#.........",
    ".##.#.#######.",
    ".#..#.#.....#.",
    ".#.##.#.###.#.",
    ".#....#.#~#.#.",
    ".######.#~#.#.",
    "......#.#.#...",
    ".####.#.#.####",
    ".#....#...~..G",
    ".#.#########.#",
    "...~~~~......."
]

BIAYA = {".": 1, "~": 5, "S": 1, "G": 1}
ARAH = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # atas, bawah, kiri, kanan


def cari_posisi(simbol):
    for r, baris in enumerate(LABIRIN):
        if simbol in baris:
            return (r, baris.index(simbol))


START, GOAL = cari_posisi("S"), cari_posisi("G")


def tetangga(state):
    """Fungsi successor: kembalikan (state_baru, biaya_langkah)."""
    r, c = state
    for dr, dc in ARAH:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(LABIRIN) and 0 <= nc < len(LABIRIN[0]):
            sel = LABIRIN[nr][nc]
            if sel != "#":
                yield (nr, nc), BIAYA[sel]


def heuristik(state):
    """Jarak Manhattan ke goal (admissible, karena biaya minimum = 1)."""
    return abs(state[0] - GOAL[0]) + abs(state[1] - GOAL[1])


def rekonstruksi(induk, state):
    jalur = []
    while state is not None:
        jalur.append(state)
        state = induk[state]
    return jalur[::-1]


def hitung_biaya(jalur):
    return sum(BIAYA[LABIRIN[r][c]] for r, c in jalur[1:])


# ---------------------------------------------------------------
# 2. ALGORITMA PENCARIAN
#    Setiap fungsi mengembalikan (jalur, jumlah_node_diperluas, urutan_dikunjungi)
# ---------------------------------------------------------------
def bfs():
    frontier = deque([START])
    induk = {START: None}
    dikunjungi = []
    while frontier:
        state = frontier.popleft()          # FIFO
        dikunjungi.append(state)
        if state == GOAL:
            return rekonstruksi(induk, state), len(dikunjungi), dikunjungi
        for nxt, _ in tetangga(state):
            if nxt not in induk:
                induk[nxt] = state
                frontier.append(nxt)
    return None, len(dikunjungi), dikunjungi


def dfs():
    frontier = [START]
    induk = {START: None}
    dikunjungi = []
    selesai = set()
    while frontier:
        state = frontier.pop()              # LIFO
        if state in selesai:
            continue
        selesai.add(state)
        dikunjungi.append(state)
        if state == GOAL:
            return rekonstruksi(induk, state), len(dikunjungi), dikunjungi
        for nxt, _ in tetangga(state):
            if nxt not in selesai:
                induk[nxt] = state
                frontier.append(nxt)
    return None, len(dikunjungi), dikunjungi


def best_first(f):
    """Kerangka umum untuk UCS, Greedy, dan A*. f(g, state) = prioritas."""
    frontier = [(f(0, START), 0, START)]
    induk = {START: None}
    g_terbaik = {START: 0}
    dikunjungi = []
    selesai = set()
    while frontier:
        _, g, state = heapq.heappop(frontier)
        if state in selesai:
            continue
        selesai.add(state)
        dikunjungi.append(state)
        if state == GOAL:
            return rekonstruksi(induk, state), len(dikunjungi), dikunjungi
        for nxt, biaya in tetangga(state):
            g_baru = g + biaya
            if nxt not in g_terbaik or g_baru < g_terbaik[nxt]:
                g_terbaik[nxt] = g_baru
                induk[nxt] = state
                heapq.heappush(frontier, (f(g_baru, nxt), g_baru, nxt))
    return None, len(dikunjungi), dikunjungi


def ucs():
    return best_first(lambda g, s: g)                  # f(n) = g(n)


def greedy():
    return best_first(lambda g, s: heuristik(s))       # f(n) = h(n)


def a_star():
    return best_first(lambda g, s: g + heuristik(s))   # f(n) = g(n) + h(n)


# ---------------------------------------------------------------
# 3. VISUALISASI & PERBANDINGAN
# ---------------------------------------------------------------
def gambar(jalur, dikunjungi):
    """Tampilkan labirin: '*' = jalur akhir, 'o' = node yang dieksplorasi."""
    peta = [list(baris) for baris in LABIRIN]
    for r, c in dikunjungi:
        if peta[r][c] in ".~":
            peta[r][c] = "o"
    if jalur:
        for r, c in jalur:
            if peta[r][c] not in "SG":
                peta[r][c] = "*"
    return "\n".join("  " + "".join(baris) for baris in peta)


def jalankan(nama, fungsi, tampil_peta=True):
    t0 = time.perf_counter()
    jalur, diperluas, dikunjungi = fungsi()
    waktu = (time.perf_counter() - t0) * 1000

    print(f"\n=== {nama} ===")
    if jalur is None:
        print("  Jalur tidak ditemukan.")
    else:
        print(f"  Panjang jalur : {len(jalur) - 1} langkah")
        print(f"  Total biaya   : {hitung_biaya(jalur)}")
    print(f"  Node diperluas: {diperluas}")
    print(f"  Waktu         : {waktu:.3f} ms")
    if tampil_peta:
        print(gambar(jalur, dikunjungi))

    return nama, (len(jalur) - 1 if jalur else None), \
        (hitung_biaya(jalur) if jalur else None), diperluas


def main():
    print("LABIRIN (S=start, G=goal, #=dinding, ~=rawa biaya 5)")
    print("\n".join("  " + b for b in LABIRIN))

    algoritma = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("UCS", ucs),
        ("Greedy Best-First", greedy),
        ("A* (Manhattan)", a_star),
    ]
    ringkasan = [jalankan(n, f) for n, f in algoritma]

    print("\n" + "=" * 60)
    print(f"{'Algoritma':<20}{'Langkah':>9}{'Biaya':>9}{'Node':>10}")
    print("-" * 60)
    for nama, langkah, biaya, node in ringkasan:
        print(f"{nama:<20}{langkah:>9}{biaya:>9}{node:>10}")
    print("=" * 60)
    print("Catatan:")
    print(" - BFS optimal untuk jumlah langkah, tetapi mengabaikan biaya rawa.")
    print(" - UCS dan A* optimal untuk total biaya; A* biasanya lebih hemat node.")
    print(" - Greedy cepat tetapi tidak menjamin jalur optimal.")
    print(" - DFS tidak menjamin optimal dan jalurnya bisa sangat panjang.")


if __name__ == "__main__":
    main()
