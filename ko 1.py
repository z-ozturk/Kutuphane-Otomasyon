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

def kitap_ekle():
    #kullanıcıdan kitap verileri alınır
    kitap_adi = input("Kitabın adını giriniz: ").strip()
    yazar_adi = input("Yazar adını giriniz: ").strip()
    yayin_evi = input("Yayın evini giriniz: ").strip()
    baski_yili = input("Baskı yılını giriniz: ").strip()

    #tüm bilgilerin girildiği doğrulanır
    if not all([kitap_adi, yazar_adi, yayin_evi, baski_yili]):
        print("Hata: Eksik bilgi girdiniz.")
        return
    
    veriler = [(kitap_adi, yazar_adi, yayin_evi, baski_yili)]

    try:
        with sql.connect('Liste2024.sqlite') as vt:    #veritabanına bağlanma
            im = vt.cursor()

            #tablo yoksa oluşturur
            im.execute("""
                CREATE TABLE IF NOT EXISTS 'Kitap Listesi' (
                       kitap_adi TEXT,
                       yazar_adi TEXT,
                       yayin_evi TEXT,
                       baski_yili TEXT
                )
            """)

            #kitap bilgilerini tabloya ekleme
            im.executemany("""INSERT INTO 'Kitap Listesi' VALUES (?, ?, ?, ?)""", veriler)
            vt.commit()   #değişiklikleri kaydetme
            print("Kitap başarıyla eklendi.")
    
    except sql.Error as e:        #hata yönetimi
        print(f"Veri tabanı hatası!: {e}")

def kitap_silme():

    try:
        with sql.connect('Liste2024.sqlite') as vt:     #veritabanına bağlanma
            im = vt.cursor()

            #kitap listesini görüntülüyoruz
            komut = """SELECT * FROM 'Kitap Listesi'"""
            im.execute(komut)
            for kitap in im:
                print(kitap)

            #kullanıcıdan sileceği kitabın adı alınır
            silinecek = input("silmek istediğiniz kitabı seçiniz: ")

            #eğer kullanıcı boş değer girerse hata mesajı verir
            if not silinecek.strip( ):
                print("Hata: Geçerli bir kitap adı giriniz.")
                return
            
            #veritabanından silme işlemi yapılır
            komut = "DELETE FROM 'Kitap Listesi' WHERE kitap_adi = ?"
            im.execute(komut, (silinecek,))
            vt.commit()
            
            #eğer silme işleminin etkilediği satır sayısı 0 ise, işlem yapılmamıştır.
            #yani o isimde kitap yoktur. hata mesajı döner
            if im.rowcount == 0:
                print("Hata: Silmek istediğiniz kitap bulunamadı.")
            else:
                print("Silme işlemi başarılı.")
    
    except sql.Error as e:     #hata yönetimi
        print(f"Hata!: {e}")
