# __init__.py - Eklenti Giriş Noktası
# Eklentinin çalışması için gerekli olan temel global eklenti modülünü içe aktarıyoruz.
import globalPluginHandler
# Kullanıcı arayüzü işlemleri için NVDA gui modülünü içe aktarıyoruz.
import gui
# Pencere ve arayüz çizimleri için wxPython kütüphanesini içe aktarıyoruz.
import wx
# Kullanıcıya mesaj göstermek için NVDA ui modülünü içe aktarıyoruz.
import ui
# Ortak araçlardan ayar yükleme, taşıma ve çeviri fonksiyonlarını utils dosyasından çekiyoruz.
from .utils import Ayarlari_Yukle, Ayarlari_Kontrol_Et_Ve_Tasi, _
# Ana sohbet penceresi sınıfını içe aktarıyoruz.
from .Main_Window import Youtube_Canli_Sohbet_Penceresi
# Ayarlar penceresi sınıfını içe aktarıyoruz.
from .Settings_Window import Ayarlar_Penceresi

# NVDA'nın global eklenti sınıfından miras alan ana mimari sınıfımızı tanımlıyoruz.
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    # Eklentimizin NVDA kısayol tuşları menüsündeki kategori adını belirliyoruz.
    scriptCategory = _("Youtube Canlı Sohbet İstemcisi")

    # Sınıf başlatıldığında otomatik olarak çalışacak yapıcı metodu tanımlıyoruz.
    def __init__(self):
        # Üst sınıfın (GlobalPlugin) yapıcı metodunu miras gereği çağırıyoruz.
        super(GlobalPlugin, self).__init__()
        
        # Ayarların kontrolü ve güvenli dizine taşınması işlemlerini deniyoruz.
        try:
            # Eski ayarlar varsa yeni yapıya taşınmasını sağlayan metodu tetikliyoruz.
            Ayarlari_Kontrol_Et_Ve_Tasi()
            
        # Olası bir hata durumunu yakalıyoruz.
        except Exception as Hata:
            # Hatayı geliştiricilerin görebileceği şekilde NVDA günlüğüne hata olarak kaydediyoruz.
            globalPluginHandler.log.error(f"YoutubeChatClient Hata: {Hata}")

        # NVDA arayüzü tam yüklendikten sonra hata vermemesi için menü oluşturma metodunu arayüz döngüsüne aktarıyoruz.
        wx.CallAfter(self.Menuyu_Olustur)

    # NVDA araçlar menüsüne eklentimizin menü öğesini ve kısayolunu ekleyen metot.
    def Menuyu_Olustur(self):
        # Menü ekleme işlemlerini güvenlik için hata kontrolü (try-except) içinde deniyoruz.
        try:
            # NVDA'nın sistem tepsisindeki Araçlar menüsü nesnesine erişiyoruz.
            self.Araclar_Menusu = gui.mainFrame.sysTrayIcon.toolsMenu
            # Araçlar menüsüne eklentimiz için yeni bir tıklanabilir öğe ekliyoruz.
            self.Menu_Ogesi = self.Araclar_Menusu.Append \
            (
                # Menü öğesi için sisteme otomatik bir benzersiz kimlik (ID) atatıyoruz.
                wx.ID_ANY, 
                # Menüde görünecek olan başlık metnini çeviri fonksiyonu ile alıyoruz.
                _("Youtube Canlı Sohbet İstemcisi"), 
                # Menü öğesinin üzerine gelindiğinde ekran okuyucunun söyleyeceği açıklama metnini ekliyoruz.
                _("YouTube canlı sohbet penceresini açar")
            )
            # Menü öğesine tıklandığında hangi fonksiyonun çalışacağını bir olay dinleyicisi (Bind) ile bağlıyoruz.
            gui.mainFrame.sysTrayIcon.Bind \
            (
                # Olay türünü menü tıklaması (EVT_MENU) olarak belirliyoruz.
                wx.EVT_MENU, 
                # Tıklama durumunda çalıştırılacak olan metodumuzu hedef olarak gösteriyoruz.
                self.Menu_Komutunu_Isle, 
                # Bu olayın az önce oluşturduğumuz menü öğesine ait olduğunu belirtiyoruz.
                self.Menu_Ogesi
            )
            
        # Olası bir hata durumunu yakalıyoruz.
        except Exception as Hata:
            # Menü oluşturma hatasını sorunun tespiti için NVDA günlüğüne kaydediyoruz.
            globalPluginHandler.log.error(f"YoutubeChatClient Menü Hatası: {Hata}")

    # Menüden eklentiye tıklandığında tetiklenecek olan ara metot.
    def Menu_Komutunu_Isle(self, Olay):
        # Pencere açma işlemini NVDA ana arayüz döngüsüne (CallAfter) güvenli bir şekilde aktarıyoruz.
        wx.CallAfter(self.Kontrol_Et_Ve_Goster)

    # Kısayol tuşu ile eklentiyi çağıran zorunlu NVDA betik metodu (Adı NVDA standartları gereği değiştirilmez).
    def script_openChatDialog(self, Hareket):
        # Pencere açma işlemini NVDA arayüz döngüsüne güvenli bir şekilde aktarıyoruz.
        wx.CallAfter(self.Kontrol_Et_Ve_Goster)

    # API anahtarı durumunu kontrol edip sonuca göre uygun pencereyi gösteren mantık metodu.
    def Kontrol_Et_Ve_Goster(self):
        # Kullanıcının daha önce kaydettiği ayarları yapılandırma dosyasından yüklüyoruz.
        Ayarlar = Ayarlari_Yukle()
        # Ayarlar sözlüğü içinden API anahtarını alıp, başındaki ve sonundaki olası boşlukları siliyoruz.
        Api_Anahtari = Ayarlar.get("api_key", "").strip()
        
        # Eğer alınan API anahtarı boş ise (daha önce girilmemişse) çalışacak şart bloğu.
        if not Api_Anahtari:
            # Kullanıcıya API anahtarı eksikliği hakkında bilgi veren uyarı diyalogu oluşturuyoruz.
            Diyalog = wx.MessageDialog \
            (
                # Diyalogun ana ebeveyn penceresi olarak NVDA ana ekranını ayarlıyoruz.
                gui.mainFrame, 
                # Kullanıcıya gösterilecek olan çevrilmiş bilgi ve soru metnini belirliyoruz.
                _("API Anahtarı bulunamadı. Ayarlar menüsüne gidip bir anahtar girmek ister misiniz?"),
                # Diyalog penceresinin başlık kısmını belirliyoruz.
                _("Eksik Yapılandırma"), 
                # Diyalogda Evet/Hayır butonları ve sistem uyarı ikonu görünmesini sağlıyoruz.
                wx.YES_NO | wx.ICON_WARNING
            )
            # Diyalog penceresini ekranda gösteriyoruz ve kullanıcının verdiği cevabı kontrol ediyoruz.
            if Diyalog.ShowModal() == wx.ID_YES:
                # Eğer kullanıcı sorulan soruya 'Evet' derse, doğrudan ayarlar penceresini açıyoruz.
                self.Pencereyi_Ac(Ayarlar_Penceresi)
            # Kullanıcı cevabını verdikten ve işlem bittikten sonra diyalog penceresini bellekten siliyoruz.
            Diyalog.Destroy()
            
        # Eğer sistemde bir API anahtarı mevcutsa çalışacak olan alternatif şart bloğu.
        else:
            # Sorun olmadığı için doğrudan ana canlı sohbet penceresini açıyoruz.
            self.Pencereyi_Ac(Youtube_Canli_Sohbet_Penceresi)

    # Kendisine gönderilen pencere sınıfını ekranda gösteren veya zaten açıksa öne getiren metot.
    def Pencereyi_Ac(self, Pencere_Sinifi):
        # NVDA ana ekranına bağlı olan tüm açık alt (çocuk) pencereleri bir döngüye alıyoruz.
        for Cocuk_Pencere in gui.mainFrame.GetChildren():
            # Eğer döngüdeki pencere, açmak istediğimiz pencere sınıfından bir örneksi kontrol ediyoruz.
            if isinstance(Cocuk_Pencere, Pencere_Sinifi):
                # Bulunan pencereyi diğer tüm açık pencerelerin üstüne (öne) getiriyoruz.
                Cocuk_Pencere.Raise()
                # Ekran okuyucunun ve klavyenin odağını bu pencereye ayarlıyoruz.
                Cocuk_Pencere.SetFocus()
                # Yeni pencere oluşturmaya gerek kalmadığı için fonksiyondan hemen çıkıyoruz.
                return
        
        # Eğer pencere önceden açık değilse, NVDA'nın özel açılır pencere öncesi hazırlığını yapıyoruz.
        gui.mainFrame.prePopup()
        # İstenen pencere sınıfından ana ekrana bağlı yeni bir pencere (diyalog) nesnesi oluşturuyoruz.
        Diyalog = Pencere_Sinifi(gui.mainFrame)
        # Oluşturulan yepyeni pencereyi ekranda görünür hale getiriyoruz.
        Diyalog.Show()
        # Pencere başarıyla gösterildikten sonra NVDA'nın açılır pencere sonrası rutin işlemlerini DÜZELTİLMİŞ ŞEKİLDE çalıştırıyoruz.
        gui.mainFrame.postPopup()

    # Kısayol komutunun NVDA girdi menüsünde okunacak açıklaması.
    script_openChatDialog.__doc__ = _("YouTube Canlı Sohbet arayüzünü başlatır.")
    
    # Eklentiyi klavyeden çağırmak için gerekli kısayol tuş atamasını yapıyoruz (NVDA+Shift+Control+Y).
    __gestures = \
    {
        # Hareketi ve çağrılacak betiği bir sözlük olarak tanımlıyoruz.
        "kb:NVDA+shift+control+y": "openChatDialog"
    }

    # Eklenti NVDA'dan kaldırılırken veya NVDA kapanırken çalışacak temizlik metodu.
    def terminate(self):
        # Oluşturduğumuz menü öğesini sistemden kaldırma işlemini deniyoruz.
        try: 
            # Eklentimizin menü öğesini NVDA Araçlar menüsünden eksiksiz siliyoruz.
            self.Araclar_Menusu.Remove(self.Menu_Ogesi)
        # Olası bir hata çıkması durumunda işlemi sessizce pas geçiyoruz.
        except: 
            # Hata oluşursa NVDA'nın çökmemesi için hiçbir şey yapmıyoruz.
            pass
        # Üst eklenti sınıfının kendi sonlandırma metodunu çağırarak işlemi tamamen sonlandırıyoruz.
        super(GlobalPlugin, self).terminate()