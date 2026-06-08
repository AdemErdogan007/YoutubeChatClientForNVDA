# Main_Window.py - Ana Sohbet Ekranı
# Kullanıcı arayüz bileşenlerini oluşturmak için wxPython kütüphanesini dahil ediyoruz.
import wx
# JSON verilerini işlemek, ayrıştırmak ve metne dökmek için json modülünü ekliyoruz.
import json
# Canlı sohbet verilerini arka planda akışı engellemeden çekmek için threading modülünü ekliyoruz.
import threading
# Zaman gecikmeleri ve uyku modları uygulamak için time modülünü dahil ediyoruz.
import time
# YouTube API'sine HTTP istekleri göndermek için urllib.request modülünü ekliyoruz.
import urllib.request
# URL adreslerini ayrıştırmak ve parametreleri okumak için urllib.parse modülünü ekliyoruz.
import urllib.parse
# Gelen sohbet mesajlarını NVDA üzerinden seslendirmek için speech modülünü ekliyoruz.
import speech
# Kullanıcıya bilgi mesajları ve uyarılar göstermek için NVDA ui modülünü dahil ediyoruz.
import ui
# Eklenti bilgilerine ve manifest verilerine erişmek için addonHandler modülünü ekliyoruz.
import addonHandler
# Web sitelerini varsayılan tarayıcıda açabilmek için webbrowser modülünü dahil ediyoruz.
import webbrowser
# Ortak temel sınıfı, ayar yükleme fonksiyonunu, temel API adresini ve çeviri aracını utils modülünden alıyoruz.
from .utils import Temel_Pencere, Ayarlari_Yukle, Youtube_Api_Temel_Adres, Readme_Ac, _
# Ayarlar penceresini çağırabilmek için ilgili sınıfı içe aktarıyoruz.
from .Settings_Window import Ayarlar_Penceresi
# Sürüm geçmişi ekranını açabilmek için ilgili diyalog sınıfını içe aktarıyoruz.
from .Version_History_Window import Surum_Gecmisi_Penceresi
# API rehberi penceresini açabilmek için ilgili rehber sınıfını içe aktarıyoruz.
from .How_to_Use_Window import Api_Rehberi_Penceresi
# Eklenti hakkında ekranını açabilmek için ilgili hakkında sınıfını içe aktarıyoruz.
from .About_Window import Eklenti_Hakkinda_Penceresi

