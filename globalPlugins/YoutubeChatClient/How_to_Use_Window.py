# How_to_Use_Window.py - API Anahtarı Alma Rehberi Penceresi
# Arayüz nesneleri üretmek için wxPython kütüphanesini içe aktarıyoruz.
import wx
# Tarayıcıda dış bağlantı açmak için webbrowser kütüphanesini içe aktarıyoruz.
import webbrowser
# Temel pencere sınıfı, doküman okuma aracı ve çeviri fonksiyonunu utils modülünden içe aktarıyoruz.
from .utils import Temel_Pencere, Dokuman_Dosyasi_Oku, _

# Kullanıcılara API anahtarını nasıl alacaklarını gösteren rehber penceresinin sınıfını tanımlıyoruz.
class Api_Rehberi_Penceresi(Temel_Pencere):
    # Sınıf örneklemi başlatıldığında çalışacak olan ana yapıcı metodu tanımlıyoruz.
    def __init__(self, Ebeveyn):
        # Üst sınıfın yapıcı metodunu çağırıp, pencerenin genel başlığını ve boyutunu (600x550) ayarlıyoruz.
        super(Api_Rehberi_Penceresi, self).__init__ \
        (
            # Pencerenin kime (hangi ebeveyne) ait olduğunu belirtiyoruz.
            Ebeveyn, 
            # Pencere başlığını yerelleştirme (çeviri) fonksiyonu ile alarak ayarlıyoruz.
            _("API Anahtarı Alma Rehberi"), 
            # Pencerenin genişliğini ve yüksekliğini belirliyoruz.
            (600, 550)
        )
        
        # İçerisine nesneleri (buton, metin) ekleyeceğimiz temel paneli oluşturuyoruz.
        Panel = wx.Panel(self)
        # Nesneleri alt alta düzenli bir şekilde sıralayacak dikey kutu boyutlandırıcısını oluşturuyoruz.
        Dikey_Kutu = wx.BoxSizer(wx.VERTICAL)
        
        # Rehber metin verisini yerel doküman dosyasından (api_guide.txt) okutuyoruz.
        Metin_Icerigi = Dokuman_Dosyasi_Oku("api_guide.txt")
        
        # Okunan rehber metnini erişilebilir bir biçimde ekranda tutacak çok satırlı metin kutusu oluşturuyoruz.
        Metin_Kutusu = wx.TextCtrl \
        (
            # Metin kutusunun çizileceği asıl paneli belirtiyoruz.
            Panel, 
            # Metin kutusunun özelliklerini (çok satırlı, kullanıcı tarafından değiştirilemez, zengin metin) atıyoruz.
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, 
            # Dosyadan okunan metni değer olarak metin kutusuna yüklüyoruz.
            value=Metin_Icerigi
        )
        # Üretilen metin kutusunu dikey boyutlandırıcı listesine ekliyor ve her taraftan 10 piksel pay bırakıyoruz.
        Dikey_Kutu.Add(Metin_Kutusu, 1, wx.EXPAND | wx.ALL, 10)

        # Kullanıcıyı hızlıca Google Cloud Console'a yönlendirecek olan eylem butonunu üretiyoruz.
        Konsol_Butonu = wx.Button \
        (
            # Butonun form üzerinde bulunacağı paneli belirtiyoruz.
            Panel, 
            # Butonun ekran okuyucu tarafından okunacak çevrilmiş etiketini belirliyoruz.
            label=_("Google Cloud Console'u Tarayıcıda Aç")
        )
        # Eylem butonuna tıklandığında hedeflenen Google Cloud Console web sayfasını açacak olayı bağlıyoruz.
        Konsol_Butonu.Bind \
        (
            # Gerçekleşmesi beklenen olay türünü (buton tıklaması) olarak atıyoruz.
            wx.EVT_BUTTON, 
            # Tıklama anında lambda ile tarayıcıyı tetikliyor ve adresi gönderiyoruz.
            lambda Olay: webbrowser.open("https://console.cloud.google.com/")
        )
        # Konsol butonunu ekranın dikey hiyerarşisinde alta ve ortaya gelecek şekilde boyutlandırıcıya dâhil ediyoruz.
        Dikey_Kutu.Add(Konsol_Butonu, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        # Okuma işlemi bitince pencereyi kapatmak için standart bir kapatma butonu üretiyoruz.
        Kapat_Butonu = wx.Button \
        (
            # Kapatma butonunun bağlı olduğu paneli belirtiyoruz.
            Panel, 
            # Butonun sistemde diyalog kapatıcı olarak algılanması için ID'sini (OK) yapıyoruz.
            id=wx.ID_OK, 
            # Butonun görünecek olan çevrilmiş metin etiketini ayarlıyoruz.
            label=_("Kapat")
        )
        # Kapat butonunu dikey boyutlandırıcının en altına ve merkeze yerleştiriyoruz.
        Dikey_Kutu.Add(Kapat_Butonu, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        # Her pencerede olması gereken telif hakkı bilgisini alt kısıma ekleyen ebeveyn sınıf metodunu çağırıyoruz.
        self.Telif_Hakkini_Ekle(Dikey_Kutu, Panel)
        # İçine nesneleri doldurduğumuz dikey boyutlandırıcının ayarlarını nihai olarak panele uyguluyoruz.
        Panel.SetSizer(Dikey_Kutu)