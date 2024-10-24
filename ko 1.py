import sqlite3 as sql

def veritabani_sorgusu(veritabani, tablo):
    try:
        vt = sql.connect(veritabani)  # veritabanına bağlanma
        im = vt.cursor()  # veritabanı üzerinde işlem oluşturmak için kullanılır.

        komut = f"SELECT * FROM '{tablo}'"
        im.execute(komut)

        #verileri yazdırma
        for veri in im:  
            print(veri)
    except sql.Error as e:        #Hata yönetimi
        print(f"veritabani hatasi!: {e}")
    finally:
        vt.close()     #bağlantıyı kapatma

def kitap_goster():
    
    print("Kitap Listesi\n")
    veritabani_sorgusu('Liste2024.sqlite', 'Kitap Listesi')

    print("Ödünç Verilmiş Kitaplar\n")
    veritabani_sorgusu('oduncverilmis.sqlite', 'Ödünç Listesi')
