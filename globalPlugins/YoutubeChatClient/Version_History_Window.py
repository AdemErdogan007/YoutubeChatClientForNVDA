# Version_History_Window.py - Sürüm Geçmişi Penceresi
# Pencereler ve butonlar gibi arayüz bileşenleri için wxPython kütüphanesini içe aktarıyoruz.
import wx
# Temel pencere mimarisi, metin dosyası okuma aracı ve çeviri fonksiyonunu utils içinden çağırıyoruz.
from .utils import Temel_Pencere, Dokuman_Dosyasi_Oku, _

# Eklentinin güncelleme kayıtlarını (sürüm geçmişini) gösterecek olan sınıfı yapılandırıyoruz.
class Surum_Gecmisi_Penceresi(Temel_Pencere):
    # Sınıf oluşturulurken başlangıç değişkenlerini ayarlayacak yapıcı metodu tanımlıyoruz.
    def __init__(self, Ebeveyn):
        # Üst sınıf (Temel_Pencere) yapıcı metodunu çağırarak pencere ismini ve boyutunu (500x400) belirliyoruz.
        super(Surum_Gecmisi_Penceresi, self).__init__ \
        (
            # Yeni açılacak pencerenin hangi ebeveyn pencereden türediğini iletiyoruz.
            Ebeveyn, 
            # Pencerenin en üstünde görünecek başlığı çeviri destekli şekilde alıyoruz.
            _("Sürüm Geçmişi"), 
            # Pencerenin genişliğini 500, yüksekliğini 400 piksel olarak sınırlandırıyoruz.
            (500, 400)
        )
        
        # Görsel unsurları gruplayarak ekranda göstereceğimiz ana paneli oluşturuyoruz.
        Panel = wx.Panel(self)
        # Görsel unsurları dikey sırayla alt alta yerleştirecek kutu düzenleyicisini (sizer) ayarlıyoruz.
        Dikey_Kutu = wx.BoxSizer(wx.VERTICAL)
        
        # Güncelleme geçmişi bilgilerini tutan metin dosyasını (changelog.txt) okuyucu fonksiyona yollayıp sonucunu alıyoruz.
        Metin_Icerigi = Dokuman_Dosyasi_Oku("changelog.txt")
        
        # Kullanıcının metni okuyabilmesi için salt okunur özelliklere sahip bir yazışma kutusu üretiyoruz.
        Metin_Kutusu = wx.TextCtrl \
        (
            # Ürettiğimiz metin kutusunu oluşturduğumuz panele atıyoruz.
            Panel, 
            # Metin kutusunun birden fazla satıra izin vermesini, sadece okunmasını ve stil kodlarını tanımasını istiyoruz.
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, 
            # Metin dosyasından okuyup aldığımız veriyi bu kontrol elemanının içine değer olarak basıyoruz.
            value=Metin_Icerigi
        )
        # İçi doldurulan metin kutusunu dikey yerleşim düzenine eklerken ona genişleyebilme esnekliği ve 10 piksel kenar boşluğu tanıyoruz.
        Dikey_Kutu.Add(Metin_Kutusu, 1, wx.EXPAND | wx.ALL, 10)
        
        # Kullanıcının işi bittiğinde ekranı rahatça kapatabilmesi için onay tipi bir buton tasarlıyoruz.
        Kapat_Butonu = wx.Button \
        (
            # Butonu aktif panele yerleştiriyoruz.
            Panel, 
            # Butonun pencereyi sonlandırma işlemini yapabilmesi adına ID değerini 'OK' olarak setliyoruz.
            id=wx.ID_OK, 
            # Butonun ekran okuyucuya ve göze hitap edecek etiketi olan 'Kapat' metnini çeviriden alıyoruz.
            label=_("Kapat")
        )
        # Hazırladığımız butonu ekran tasarımının en alt kısmına ortalayarak yerleştiriyoruz ve altından 10 piksel boşluk veriyoruz.
        Dikey_Kutu.Add(Kapat_Butonu, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        # Temel sınıftan miras aldığımız fonksiyon sayesinde pencerenin dibine marka telif bilgisini işliyoruz.
        self.Telif_Hakkini_Ekle(Dikey_Kutu, Panel)
        # Tasarım işlemlerini tamamladığımız dikey düzenleyici yapısını pencere panelinin ana kuralı olarak ilan ediyoruz.
        Panel.SetSizer(Dikey_Kutu)