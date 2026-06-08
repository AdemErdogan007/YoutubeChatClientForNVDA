# utils.py - Ortak Araçlar ve MANUEL Dil Yönetimi
# wxPython kütüphanesini arayüz çizimleri için içe aktarıyoruz.
import wx
# İşletim sistemi ve dosya yolu işlemleri için os modülünü içe aktarıyoruz.
import os
# JSON formatında veri okuma ve yazma için json modülünü içe aktarıyoruz.
import json
# Tarayıcıda web sayfası açmak için webbrowser modülünü içe aktarıyoruz.
import webbrowser
# Dosya kopyalama ve taşıma işlemleri için shutil modülünü içe aktarıyoruz.
import shutil
# NVDA'nın global değişkenlerine erişmek için globalVars modülünü içe aktarıyoruz.
import globalVars
# Python'un standart metin çeviri kütüphanesini içe aktarıyoruz.
import gettext
# NVDA'nın anlık dilini öğrenmek için languageHandler modülünü içe aktarıyoruz.
import languageHandler
# Tarih ve saat bilgilerini almak için datetime sınıfını içe aktarıyoruz.
from datetime import datetime

# Youtube API isteklerinin yapılacağı temel URL adresini sabit olarak tanımlıyoruz.
Youtube_Api_Temel_Adres = "https://www.googleapis.com/youtube/v3/"

# Eski ayar dosyasının bulunabileceği eklenti klasörü yolunu sabit olarak belirliyoruz.
Eski_Ayar_Dosyasi = os.path.join(os.path.dirname(__file__), "settings.json")
# Yeni ve güvenli ayar dosyasının yolunu (NVDA yapılandırma dizininde) belirliyoruz.
Ayar_Dosyasi = os.path.join(globalVars.appArgs.configPath, "YoutubeChatClient_Settings.json")

# Çeviri işlemini gerçekleştirecek olan metodumuzu tanımlıyoruz.
def _(Mesaj):
    # Hata oluşma ihtimaline karşı deneme bloğunu başlatıyoruz.
    try:
        # Çalışan mevcut dosyanın bulunduğu dizini tam yol olarak alıyoruz.
        Temel_Dizin = os.path.dirname(os.path.abspath(__file__))
        # İki üst klasöre çıkarak eklentinin ana dizinine ulaşıyoruz.
        Eklenti_Koku = os.path.abspath(os.path.join(Temel_Dizin, "..", ".."))
        # Dil dosyalarının barındırıldığı locale klasörünün yolunu oluşturuyoruz.
        Dil_Yolu = os.path.join(Eklenti_Koku, "locale")

        # NVDA üzerinden kullanıcının seçtiği geçerli dili öğreniyoruz.
        Gecerli_Dil = languageHandler.getLanguage()
        # Dil kodunun sadece ana dil kısmını (örneğin 'tr' veya 'en') ayırıyoruz.
        Ana_Dil = Gecerli_Dil.split('_')[0]
        
        # gettext nesnesini dil dosyalarını arayacak şekilde yapılandırıyoruz.
        Cevirmen = gettext.translation \
        (
            # NVDA'nın standart çeviri alanını belirtiyoruz.
            'nvda', 
            # Dil dosyalarının aranacağı dizini belirliyoruz.
            localedir=Dil_Yolu, 
            # Denenecek dilleri bir liste halinde veriyoruz.
            languages=[Gecerli_Dil, Ana_Dil], 
            # Çeviri bulunamazsa hata vermek yerine orijinal metne dönmesini sağlıyoruz.
            fallback=True
        )
        
        # Metni çevirip sonucu geri döndürüyoruz.
        return Cevirmen.gettext(Mesaj)
        
    # Eğer çeviri sırasında bir hata meydana gelirse yakalıyoruz.
    except Exception as Hata:
        # Orijinal metni hiçbir değişiklik yapmadan geri döndürüyoruz.
        return Mesaj

# Ayarları eski dizinden yeni NVDA yapılandırma dizinine taşıyan metot.
def Ayarlari_Kontrol_Et_Ve_Tasi():
    # Eğer eski dosya mevcutsa ve yeni dosya henüz oluşturulmamışsa taşıma işlemini başlatıyoruz.
    if os.path.exists(Eski_Ayar_Dosyasi) and not os.path.exists(Ayar_Dosyasi):
        # Taşıma işlemini hatasız gerçekleştirmeyi deniyoruz.
        try:
            # Eski dosyayı yeni dosya konumuna taşıyoruz.
            shutil.move(Eski_Ayar_Dosyasi, Ayar_Dosyasi)
        # Taşıma sırasında bir hata olursa diğer yöntemi deniyoruz.
        except:
            # Kopyalama işlemini hatasız gerçekleştirmeyi deniyoruz.
            try: 
                # Dosyayı yeni konuma kopyalıyoruz.
                shutil.copy2(Eski_Ayar_Dosyasi, Ayar_Dosyasi)
                # Başarılı olursa eski dosyayı siliyoruz.
                os.remove(Eski_Ayar_Dosyasi)
            # Kopyalama işleminde de hata olursa hiçbir şey yapmıyoruz.
            except: 
                # Hata durumunu yoksayıyoruz.
                pass

