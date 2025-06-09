from processing import cari_resep_berdasarkan_judul, highlight_title_html
from IPython.display import display, HTML

while True:
    print("\n=== Sistem Pencarian Resep ===")
    query_user = input("Masukkan kata kunci judul (contoh: ayam goreng): ").strip()

    if query_user.lower() in ['exit', 'quit', 'keluar']:
        print("👋 Terima kasih telah menggunakan sistem pencarian resep!")
        break

    hasil = cari_resep_berdasarkan_judul(query_user, top_n=5)

    if hasil.empty:
        print("❌ Tidak ditemukan resep yang cocok.")
    else:
        query_words = query_user.lower().split()
        hasil["Title"] = hasil["Title"].apply(lambda x: highlight_title_html(x, query_words))
        hasil["Skor Kemiripan"] = hasil["Skor Kemiripan"].round(4)
        hasil_terpilih = hasil[["Title", "kategori", "Skor Kemiripan", "Ingredients"]]
        display(HTML(hasil_terpilih.to_html(escape=False, index=False)))
