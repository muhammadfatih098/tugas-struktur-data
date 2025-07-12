import csv
from datetime import datetime

# ==== CONFIGURASI ====
CSV_FILE = 'keuangan.csv'

# ==== HASHMAP KATEGORI ====
kategori_map = {
    'Gaji': 'Pemasukan',
    'Bonus': 'Pemasukan',
    'Investasi': 'Pemasukan',
    'Makanan': 'Pengeluaran',
    'Transportasi': 'Pengeluaran',
    'Hiburan': 'Pengeluaran',
    'Belanja': 'Pengeluaran',
    'Tagihan': 'Pengeluaran'
}

def get_jenis(kategori):
    return kategori_map.get(kategori, 'Tidak Diketahui')

# ==== FUNGSI CSV ====
def load_data():
    data = []
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['Jumlah'] = int(row['Jumlah'])
                data.append(row)
    except FileNotFoundError:
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Tanggal', 'Kategori', 'Jenis', 'Jumlah', 'Catatan'])
    return data

def save_data(data):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['Tanggal', 'Kategori', 'Jenis', 'Jumlah', 'Catatan']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# ==== CRUD ====
def tambah_transaksi(data):
    tanggal = input("Masukkan tanggal (YYYY-MM-DD): ")
    kategori = input("Masukkan kategori: ")
    jenis = get_jenis(kategori)
    if jenis == 'Tidak Diketahui':
        print("❌ Kategori tidak dikenal.")
        return
    try:
        jumlah = int(input("Masukkan jumlah: "))
    except ValueError:
        print("❌ Jumlah harus angka.")
        return
    catatan = input("Catatan (opsional): ")

    data.append({
        'Tanggal': tanggal,
        'Kategori': kategori,
        'Jenis': jenis,
        'Jumlah': jumlah,
        'Catatan': catatan
    })
    print("✅ Transaksi berhasil ditambahkan!")

def tampilkan_data(data):
    if not data:
        print("Data masih kosong.")
        return
    print("\n===== DAFTAR TRANSAKSI =====")
    for i, row in enumerate(data, start=1):
        print(f"{i}. {row['Tanggal']} | {row['Kategori']} | {row['Jenis']} | Rp{row['Jumlah']} | {row['Catatan']}")

def edit_transaksi(data):
    tampilkan_data(data)
    if not data:
        return
    try:
        indeks = int(input("Masukkan nomor transaksi yang ingin diedit: ")) - 1
        if indeks < 0 or indeks >= len(data):
            print("❌ Nomor tidak valid.")
            return

        transaksi = data[indeks]
        print(f"\nTransaksi lama: {transaksi}")

        tanggal = input(f"Tanggal baru [{transaksi['Tanggal']}]: ") or transaksi['Tanggal']
        kategori = input(f"Kategori baru [{transaksi['Kategori']}]: ") or transaksi['Kategori']
        jenis = get_jenis(kategori)
        jumlah_input = input(f"Jumlah baru [{transaksi['Jumlah']}]: ")
        jumlah = int(jumlah_input) if jumlah_input else transaksi['Jumlah']
        catatan = input(f"Catatan baru [{transaksi['Catatan']}]: ") or transaksi['Catatan']

        data[indeks] = {
            'Tanggal': tanggal,
            'Kategori': kategori,
            'Jenis': jenis,
            'Jumlah': jumlah,
            'Catatan': catatan
        }
        print("✅ Transaksi berhasil diperbarui!")

    except ValueError:
        print("❌ Input harus berupa angka.")

def hapus_transaksi(data):
    tampilkan_data(data)
    if not data:
        return
    try:
        indeks = int(input("Masukkan nomor transaksi yang ingin dihapus: ")) - 1
        if indeks < 0 or indeks >= len(data):
            print("❌ Nomor tidak valid.")
            return

        konfirmasi = input("Apakah Anda yakin ingin menghapus transaksi ini? (y/n): ")
        if konfirmasi.lower() == 'y':
            data.pop(indeks)
            print("✅ Transaksi berhasil dihapus.")
        else:
            print("❌ Penghapusan dibatalkan.")

    except ValueError:
        print("❌ Input harus berupa angka.")

# ==== MENU UTAMA ====
def menu_utama():
    data = load_data()
    while True:
        print("\n===== APLIKASI MANAJEMEN KEUANGAN =====")
        print("1. Tambah Transaksi")
        print("2. Lihat Semua Transaksi")
        print("3. Edit Transaksi")
        print("4. Hapus Transaksi")
        print("5. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            tambah_transaksi(data)
            save_data(data)
        elif pilihan == '2':
            tampilkan_data(data)
        elif pilihan == '3':
            edit_transaksi(data)
            save_data(data)
        elif pilihan == '4':
            hapus_transaksi(data)
            save_data(data)
        elif pilihan == '5':
            print("👋 Keluar dari aplikasi.")
            break
        else:
            print("❌ Pilihan tidak valid!")

# ==== JALANKAN PROGRAM ====
if __name__ == "__main__":
    menu_utama()
