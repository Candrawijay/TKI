import streamlit as st
from processing import cari_resep_berdasarkan_judul, highlight_title_html

st.set_page_config(page_title="Cari Resep", layout="wide")

st.title("🍲 Sistem Pencarian Resep")
st.markdown("Masukkan kata kunci berdasarkan **judul resep** (contoh: _ayam goreng_, _udang bakar_)")

query = st.text_input("🔍 Kata kunci resep:")

if query:
    hasil = cari_resep_berdasarkan_judul(query, top_n=5)
    if hasil.empty:
        st.warning("❌ Tidak ditemukan resep yang cocok.")
    else:
        query_words = query.lower().split()
        hasil["Title"] = hasil["Title"].apply(lambda x: highlight_title_html(x, query_words))
        hasil["Skor Kemiripan"] = hasil["Skor Kemiripan"].round(4)
        hasil_terpilih = hasil[["Title", "kategori", "Skor Kemiripan", "Ingredients"]]

        # Tampilkan dalam format HTML
        st.write("### ✨ Hasil Pencarian:")
        st.write(hasil_terpilih.to_html(escape=False, index=False), unsafe_allow_html=True)