# YouTube canlı sohbet akışını yönetecek olan ana pencere sınıfımızı tanımlıyoruz.
class Youtube_Canli_Sohbet_Penceresi(Temel_Pencere):
    # Sınıf başlatıldığında otomatik çalışacak olan yapıcı metodu kuruyoruz.
    def __init__(self, Ebeveyn):
        # Hata kontrol bloğu altında eklenti sürüm bilgisini almaya çalışıyoruz.
        try:
            # Eklentinin manifest dosyasında yazılı olan güncel sürüm numarasını çekiyoruz.
            Surum_Bilgisi = addonHandler.getCodeAddon().manifest.get("version", "1.6")
        # Eğer sürüm bilgisi alınırken bir hata oluşursa yakalıyoruz.
        except:
            # Hata durumunda varsayılan sürüm değerini el ile atıyoruz.
            Surum_Bilgisi = "1.6"
        
        # Üst sınıfın yapıcı metodunu çağırarak pencere başlığına sürüm numarasını yerleştirip boyutunu (550x700) veriyoruz.
        super(Youtube_Canli_Sohbet_Penceresi, self).__init__ \
        (
            # Ebeveyn pencere nesnesini iletiyoruz.
            Ebeveyn, 
            # Pencere başlığını dinamik sürüm numarası ile çeviri fonksiyonundan geçirerek oluşturuyoruz.
            _("Youtube Canlı Sohbet İstemcisi - v{version}").format(version=Surum_Bilgisi), 
            # Pencerenin genişlik ve yüksekliğini piksel cinsinden belirliyoruz.
            (550, 700)
        )
        
        # Sohbet akışının aktif olup olmadığını kontrol eden mantıksal değişkeni başlangıçta kapalı yapıyoruz.
        self.Akis_Devam_Ediyor = False
        # YouTube API'sinden bir sonraki sayfa verisini isteyebilmek için gerekli belirteci boş bırakıyoruz.
        self.Sonraki_Sayfa_Isareti = None
        # Aynı mesajların ekranda mükerrer olarak gösterilmesini engellemek için boş bir küme oluşturuyoruz.
        self.Son_Mesajlar_Kumesi = set()
        # Kullanıcının kaydettiği güncel eklenti ayarlarını yapılandırma dosyasından yüklüyoruz.
        self.Ayarlar_Sozlugu = Ayarlari_Yukle()
        # Pencerenin görsel arayüz elemanlarını inşa eden metodumuzu çağırıyoruz.
        self.Arayuzu_Olustur()

    # Dosyadaki ayarları dinamik olarak yenilemek için ara metodumuzu tanımlıyoruz.
    def Mevcut_Ayarlari_Getir(self):
        # utils içerisindeki ayar yükleme fonksiyonunu tetikleyip sonucunu döndürüyoruz.
        return Ayarlari_Yukle()

    # Pencere içindeki tüm görsel arayüz elemanlarını yerleştiren ana metot.
    def Arayuzu_Olustur(self):
        # Görsel bileşenlerin üzerine dizileceği ana paneli oluşturuyoruz.
        Panel_Nesnesi = wx.Panel(self)
        # Bileşenleri dikey hiyerarşide alt alta dizmesi için ana bir kutu düzenleyici tanımlıyoruz.
        Dikey_Kutu = wx.BoxSizer(wx.VERTICAL)

        # En üst menü buton alanı için yatay bir kutu düzenleyici oluşturuyoruz.
        Yatay_Kutu_Ust = wx.BoxSizer(wx.HORIZONTAL)
        # Butonu sağ tarafa yaslamak için sol tarafa esnek boşluk yerleştiriyoruz.
        Yatay_Kutu_Ust.AddStretchSpacer()
        # Diğer alt pencerelere erişim sağlayacak seçenekler butonunu üretiyoruz.
        self.Secenekler_Butonu = wx.Button(Panel_Nesnesi, label=_("Seçenekler"))
        # Seçenekler butonuna tıklandığında açılır menüyü tetikleyecek olayı bağlıyoruz.
        self.Secenekler_Butonu.Bind(wx.EVT_BUTTON, self.Secenekler_Menusunu_Goster)
        # Butonu yatay kutunun içerisine 5 piksel dış boşluk bırakarak ekliyoruz.
        Yatay_Kutu_Ust.Add(self.Secenekler_Butonu, 0, wx.ALL, 5)
        # Hazırlanan üst yatay kutuyu ana dikey düzenleyiciye dahil ediyoruz.
        Dikey_Kutu.Add(Yatay_Kutu_Ust, 0, wx.EXPAND)

        # URL giriş kutusunun üzerine açıklayıcı bir statik metin etiketi yerleştiriyoruz.
        Dikey_Kutu.Add(wx.StaticText(Panel_Nesnesi, label=_("YouTube Canlı Yayın URL'si:")), 0, wx.EXPAND | wx.ALL, 5)
        # Kullanıcının YouTube linkini yapıştıracağı metin giriş kutusunu üretiyoruz.
        self.Yayin_Adresi_Kutusu = wx.TextCtrl(Panel_Nesnesi)
        # Metin kutusunu dikey düzene yayılacak şekilde ve 5 piksel dış boşlukla ekliyoruz.
        Dikey_Kutu.Add(self.Yayin_Adresi_Kutusu, 0, wx.EXPAND | wx.ALL, 5)

        # Akış kontrol butonlarını yan yana yerleştirmek için yatay bir kutu düzenleyici kuruyoruz.
        Yatay_Kutu_Butonlar = wx.BoxSizer(wx.HORIZONTAL)
        # Canlı sohbeti başlatma görevini yapacak olan butonu üretiyoruz.
        self.Baslat_Butonu = wx.Button(Panel_Nesnesi, label=_("Sohbet Akışını Başlat"))
        # Canlı sohbet akışını durduracak olan ikinci kontrol butonunu üretiyoruz.
        self.Durdur_Butonu = wx.Button(Panel_Nesnesi, label=_("Sohbet Akışını Durdur"))
        # Akış henüz başlamadığı için durdurma butonunu başlangıçta pasif yapıyoruz.
        self.Durdur_Butonu.Disable()
        # Başlat butonuna tıklandığında akış başlatma fonksiyonunu çalıştıracak olayı bağlıyoruz.
        self.Baslat_Butonu.Bind(wx.EVT_BUTTON, self.Akisi_Baslat)
        # Durdur butonuna tıklandığında akış durdurma fonksiyonunu tetikleyecek olayı bağlıyoruz.
        self.Durdur_Butonu.Bind(wx.EVT_BUTTON, self.Akisi_Durdur)
        
        # Başlat butonunu yatay düzene eşit pay alacak şekilde ekliyoruz.
        Yatay_Kutu_Butonlar.Add(self.Baslat_Butonu, 1, wx.ALL, 5)
        # Durdur butonunu yatay düzene eşit oranda pay alacak şekilde dahil ediyoruz.
        Yatay_Kutu_Butonlar.Add(self.Durdur_Butonu, 1, wx.ALL, 5)
        # Butonların bulunduğu yatay kutuyu ana dikey düzenleyici listesine ekliyoruz.
        Dikey_Kutu.Add(Yatay_Kutu_Butonlar, 0, wx.EXPAND | wx.ALL, 5)

        # Sohbet listesinin üzerinde duracak olan açıklayıcı statik metni ekliyoruz.
        Dikey_Kutu.Add(wx.StaticText(Panel_Nesnesi, label=_("Sohbet Akışı:")), 0, wx.EXPAND | wx.ALL, 5)
        # Mesajların listeleneceği, tekli seçime uygun ve yatay kaydırma çubuklu liste kutusunu üretiyoruz.
        self.Sohbet_Liste_Kutusu = wx.ListBox(Panel_Nesnesi, style=wx.LB_SINGLE | wx.HSCROLL)
        # Liste kutusunu pencerede en büyük alanı kaplayacak (oran=1) esneklikte dikey kutuya ekliyoruz.
        Dikey_Kutu.Add(self.Sohbet_Liste_Kutusu, 1, wx.EXPAND | wx.ALL, 5)

        # Alt kısımda anlık bağlantı durumunu bildirecek olan statik metin alanını üretiyoruz.
        self.Durum_Metni = wx.StaticText(Panel_Nesnesi, label=_("Hazır."))
        # Durum metnini dikey kutunun alt sınırına yerleştiriyoruz.
        Dikey_Kutu.Add(self.Durum_Metni, 0, wx.EXPAND | wx.ALL, 5)
        
        # utils'ten gelen telif hakkı buton bileşenini formun en altına entegre ediyoruz.
        self.Telif_Hakkini_Ekle(Dikey_Kutu, Panel_Nesnesi)
        # Hazırlanan tüm dikey yerleşim sitemini panel nesnesinin sizer kuralı yapıyoruz.
        Panel_Nesnesi.SetSizer(Dikey_Kutu)
        # Klavyeden basılan tuşları yakalamak için tüm pencere düzeyinde tuş kancası olayını bağlıyoruz.
        self.Bind(wx.EVT_CHAR_HOOK, self.Penceyi_Kapat_Klavye)

    # Seçenekler butonuna basıldığında ekrana açılır popup menü çıkaran metot.
    def Secenekler_Menusunu_Goster(self, Olay):
        # wxPython popup menü nesnesini hafızada örnekliyoruz.
        Menu_Nesnesi = wx.Menu()
        # Menüye Ayarlar öğesini ekliyoruz.
        Oge_Ayarlar = Menu_Nesnesi.Append(wx.ID_ANY, _("Ayarlar"))
        # Ayarlar öğesine tıklandığında ayar penceresini modal açacak fonksiyonu bağlıyoruz.
        self.Bind(wx.EVT_MENU, lambda Eylem: self.Pencereyi_Modal_Ac(Ayarlar_Penceresi), Oge_Ayarlar)

        # Menüye Sürüm Geçmişi öğesini dahil ediyoruz.
        Oge_Gecmis = Menu_Nesnesi.Append(wx.ID_ANY, _("Sürüm Geçmişi"))
        # Sürüm geçmişi tıklandığında ilgili geçmiş penceresini tetikleyecek fonksiyonu bağlıyoruz.
        self.Bind(wx.EVT_MENU, lambda Eylem: self.Pencereyi_Modal_Ac(Surum_Gecmisi_Penceresi), Oge_Gecmis)

        # Menüye Nasıl Kullanılır? rehber link öğesini ekliyoruz.
        Oge_Kullanim = Menu_Nesnesi.Append(wx.ID_ANY, _("Nasıl Kullanılır?"))
        # Tıklanma durumunda yerel yardım dosyasını tarayıcıda açacak metodu bağlıyoruz.
        self.Bind(wx.EVT_MENU, lambda Eylem: Readme_Ac(), Oge_Kullanim)

        # Menüye API Anahtarı Nasıl Alınır? rehber pencere öğesini ekliyoruz.
        Oge_Rehber = Menu_Nesnesi.Append(wx.ID_ANY, _("API Anahtarı Nasıl Alınır?"))
        # Tıklanma durumunda API kılavuz diyalogunu çağıracak fonksiyonu bağlıyoruz.
        self.Bind(wx.EVT_MENU, lambda Eylem: self.Pencereyi_Modal_Ac(Api_Rehberi_Penceresi), Oge_Rehber)

        # Menüye Eklenti Hakkında diyalog öğesini ekliyoruz.
        Oge_Hakkinda = Menu_Nesnesi.Append(wx.ID_ANY, _("Eklenti Hakkında"))
        # Tıklanma durumunda hakkında penceresini açacak lambda fonksiyonunu bağlıyoruz.
        self.Bind(wx.EVT_MENU, lambda Eylem: self.Pencereyi_Modal_Ac(Eklenti_Hakkinda_Penceresi), Oge_Hakkinda)

        # Menüye web sitesi dış bağlantı öğesini ekliyoruz.
        Oge_Web = Menu_Nesnesi.Append(wx.ID_ANY, _("Web Sitesini Ziyaret Et"))
        # Tıklanma durumunda geliştiricinin web sitesini tarayıcıya gönderecek olayı bağlıyoruz.
        self.Bind(wx.EVT_MENU, lambda Eylem: webbrowser.open("https://erdoganteknoloji.com.tr/"), Oge_Web)
        
        # Oluşturulan popup menüyü butonun hemen altında ekranda gösteriyoruz.
        self.PopupMenu(Menu_Nesnesi)
        # Menü kapandıktan sonra hafızadan güvenle temizliyoruz.
        Menu_Nesnesi.Destroy()

    # Gönderilen pencere sınıfını modal (öncelikli kilitli) modda açan metot.
    def Pencereyi_Modal_Ac(self, Pencere_Sinifi):
        # İlgili pencere sınıfından mevcut pencereyi ebeveyn göstererek yeni bir nesne türetiyoruz.
        Diyalog_Nesnesi = Pencere_Sinifi(self)
        # Diyalog penceresini modal olarak açıp kullanıcının işlem yapmasını bekliyoruz.
        Diyalog_Nesnesi.ShowModal()
        # İşlem bittiğinde pencere nesnesini bellekten siliyoruz.
        Diyalog_Nesnesi.Destroy()
        # Eğer kapatılan pencere Ayarlar ise, değişen yeni ayarları anlık olarak hafızaya tekrar yüklüyoruz.
        if Pencere_Sinifi == Ayarlar_Penceresi:
            # Sınıf içi ayar sözlüğünü güncel veriler ile yeniliyoruz.
            self.Ayarlar_Sozlugu = self.Mevcut_Ayarlari_Getir()

    # Klavyeden basılan Escape (ESC) tuşu ile pencereyi kapatmayı sağlayan metot.
    def Penceyi_Kapat_Klavye(self, Olay):
        # Basılan tuş kodunun Escape tuşu olup olmadığını kontrol ediyoruz.
        if Olay.GetKeyCode() == wx.WXK_ESCAPE:
            # Eğer ESC tuşuna basıldıysa mevcut pencereyi kapatıp yok ediyoruz.
            self.Destroy()
        # Başka bir tuşa basıldıysa işlemin sistemce devam etmesine izin veriyoruz.
        else:
            # Olayı bir sonraki işlemciye devrediyoruz.
            Olay.Skip()

    # Başlat butonuna basıldığında HTTP akış zincirini kuran tetikleyici metot.
    def Akisi_Baslat(self, Olay):
        # Güncel eklenti ayarlarını dosyadan yeniden çekiyoruz.
        self.Ayarlar_Sozlugu = self.Mevcut_Ayarlari_Getir()
        # Ayarlar içerisinden API anahtarını alıp kenar boşluklarını temizliyoruz.
        Api_Anahtari = self.Ayarlar_Sozlugu.get("api_key", "").strip()
        # Kullanıcının yapıştırdığı YouTube canlı yayın adresini kutudan okuyoruz.
        Yayin_Adresi = self.Yayin_Adresi_Kutusu.GetValue().strip()
        
        # Eğer sistemde kayıtlı bir API anahtarı yoksa akışı başlatmıyoruz.
        if not Api_Anahtari:
            # Ekran okuyucu ve ekran aracılığıyla API anahtarının eksik olduğunu bildiriyoruz.
            ui.message(_("API Anahtarı eksik. Lütfen ayarlardan giriniz."))
            # Metodun çalışmasını burada kesiyoruz.
            return
        
        # Verilen URL adresinden YouTube video kimliğini (ID) ayıklıyoruz.
        Video_Kimligi = self.Video_Kimligini_Al(Yayin_Adresi)
        # Eğer adres boşsa veya video kimliği tespit edilemediyse hata veriyoruz.
        if not Yayin_Adresi or not Video_Kimligi:
            # Geçersiz adres uyarısını kullanıcıya iletiyoruz.
            ui.message(_("Geçersiz YouTube URL'si."))
            # Metodun yürütülmesini durduruyoruz.
            return

        # Akış kontrol durumunu aktif (True) hale getiriyoruz.
        self.Akis_Devam_Ediyor = True
        # Yeni akış başladığı için başlat butonunu pasif konuma alıyoruz.
        self.Baslat_Butonu.Disable()
        # Akışı kesebilmek adına durdurma butonunu aktif hale getiriyoruz.
        self.Durdur_Butonu.Enable()
        # Sohbet listesinin içerisindeki eski tüm mesajları temizliyoruz.
        self.Sohbet_Liste_Kutusu.Clear()
        # Eski mesaj hafıza kümesini tamamen sıfırlıyoruz.
        self.Son_Mesajlar_Kumesi.clear()
        # Sayfalama belirtecini ilk istek için boş (None) yapıyoruz.
        self.Sonraki_Sayfa_Isareti = None
        # Ayarlardan gelen istek periyodu süresini alıyoruz (Yoksa varsayılan 10 saniye).
        Yenileme_Hizi = self.Ayarlar_Sozlugu.get("refresh_rate", 10)
        # Arayüzün kilitlenmesini önlemek için API sorgularını arka planda yapacak bir iş parçacığı (Thread) başlatıyoruz.
        threading.Thread \
        (
            # Hedef işçi fonksiyonu olarak ilgili metodumuzu gösteriyoruz.
            target=self.Arka_Plan_Is_Parcacigi, 
            # Fonksiyona gerekli parametreleri bir demet (tuple) halinde gönderiyoruz.
            args=(Api_Anahtari, Video_Kimligi, Yenileme_Hizi), 
            # NVDA kapandığında bu thread'in de otomatik sonlanması için daemon modunu aktif yapıyoruz.
            daemon=True
        ).start()

    # Durdur butonuna tıklandığında veri çekme döngüsünü kıran metot.
    def Akisi_Durdur(self, Olay):
        # Arka plandaki while döngüsünün kırılması için kontrol değişkenini False yapıyoruz.
        self.Akis_Devam_Ediyor = False
        # Başlat butonunu tekrar tıklanabilir hale getiriyoruz.
        self.Baslat_Butonu.Enable()
        # Durdurma butonunu görevini tamamladığı için pasif yapıyoruz.
        self.Durdur_Butonu.Disable()
        # Durum metnini güvenli arayüz döngüsü içinde 'Durduruldu' olarak güncelliyoruz.
        wx.CallAfter(self.Durum_Metni.SetLabel, _("Durduruldu."))

    # Gönderilen YouTube URL adresinden video ID'sini regex yerine string analizi ile ayıklayan metot.
    def Video_Kimligini_Al(self, Adres):
        # URL adresini bileşenlerine ayırmak için parse fonksiyonunu kullanıyoruz.
        Sorgu_Sonucu = urllib.parse.urlparse(Adres)
        # Eğer kısa paylaşım alanı olan 'youtu.be' ise video ID yolun ilk elemanıdır.
        if Sorgu_Sonucu.hostname == 'youtu.be': 
            # İlk eğik çizgiden sonrasını kimlik olarak geri döndürüyoruz.
            return Sorgu_Sonucu.path[1:]
        # Standart veya masaüstü YouTube alan adları kontrol ediliyor.
        if Sorgu_Sonucu.hostname in ('www.youtube.com', 'youtube.com'):
            # Eğer standart izleme sayfası ise 'v' sorgu parametresini okuyoruz.
            if Sorgu_Sonucu.path == '/watch': 
                # Sorgu metni içindeki 'v' anahtarının ilk değerini alıp döndürüyoruz.
                return urllib.parse.parse_qs(Sorgu_Sonucu.query).get('v', [None])[0]
            # Eğer gömülü (embed) video formatında bir adres ise parçalayarak alıyoruz.
            if Sorgu_Sonucu.path[:7] == '/embed/': 
                # Eğik çizgiye göre bölüp üçüncü sıradaki video ID'sini döndürüyoruz.
                return Sorgu_Sonucu.path.split('/')[2]
            # Alternatif yaş kısıtlamalı yönlendirme URL formatı kontrol ediliyor.
            if Sorgu_Sonucu.path[:3] == '/v/': 
                # Adres yolunu bölüp ilgili video kimlik indexini döndürüyoruz.
                return Sorgu_Sonucu.path.split('/')[2]
        # Hiçbiri eşleşmezse geçersiz video olarak boş değer döndürüyoruz.
        return None

    # Arka planda bağımsız çalışan ve periyodik sorguları yöneten iş parçacığı fonksiyonu.
    def Arka_Plan_Is_Parcacigi(self, Api_Anahtari, Video_Kimligi, Bekleme_Suresi):
        # Durum çubuğuna 'Bağlanıyor...' bilgisini emniyetli olarak yazdırıyoruz.
        wx.CallAfter(self.Durum_Metni.SetLabel, _("Bağlanıyor..."))
        # Videoya ait aktif canlı sohbet kanal kimliğini (Chat ID) çekiyoruz.
        Sohbet_Kanal_Kimligi = self.Canli_Sohbet_Kimligini_Getir(Api_Anahtari, Video_Kimligi)
        # Eğer canlı sohbet kimliği bulunamadıysa (yayın yoksa veya sohbet kapalıysa) duruyoruz.
        if not Sohbet_Kanal_Kimligi:
            # Kullanıcıya canlı sohbetin bulunamadığı uyarısını arayüz döngüsünde gösteriyoruz.
            wx.CallAfter(ui.message, _("Canlı sohbet bulunamadı."))
            # Akışı kapatmak için durdurma eylemini tetikliyoruz.
            wx.CallAfter(self.Akisi_Durdur, None)
            # İş parçacığından çıkış yapıyoruz.
            return
        
        # Sohbet başarıyla tespit edildiyse durum mesajını güncelliyoruz.
        wx.CallAfter(self.Durum_Metni.SetLabel, _("Sohbet Bağlandı."))
        # Kullanıcı durdur butonuna basmadığı sürece dönecek olan ana döngü.
        while self.Akis_Devam_Ediyor:
            # İsteklerin ağ hatası ile çökmemesi için hata kontrol bloğu açıyoruz.
            try:
                # Sohbet mesajlarını API üzerinden çeken fonksiyonu çağırıyoruz.
                self.Sohbet_Mesajlarini_Cek(Api_Anahtari, Sohbet_Kanal_Kimligi)
                # Ayarlarda belirlenen süre boyunca iş parçacığını uyku moduna alıyoruz.
                time.sleep(Bekleme_Suresi)
            # İstek sırasında bir internet kesintisi veya hata meydana gelirse yakalıyoruz.
            except Exception as Hata:
                # Ağ hatası durumunda YouTube sunucusunu yormamak adına bekleme süresini iki katına çıkarıp uyuyoruz.
                time.sleep(Bekleme_Suresi * 2)

    # YouTube API kullanarak video detaylarından canlı sohbet ID'sini çeken metot.
    def Canli_Sohbet_Kimligini_Getir(self, Api_Anahtari, Video_Kimligi):
        # İstek atılacak olan YouTube API video endpoint adresini parametrelerle hazırlıyoruz.
        Istek_Adresi = f"{Youtube_Api_Temel_Adres}videos?part=liveStreamingDetails&id={Video_Kimligi}&key={Api_Anahtari}"
        # Kullanıcı verilerini korumak amacıyla bağlantıyı hata olasılığına karşı korumalı blokta açıyoruz.
        try:
            # HTTP isteğini gönderiyor ve yanıt nesnesini alıyoruz.
            with urllib.request.urlopen(Istek_Adresi) as Yanit:
                # Gelen veriyi okuyor ve UTF-8 formatında çözüp JSON nesnesine dönüştürüyoruz.
                Veri = json.loads(Yanit.read().decode('utf-8'))
                # JSON ağacından 'items' listesini çekiyoruz.
                Elemanlar = Veri.get("items", [])
                # Eğer liste doluysa canlı yayın detaylarındaki 'activeLiveChatId' verisini döndürüyoruz.
                if Elemanlar: 
                    # Aktif sohbet ID değerini sözlükten ayıklayıp geri yolluyoruz.
                    return Elemanlar[0].get("liveStreamingDetails", {}).get("activeLiveChatId")
        # Herhangi bir bağlantı veya yetki hatası olursa yakalıyoruz.
        except: 
            # Hata durumunda geriye boş değer döndürüyoruz.
            pass
        # Sohbet kimliği alınamazsa varsayılan boş değer dönüyor.
        return None

    # Canlı sohbet odasındaki yeni mesajları çeken ve listeleyen kritik fonksiyon.
    def Sohbet_Mesajlarini_Cek(self, Api_Anahtari, Sohbet_Kanal_Kimligi):
        # Mesaj listeleme API endpoint adresini kanal kimliği ve API anahtarı ile birleştiriyoruz.
        Istek_Adresi = f"{Youtube_Api_Temel_Adres}liveChat/messages?liveChatId={Sohbet_Kanal_Kimligi}&part=snippet,authorDetails&key={Api_Anahtari}"
        # Eğer bir sonraki sayfa imleci (Page Token) mevcutsa bunu da istek adresine parametre ekliyoruz.
        if self.Sonraki_Sayfa_Isareti: 
            # Adrese sayfa imlecini iliştiriyoruz.
            Istek_Adresi += f"&pageToken={self.Sonraki_Sayfa_Isareti}"
        
        # Ağ bağlantı okuma işlemlerini korumalı blok içerisine alıyoruz.
        try:
            # Sunucuya HTTP bağlantısı açıyoruz.
            with urllib.request.urlopen(Istek_Adresi) as Yanit:
                # Gelen veriyi UTF-8 ile çözüp JSON olarak hafızaya alıyoruz.
                Veri = json.loads(Yanit.read().decode('utf-8'))
                # Bir sonraki isteklerde mükerrerliği önleyecek yeni sayfa token bilgisini güncelliyoruz.
                self.Sonraki_Sayfa_Isareti = Veri.get("nextPageToken")
                # Yeni gelen mesaj metinlerini biriktirmek için boş bir geçici liste açıyoruz.
                Yeni_Mesajlar_Listesi = []
                # Ayarlardan zaman damgası gösterim tercihini okuyoruz.
                Zamani_Goster = self.Ayarlar_Sozlugu.get("show_timestamp", False)

                # Gelen JSON verisindeki her bir mesaj öğesi için döngü başlatıyoruz.
                for Oge in Veri.get("items", []):
                    # Eğer bu mesaj ID'si daha önce işlenmiş mesajlar kümesinde yoksa yeni kabul ediyoruz.
                    if Oge["id"] not in self.Son_Mesajlar_Kumesi:
                        # Mesajın içerik detaylarını barındıran snippet bölümünü alıyoruz.
                        Icerik_Detayi = Oge["snippet"]
                        # Mesajı gönderen kullanıcının görünen adını alıyoruz.
                        Yazar_Adi = Oge["authorDetails"]["displayName"]
                        # Gönderilen mesajın YouTube tarafındaki yapısal türünü (text, superchat vb.) alıyoruz.
                        Mesaj_Turu = Icerik_Detayi.get("type")
                        # Mesajın yayınlanma saatini string içerisinden saat:dakika:saniye olarak kırpıyoruz.
                        Saat_Metni = Icerik_Detayi["publishedAt"][11:19]
                        # Ekrana basılacak ana metin değişkenini boş olarak hazırlıyoruz.
                        Gorunen_Metin = ""
                        # Özel etkinlikler için (Üyelik, Süper Chat) ön ek etiket değişkeni açıyoruz.
                        On_Ek = ""

                        # Eğer normal bir yazılı sohbet mesajı ise çalışacak şart.
                        if Mesaj_Turu == "textMessageEvent": 
                            # Görünen sohbet metnini doğrudan değişkene aktarıyoruz.
                            Gorunen_Metin = Icerik_Detayi.get("displayMessage", "")
                        # Eğer bağış içeren bir Süper Chat etkinliği ise çalışacak şart.
                        elif Mesaj_Turu == "superChatEvent":
                            # Süper Chat bağış detay nesnesini çekiyoruz.
                            Detay = Icerik_Detayi.get("superChatDetails", {})
                            # Bağış miktarını ve para birimini ön ek etiketi olarak hazırlıyoruz.
                            On_Ek = f"[SUPER CHAT {Detay.get('amountDisplayString', '')}]"
                            # Bağışçının yazdığı yorum metnini alıyoruz.
                            Gorunen_Metin = Detay.get("userComment", "")
                        # Eğer çıkartma içeren bir Süper Sticker etkinliği ise çalışacak şart.
                        elif Mesaj_Turu == "superStickerEvent":
                            # Çıkartma detay nesnesini çekiyoruz.
                            Detay = Icerik_Detayi.get("superStickerDetails", {})
                            # Çıkartma miktarını ön ek etiketine yazıyoruz.
                            On_Ek = f"[SUPER STICKER {Detay.get('amountDisplayString', '')}]"
                            # Çıkartmanın alternatif metin açıklamasını okuyoruz.
                            Gorunen_Metin = Detay.get("superStickerMetadata", {}).get("altText", "Sticker")
                        # Eğer kanala yeni katılan bir üyelik etkinliği ise çalışacak şart.
                        elif Mesaj_Turu == "newSponsorEvent":
                            # Görünen mesajı sistemden alıyor veya varsayılan Türkçe karşılığını yazıyoruz.
                            Gorunen_Metin = Icerik_Detayi.get("displayMessage", _("Yeni Üye Oldu!"))
                            # Üyelik ön ek etiketini yerelleştirilmiş olarak atıyoruz.
                            On_Ek = _("[YENİ ÜYELİK]")
                        # Eğer eski bir üyenin aylık üyelik yenileme kutlaması ise çalışacak şart.
                        elif Mesaj_Turu == "memberMilestoneChatEvent":
                            # Üyelik dönüm noktası detaylarını alıyoruz.
                            Detay = Icerik_Detayi.get("memberMilestoneChatDetails", {})
                            # Kaçıncı ay dönümü olduğunu ön ek etiketine dinamik yerleştirip çeviriyoruz.
                            On_Ek = _("[ÜYELİK {month}. AY]").format(month=Detay.get('memberMonth', '?'))
                            # Üyenin kutlama mesajını veya sistem otomatik metnini alıyoruz.
                            Gorunen_Metin = Detay.get("userComment", "") or Icerik_Detayi.get("displayMessage", "")

                        # Eğer hiçbir türe girmediyse ve boş kaldıysa genel ekran mesajını yedek olarak alıyoruz.
                        if not Gorunen_Metin and not On_Ek: 
                            # Sistem mesaj içeriğini ekrana basılacak metin yapıyoruz.
                            Gorunen_Metin = Icerik_Detayi.get("displayMessage", "")

                        # Zaman damgası ayarı açık ise mesajın başına saat bilgisini ekliyoruz.
                        if Zamani_Goster: 
                            # Saat, etiket, yazar ve mesaj metnini birleştirip son hali veriyoruz.
                            Nihai_Mesaj = f"[{Saat_Metni}] {On_Ek} {Yazar_Adi}: {Gorunen_Metin}"
                        # Zaman damgası kapalı ise saat bilgisi olmadan birleştiriyoruz.
                        else: 
                            # Etiket, yazar ve mesaj metnini birleştirerek son hali oluşturuyoruz.
                            Nihai_Mesaj = f"{On_Ek} {Yazar_Adi}: {Gorunen_Metin}"

                        # Oluşturulan tam mesaj satırını geçici biriktirme listesine ekliyoruz.
                        Yeni_Mesajlar_Listesi.append(Nihai_Mesaj)
                        # Mesajın benzersiz ID'sini mükerrer olmaması için hafıza kümesine kaydediyoruz.
                        self.Son_Mesajlar_Kumesi.add(Oge["id"])
                
                # Eğer döngü sonucunda listeye en az bir tane yeni mesaj eklendiyse ekranı güncellemeye yolluyoruz.
                if Yeni_Mesajlar_Listesi: 
                    # Arayüz elemanlarını güncellemek için listeyi CallAfter ile güvenli metoda gönderiyoruz.
                    wx.CallAfter(self.Arayuz_Listesini_Guncelle, Yeni_Mesajlar_Listesi)
        # Olası okuma hatalarında sistemin kırılmaması için boş geçiyoruz.
        except: 
            # Akışı bozmamak adına hatayı yoksayıyoruz.
            pass

    # Gelen yeni mesaj listesini ekrandaki ListBox elemanına yazan ve seslendiren metot.
    def Arayuz_Listesini_Guncelle(self, Gelen_Mesajlar):
        # Liste kutusunun içerisindeki toplam mevcut eleman sayısını alıyoruz.
        Mevcut_Eleman_Sayisi = self.Sohbet_Liste_Kutusu.GetCount()
        # Kullanıcının şu an listede seçmiş olduğu satır indeksini öğreniyoruz.
        Secili_Indeks = self.Sohbet_Liste_Kutusu.GetSelection()
        # Kullanıcının listenin en altında olup olmadığını veya hiçbir şey seçmediğini kontrol ediyoruz.
        En_Altta_Mi = (Secili_Indeks == Mevcut_Eleman_Sayisi - 1) or (Secili_Indeks == wx.NOT_FOUND)
        # Ayarlardan zorunlu son mesaja odaklanma kuralının durumunu okuyoruz.
        Zorunlu_Odak = self.Ayarlar_Sozlugu.get("focus_last", False)
        # Ayarlardan yeni mesajları seslendirme tercihini okuyoruz.
        Otomatik_Seslendir = self.Ayarlar_Sozlugu.get("auto_read", True)

        # Gelen her bir yeni mesaj satırı için döngü çalıştırıyoruz.
        for Tek_Mesaj in Gelen_Mesajlar:
            # Mesaj metnini ekrandaki liste kutusunun sonuna satır olarak ekliyoruz.
            self.Sohbet_Liste_Kutusu.Append(Tek_Mesaj)
            # Eğer otomatik seslendirme ayarı aktifse mesajı NVDA konuşma motoruna gönderiyoruz.
            if Otomatik_Seslendir: 
                # Mesajı ekran okuyucunun konuşma diliyle seslendiriyoruz.
                speech.speakMessage(Tek_Mesaj)
        
        # Eğer ayarlardan zorunlu odak açıksa veya kullanıcı zaten listenin en altındaysa odağı kaydırıyoruz.
        if Zorunlu_Odak or En_Altta_Mi:
            # Seçim odağını listenin en sonuna eklenen elemana kaydırarak güncelliyoruz.
            self.Sohbet_Liste_Kutusu.SetSelection(self.Sohbet_Liste_Kutusu.GetCount() - 1)