# Doküman dosyalarını (txt, html) okuyan ve içeriği döndüren metot.
def Dokuman_Dosyasi_Oku(Dosya_Adi):
    # Bulunulan dizinin yolunu alıyoruz.
    Temel_Yol = os.path.dirname(__file__)
    # Dokümanların bulunduğu doc klasörünün tam yolunu oluşturuyoruz.
    Dokuman_Koku = os.path.abspath(os.path.join(Temel_Yol, "..", "..", "doc"))
    # NVDA'nın güncel dilini alıyoruz.
    Gecerli_Dil = languageHandler.getLanguage()
    
    # Dilleri sırasıyla denemek için bir liste oluşturuyoruz.
    Denecek_Diller = \
    [
        # Tam dil kodunu ekliyoruz.
        Gecerli_Dil, 
        # Ana dil kodunu ekliyoruz.
        Gecerli_Dil.split('_')[0], 
        # Varsayılan İngilizce kodunu ekliyoruz.
        'en', 
        # Varsayılan Türkçe kodunu ekliyoruz.
        'tr'
    ]
    
    # Liste içindeki her bir dil için döngü başlatıyoruz.
    for Dil in Denecek_Diller:
        # O dile ait dosyanın tam yolunu oluşturuyoruz.
        Dosya_Yolu = os.path.join(Dokuman_Koku, Dil, Dosya_Adi)
        # Eğer belirtilen yolda böyle bir dosya varsa okuma işlemine geçiyoruz.
        if os.path.exists(Dosya_Yolu):
            # Okuma işlemini hatasız gerçekleştirmeyi deniyoruz.
            try:
                # Dosyayı UTF-8 formatında okuma modunda açıyoruz.
                with open(Dosya_Yolu, "r", encoding="utf-8") as Dosya:
                    # Dosyanın tüm içeriğini okuyup geri döndürüyoruz.
                    return Dosya.read()
            # Okuma sırasında bir hata meydana gelirse yakalıyoruz.
            except Exception as Hata: 
                # Hatayı kullanıcıya metin olarak geri döndürüyoruz.
                return f"Hata: {Hata}"
    
    # Hiçbir dilde dosya bulunamazsa hata mesajı döndürüyoruz.
    return f"Dosya bulunamadı: {Dosya_Adi}"

# Kullanım kılavuzunu (readme.html) tarayıcıda açan metot.
def Readme_Ac():
    # Bulunulan dizinin yolunu alıyoruz.
    Temel_Yol = os.path.dirname(__file__)
    # Dokümanların bulunduğu doc klasörünün tam yolunu oluşturuyoruz.
    Dokuman_Koku = os.path.abspath(os.path.join(Temel_Yol, "..", "..", "doc"))
    # NVDA'nın güncel dilini alıyoruz.
    Gecerli_Dil = languageHandler.getLanguage()
    
    # Dilleri sırasıyla denemek için bir liste oluşturuyoruz.
    Denecek_Diller = \
    [
        # Tam dil kodunu listeye ekliyoruz.
        Gecerli_Dil, 
        # Ana dil kodunu listeye ekliyoruz.
        Gecerli_Dil.split('_')[0], 
        # İngilizce varsayılanını listeye ekliyoruz.
        'en', 
        # Türkçe varsayılanını listeye ekliyoruz.
        'tr'
    ]
    
    # Liste içindeki her bir dil için döngü başlatıyoruz.
    for Dil in Denecek_Diller:
        # O dile ait readme dosyasının tam yolunu oluşturuyoruz.
        Dosya_Yolu = os.path.join(Dokuman_Koku, Dil, "readme.html")
        # Eğer belirtilen yolda böyle bir dosya varsa açma işlemine geçiyoruz.
        if os.path.exists(Dosya_Yolu):
            # Dosyayı varsayılan web tarayıcısında açıyoruz.
            webbrowser.open(f"file://{Dosya_Yolu}")
            # İşlem tamamlandığında metoddan çıkıyoruz.
            return

