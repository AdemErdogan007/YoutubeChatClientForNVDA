# About_Window.py - Eklenti Hakkında Penceresi
# Arayüz nesneleri tasarlamak için wxPython kütüphanesini içe aktarıyoruz.
import wx
# Temel pencere sınıfı, doküman okuma aracı ve çeviri fonksiyonunu utils modülünden içe aktarıyoruz.
from .utils import Temel_Pencere, Dokuman_Dosyasi_Oku, _

# Eklenti hakkında detaylı bilgilerini gösterecek olan pencere sınıfımızı tanımlıyoruz.
class Eklenti_Hakkinda_Penceresi(Temel_Pencere):
    # Sınıf başlatıldığında otomatik olarak çalışacak yapıcı metodu tanımlıyoruz.
    def __init__(self, Ebeveyn):
        # Üst sınıfın yapıcı metodunu çağırıp, pencere başlığını ve boyutunu (500x400) ayarlıyoruz.
        super(Eklenti_Hakkinda_Penceresi, self).__init__ \
        (
            # Pencerenin ait olduğu ebeveyn nesnesini belirtiyoruz.
            Ebeveyn, 
            # Pencere başlığını çeviri fonksiyonu aracılığıyla alıp ayarlıyoruz.
            _("Eklenti Hakkında"), 
            # Pencerenin genişlik ve yükseklik boyutlarını piksel cinsinden belirliyoruz.
            (500, 400)
        )
        
        # Pencere içerisine form nesnelerinin ekleneceği ana bir panel oluşturuyoruz.
        Panel = wx.Panel(self)
        # Nesneleri yukarıdan aşağıya (dikey) sıralayacak bir kutu boyutlandırıcı oluşturuyoruz.
        Dikey_Kutu = wx.BoxSizer(wx.VERTICAL)
        
        # Hakkında metnini arka planda dinamik olarak doküman dosyasından (about.txt) okuyoruz.
        Metin_Icerigi = Dokuman_Dosyasi_Oku("about.txt")
        
        # Okunan metni ekranda göstermek için çok satırlı ve salt okunur bir metin kutusu oluşturuyoruz.
        Metin_Kutusu = wx.TextCtrl \
        (
            # Metin kutusunun ekleneceği hedef paneli belirtiyoruz.
            Panel, 
            # Metin kutusunun çok satırlı, değiştirilemez (okunabilir) ve zengin metin olmasını sağlıyoruz.
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, 
            # Metin kutusunun içerisine az önce dosyadan okunmuş olan metni yerleştiriyoruz.
            value=Metin_Icerigi
        )
        # Oluşturulan metin kutusunu dikey boyutlandırıcıya ekliyor ve her kenardan 10 birim boşluk bırakıyoruz.
        Dikey_Kutu.Add(Metin_Kutusu, 1, wx.EXPAND | wx.ALL, 10)
        
        # Pencereyi kapatma görevini üstlenecek olan standart erişilebilir bir buton oluşturuyoruz.
        Kapat_Butonu = wx.Button \
        (
            # Butonun yerleştirileceği paneli belirtiyoruz.
            Panel, 
            # Butonun standart bir onay butonu (OK) sistem kimliğine sahip olmasını sağlıyoruz.
            id=wx.ID_OK, 
            # Butonun üzerinde okunacak olan etiketi çeviri fonksiyonu ile sisteme veriyoruz.
            label=_("Kapat")
        )
        # Kapat butonunu dikey boyutlandırıcının altına yatayda ortalayarak konumlandırıyoruz.
        Dikey_Kutu.Add(Kapat_Butonu, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        # Alt kısma telif hakkı bilgisini ekleyen temel pencereye ait metodumuzu çağırıyoruz.
        self.Telif_Hakkini_Ekle(Dikey_Kutu, Panel)
        # Bütün nesnelerin içine eklendiği hazırlanan dikey boyutlandırıcıyı ana panele uyguluyoruz.
        Panel.SetSizer(Dikey_Kutu)