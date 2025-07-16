import os
from dotenv import load_dotenv
from src.application.graph import create_workflow

# Muat environment variables dari file .env
load_dotenv()
def main():
    # Validasi API keys
    if not os.getenv("TAVILY_API_KEY"):
        print("Error: Pastikan GOOGLE_APPLICATION_CREDENTIALS dan TAVILY_API_KEY sudah diatur di file .env")
        return

    # Membuat alur kerja (graph)
    app = create_workflow()

    # Mendapatkan input dari pengguna
    query = input("Masukkan pertanyaan Anda tentang analisis harga pengiriman: ")
    
    # Menjalankan alur kerja
    print("\n---🚀 MEMULAI ALUR KERJA ANALISIS PASAR---")
    inputs = {"initial_query": query}
    
    # `stream` bisa digunakan untuk melihat progres, `invoke` untuk hasil akhir
    final_state = app.invoke(inputs)

    # Menampilkan laporan akhir
    print("\n\n---📄 LAPORAN ANALISIS PASAR FINAL 📄---")
    print(final_state["final_report"])
    print("\n---🏁 ALUR KERJA SELESAI---")

if __name__ == "__main__":
    main()