# Ayarları yapılandırma dosyasından okuyup yükleyen metot.
def Ayarlari_Yukle():
    # Eğer yeni dosya yoksa ve eski dosya varsa taşıma metodunu çağırıyoruz.
    if not os.path.exists(Ayar_Dosyasi) and os.path.exists(Eski_Ayar_Dosyasi):
        # Taşıma ve kontrol metodunu çalıştırıyoruz.
        Ayarlari_Kontrol_Et_Ve_Tasi()
    
    # Varsayılan ayar değerlerini içeren bir sözlük oluşturuyoruz.
    Varsayilan_Ayarlar = \
    { 
        # API anahtarını varsayılan olarak boş bırakıyoruz.
        "api_key": "", 
        # Otomatik okumayı varsayılan olarak açık bırakıyoruz.
        "auto_read": True, 
        # Yenileme hızını varsayılan olarak on saniye yapıyoruz.
        "refresh_rate": 10, 
        # Zaman damgasını varsayılan olarak kapalı tutuyoruz.
        "show_timestamp": False, 
        # Son mesaja odaklanmayı varsayılan olarak kapalı tutuyoruz.
        "focus_last": False 
    }
    
    # Eğer yeni ayar dosyası mevcutsa okuma işlemine geçiyoruz.
    if os.path.exists(Ayar_Dosyasi):
        # Okuma işlemini hatasız gerçekleştirmeyi deniyoruz.
        try:
            # Ayar dosyasını UTF-8 formatında okuma modunda açıyoruz.
            with open(Ayar_Dosyasi, "r", encoding="utf-8") as Dosya:
                # Okunan veriyi varsayılan ayarların üzerine yazarak geri döndürüyoruz.
                return {**Varsayilan_Ayarlar, **json.load(Dosya)}
        # Okuma sırasında bir hata meydana gelirse yakalıyoruz.
        except: 
            # Hatayı sistemin akışını bozmaması için yoksayıyoruz.
            pass
            
    # Hiçbir ayar dosyası okunamadıysa varsayılan ayarları döndürüyoruz.
    return Varsayilan_Ayarlar

# Ortak kullanılacak temel pencere sınıfını wx.Dialog üzerinden türetiyoruz.
class Temel_Pencere(wx.Dialog):
    # Sınıf başlatıldığında çalışacak yapıcı metodu tanımlıyoruz.
    def __init__(self, Ebeveyn, Baslik, Boyut):
        # Üst sınıfın yapıcı metodunu çağırarak pencere özelliklerini ayarlıyoruz.
        super(Temel_Pencere, self).__init__ \
        (
            # Pencerenin ait olduğu ebeveyn nesneyi belirtiyoruz.
            Ebeveyn, 
            # Pencere başlığını ayarlıyoruz.
            title=Baslik, 
            # Pencere boyutlarını belirliyoruz.
            size=Boyut, 
            # Pencere stillerini ve standart erişilebilirlik düğmelerini (küçült, büyüt) ekliyoruz.
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX
        )
        # Oluşturulan pencereyi ekranın ortasında açılacak şekilde hizalıyoruz.
        self.Center()

    # Telif hakkı metnini pencereye ekleyen metodumuzu tanımlıyoruz.
    def Telif_Hakkini_Ekle(self, Boyutlandirici, Panel):
        # Pencerenin altına diğer içeriklerden ayırmak için statik bir çizgi ekliyoruz.
        Boyutlandirici.Add(wx.StaticLine(Panel), 0, wx.EXPAND | wx.ALL, 5)
        # Sistemin mevcut yıl bilgisini alıyoruz.
        Guncel_Yil = datetime.now().year
        # Yazılımın ilk yayınlanma yılı olan temel yılı belirliyoruz.
        Temel_Yil = 2025
        # Telif hakkı yılı için mevcut duruma göre metin oluşturuyoruz.
        Yil_Metni = str(Temel_Yil) if Guncel_Yil <= Temel_Yil else f"{Temel_Yil} / {Guncel_Yil}"
        # Telif hakkı bilgisini içeren ve çevirisi yapılmış metni oluşturuyoruz.
        Telif_Metni = _("Copyright © {year}, ADEM ERDOĞAN (ERDOĞAN TEKNOLOJİ VE PROGRAMCILIK)").format(year=Yil_Metni)
        # Telif hakkı bilgisini tıklanabilir bir erişilebilir buton olarak tasarlıyoruz.
        Telif_Butonu = wx.Button(Panel, label=Telif_Metni)
        # Butona tıklandığında geliştiricinin web sitesini açacak olayı bağlıyoruz.
        Telif_Butonu.Bind(wx.EVT_BUTTON, lambda Olay: webbrowser.open("https://erdoganteknoloji.com.tr/"))
        # Oluşturulan butonu pencerenin esnek boyutlandırıcısına ekliyoruz.
        Boyutlandirici.Add(Telif_Butonu, 0, wx.EXPAND | wx.ALL, 2)