# Settings_Window.py - Ayarlar Penceresi
# Kullanıcı arayüz form bileşenlerini tasarlamak için wxPython kütüphanesini içe aktarıyoruz.
import wx
# Ayarları kaydederken JSON formatında saklamak için json modülünü dahil ediyoruz.
import json
# NVDA üzerinden kullanıcıya anlık durum mesaj kutuları göstermek için ui modülünü dahil ediyoruz.
import ui
# NVDA ana ekran nesnesine ve pencerelerine erişebilmek için gui modülünü dahil ediyoruz.
import gui
# Ortak temel pencere sınıfını, ayar yükleyicisini, ayar dosya yolunu ve çeviri aracını utils modülünden alıyoruz.
from .utils import Temel_Pencere, Ayarlari_Yukle, Ayar_Dosyasi, _
# API rehber penceresini açabilmek için ilgili diyalog sınıfını içe aktarıyoruz.
from .How_to_Use_Window import Api_Rehberi_Penceresi

# Eklentinin genel yapılandırma seçeneklerini barındıran Ayarlar Penceresi sınıfını kuruyoruz.
class Ayarlar_Penceresi(Temel_Pencere):
    # Sınıf çağrıldığında çalışacak olan ana yapıcı metodu tanımlıyoruz.
    def __init__(self, Ebeveyn):
        # Üst sınıf yapıcı metodunu tetikleyerek pencere başlığını ve boyutunu (550x450) belirliyoruz.
        super(Ayarlar_Penceresi, self).__init__ \
        (
            # Pencerenin türediği üst ebeveyn nesnesini gönderiyoruz.
            Ebeveyn, 
            # Pencerenin üst başlık metnini yerelleştirme fonksiyonundan geçirerek veriyoruz.
            _("Ayarlar - Youtube Canlı Sohbet İstemcisi"), 
            # Genişlik ve yükseklik piksel sınır değerlerini belirliyoruz.
            (550, 450)
        )
        # Mevcut kayıtlı eklenti ayarlarını yapılandırma dosyasından okuyup sınıf değişkenine yüklüyoruz.
        self.Ayarlar_Sozlugu = Ayarlari_Yukle()
        # Arayüz elemanlarını panel üzerine yerleştiren çizim metodumuzu başlatıyoruz.
        self.Arayuzu_Olustur()

    # Pencere elemanlarını hiyerarşik ve erişilebilir düzende inşa eden metot.
    def Arayuzu_Olustur(self):
        # Tüm form bileşenlerinin üzerine yerleştirileceği ana panel nesnesini üretiyoruz.
        self.Ana_Panel = wx.Panel(self)
        # Elemanları yukarıdan aşağıya düzenli sıralayacak ana dikey boyutlandırıcıyı kuruyoruz.
        Dikey_Kutu = wx.BoxSizer(wx.VERTICAL)

        # --- API Yapılandırma Bölümü ---
        # API alanı için etrafı çizgili ve çeviri başlıklı bir grup kutusu (StaticBox) üretiyoruz.
        Api_Grup_Kutusu = wx.StaticBox(self.Ana_Panel, label=_("API Yapılandırması"))
        # Grup kutusunun içerisine dikey eleman yerleştirmeyi sağlayan sizer yapısını kuruyoruz.
        Api_Grup_Boyutlandirici = wx.StaticBoxSizer(Api_Grup_Kutusu, wx.VERTICAL)
        
        # API metin kutusunun üzerine bilgilendirici statik metin etiketini ekliyoruz.
        Api_Grup_Boyutlandirici.Add(wx.StaticText(self.Ana_Panel, label=_("Google API Anahtarı:")), 0, wx.EXPAND | wx.ALL, 5)
        
        # Şifre kutusu ve butonları yan yana dizmek için yatay bir kutu düzenleyici açıyoruz.
        self.Anahtar_Yatay_Kutu = wx.BoxSizer(wx.HORIZONTAL)
        # Kullanıcının gizli API anahtarını yazacağı, başlangıçta maskeli (şifreli) metin kutusunu üretiyoruz.
        self.Api_Metin_Kutusu = wx.TextCtrl(self.Ana_Panel, value=self.Ayarlar_Sozlugu["api_key"], style=wx.TE_PASSWORD)
        # Metin kutusunu yatay düzende genişleyecek şekilde ve sağından 5 piksel boşlukla ekliyoruz.
        self.Anahtar_Yatay_Kutu.Add(self.Api_Metin_Kutusu, 1, wx.EXPAND | wx.RIGHT, 5)
        
        # Maskelenmiş şifreyi açık metne dönüştürmeyi sağlayacak olan Göster butonunu üretiyoruz.
        self.Goster_Gizle_Butonu = wx.Button(self.Ana_Panel, label=_("Göster"))
        # Göster/Gizle butonuna tıklandığında maskeleme durumunu tersine çevirecek metodu bağlıyoruz.
        self.Goster_Gizle_Butonu.Bind(wx.EVT_BUTTON, self.Anahtar_Gorunumunu_Degistir)
        # Butonu yatay düzene sağından 5 piksel boşluk kalacak şekilde dâhil ediyoruz.
        self.Anahtar_Yatay_Kutu.Add(self.Goster_Gizle_Butonu, 0, wx.RIGHT, 5)

        # Yanlış girilen anahtarı hızlıca temizlemek için Sil eylem butonunu üretiyoruz.
        self.Temizle_Butonu = wx.Button(self.Ana_Panel, label=_("Sil"))
        # Sil butonuna basıldığında kutu içeriğini boşaltacak olan olay fonksiyonunu bağlıyoruz.
        self.Temizle_Butonu.Bind(wx.EVT_BUTTON, self.Anahtar_Metnini_Sil)
        # Sil butonunu yatay kutunun en sağına yerleştiriyoruz.
        self.Anahtar_Yatay_Kutu.Add(self.Temizle_Butonu, 0)
        
        # Hazırlanan butonlu yatay satır düzenini API grup boyutlandırıcısına ekliyoruz.
        Api_Grup_Boyutlandirici.Add(self.Anahtar_Yatay_Kutu, 0, wx.EXPAND | wx.ALL, 5)
        
        # Kullanıcının rehber ekranına hızlı erişmesi için API yardım butonunu üretiyoruz.
        Rehber_Butonu = wx.Button(self.Ana_Panel, label=_("API Anahtarı Nasıl Alınır?"))
        # Rehber butonuna tıklandığında rehber diyalogunu ekrana modal getiren olayı bağlıyoruz.
        Rehber_Butonu.Bind(wx.EVT_BUTTON, lambda Olay: Api_Rehberi_Penceresi(self).ShowModal())
        # Rehber butonunu API grup boyutlandırıcısının altına ekliyoruz.
        Api_Grup_Boyutlandirici.Add(Rehber_Butonu, 0, wx.ALL, 5)
        
        # API grup kutusu sizer yapısını ana dikey kutu düzenleyicisine 10 dış boşlukla ekliyoruz.
        Dikey_Kutu.Add(Api_Grup_Boyutlandirici, 0, wx.EXPAND | wx.ALL, 10)

        # --- Genel Ayarlar Bölümü ---
        # Genel ayar seçenekleri için etrafı çizgili ve yerelleştirilmiş başlıklı ikinci grup kutusunu kuruyoruz.
        Genel_Grup_Kutusu = wx.StaticBox(self.Ana_Panel, label=_("Genel Ayarlar"))
        # Bu grup kutusunun içerisine dikey yerleşim düzeni sağlayan sizer yapısını tanımlıyoruz.
        Genel_Grup_Boyutlandirici = wx.StaticBoxSizer(Genel_Grup_Kutusu, wx.VERTICAL)

        # Zaman damgası gösterimini açıp kapatacak olan onay kutusunu (CheckBox) üretiyoruz.
        self.Zaman_Damgasi_Onay_Kutusu = wx.CheckBox(self.Ana_Panel, label=_("Sohbet mesajlarında zaman damgasını göster"))
        # Onay kutusunun başlangıç durumunu kayıtlı ayar değerine göre seçili veya boş yapıyoruz.
        self.Zaman_Damgasi_Onay_Kutusu.SetValue(self.Ayarlar_Sozlugu["show_timestamp"])
        # Onay kutusunu genel grup düzenine dahil ediyoruz.
        Genel_Grup_Boyutlandirici.Add(self.Zaman_Damgasi_Onay_Kutusu, 0, wx.ALL, 5)

        # Mesajların seslendirilmesini kontrol eden otomatik oku onay kutusunu üretiyoruz.
        self.Otomatik_Oku_Onay_Kutusu = wx.CheckBox(self.Ana_Panel, label=_("Yeni gelen mesajları seslendir"))
        # Başlangıç değerini mevcut kullanıcı ayarlarına göre setliyoruz.
        self.Otomatik_Oku_Onay_Kutusu.SetValue(self.Ayarlar_Sozlugu["auto_read"])
        # Otomatik oku bileşenini grup düzenine ekliyoruz.
        Genel_Grup_Boyutlandirici.Add(self.Otomatik_Oku_Onay_Kutusu, 0, wx.ALL, 5)
        
        # Yeni mesaj geldiğinde listenin en altına atlamayı sağlayan onay kutusunu üretiyoruz.
        self.Sona_Odaklan_Onay_Kutusu = wx.CheckBox(self.Ana_Panel, label=_("Yeni mesaj geldiğinde odağı son mesaja taşı"))
        # Kullanıcının kayıtlı tercih değerini bileşene yüklüyoruz.
        self.Sona_Odaklan_Onay_Kutusu.SetValue(self.Ayarlar_Sozlugu["focus_last"])
        # Sona odaklan onay kutusunu genel grup düzenine ekliyoruz.
        Genel_Grup_Boyutlandirici.Add(self.Sona_Odaklan_Onay_Kutusu, 0, wx.ALL, 5)

        # Sayısal yenileme süresini yan yana dizmek için yatay bir kutu düzenleyici kuruyoruz.
        Yenileme_Yatay_Kutu = wx.BoxSizer(wx.HORIZONTAL)
        # Süre ayar alanının soluna bilgilendirici statik metin etiketini ekliyoruz.
        Yenileme_Yatay_Kutu.Add(wx.StaticText(self.Ana_Panel, label=_("API İstek Süresi (Saniye):")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        # Kullanıcının sayısal değer (en az 3, en fazla 60 saniye) seçebileceği SpinCtrl kutusunu üretiyoruz.
        self.Sure_Ayar_Kutusu = wx.SpinCtrl(self.Ana_Panel, value=str(self.Ayarlar_Sozlugu["refresh_rate"]), min=3, max=60)
        # Değer seçim kutusunu yatay düzene yerleştiriyoruz.
        Yenileme_Yatay_Kutu.Add(self.Sure_Ayar_Kutusu, 0)
        # Hazırlanan süreli yatay kutuyu genel grup boyutlandırıcısının içerisine ekliyoruz.
        Genel_Grup_Boyutlandirici.Add(Yenileme_Yatay_Kutu, 0, wx.ALL, 5)

        # Genel grup sizer yapısını ana dikey kutu düzenleyicisine 10 dış boşlukla dâhil ediyoruz.
        Dikey_Kutu.Add(Genel_Grup_Boyutlandirici, 0, wx.EXPAND | wx.ALL, 10)

        # --- Alt Eylem Butonları Alanı ---
        # Kaydet ve Sıfırla butonlarını yan yana koymak için yatay bir kutu sizer tanımlıyoruz.
        Eylem_Butonlari_Kutusu = wx.BoxSizer(wx.HORIZONTAL)
        # Yapılan değişiklikleri diske yazacak olan Ayarları Kaydet butonunu üretiyoruz.
        Kaydet_Butonu = wx.Button(self.Ana_Panel, label=_("Ayarları Kaydet"))
        # Kaydet butonuna basıldığında verileri json dosyasına yazacak metodu bağlıyoruz.
        Kaydet_Butonu.Bind(wx.EVT_BUTTON, self.Ayarlari_Kaydet)
        # Kaydet butonunu eylem kutusuna sağından 5 piksel boşluk vererek eşit oranda yayılacak şekilde ekliyoruz.
        Eylem_Butonlari_Kutusu.Add(Kaydet_Butonu, 1, wx.RIGHT, 5)
        
        # Ayarları ilk kurulum durumuna döndürecek olan Varsayılana Döndür butonunu üretiyoruz.
        Sifirla_Butonu = wx.Button(self.Ana_Panel, label=_("Varsayılana Döndür"))
        # Sıfırlama butonuna basıldığında varsayılan değerleri basacak olan fonksiyonu bağlıyoruz.
        Sifirla_Butonu.Bind(wx.EVT_BUTTON, self.Varsayilanlara_Dondur)
        # Sıfırlama butonunu eylem kutusuna solundan 5 piksel boşluk vererek eşit oranda yayılacak şekilde ekliyoruz.
        Eylem_Butonlari_Kutusu.Add(Sifirla_Butonu, 1, wx.LEFT, 5)
        
        # Eylem butonları kutusunu ana dikey düzenleyiciye 10 dış boşlukla ekliyoruz.
        Dikey_Kutu.Add(Eylem_Butonlari_Kutusu, 0, wx.EXPAND | wx.ALL, 10)
        # Formun düzgün görünmesi ve telif yazısının dibe itilmesi için esnek bir dikey boşluk bırakıyoruz.
        Dikey_Kutu.AddStretchSpacer() 
        # Eklenti sahibi telif hakkı şerit butonunu formun en alt sınırına işliyoruz.
        self.Telif_Hakkini_Ekle(Dikey_Kutu, self.Ana_Panel)
        # Yapılandırılan tüm dikey yerleşim sizer şablonunu ana panelin kuralı olarak atıyoruz.
        self.Ana_Panel.SetSizer(Dikey_Kutu)
        # ESC tuşu ile pencereden çıkabilmek için klavye yakalama olayını bağlıyoruz.
        self.Bind(wx.EVT_CHAR_HOOK, self.Penceyi_Kapat_Klavye)

    # Şifre alanındaki maskeli yıldızları açık metne veya tam tersine çeviren dinamik görünüm metodu.
    def Anahtar_Gorunumunu_Degistir(self, Olay):
        # Mevcut metin kutusu içerisindeki yazılı olan API anahtar değerini korumak için alıyoruz.
        Gecerli_Metin = self.Api_Metin_Kutusu.GetValue()
        # Buton etiketinin 'Gizle (*)' durumunda olup olmadığını mantıksal olarak sorguluyoruz.
        Maske_Acik_Mi = self.Goster_Gizle_Butonu.GetLabel() == _("Gizle (*)")
        # Eğer maske açıksa yeni kutu şifreli (TE_PASSWORD) olacak, kapalıysa normal metin (0) tarzı olacaktır.
        Yeni_Stil = 0 if not Maske_Acik_Mi else wx.TE_PASSWORD
        # Butonun bir sonraki tıklamada alacağı yeni çevrilmiş yazı etiketini belirliyoruz.
        Yeni_Etiket = _("Gizle (*)") if not Maske_Acik_Mi else _("Göster")
        
        # Eski metin kutusunu bağlı olduğu yatay yerleşim kutusundan ayırıyoruz.
        self.Anahtar_Yatay_Kutu.Detach(self.Api_Metin_Kutusu)
        # Eski metin kutusu nesnesini hafızadan tamamen yok ediyoruz.
        self.Api_Metin_Kutusu.Destroy()
        # Belirlenen yeni stil kodu ile sıfırdan güncel bir metin kutusu nesnesi üretiyoruz.
        self.Api_Metin_Kutusu = wx.TextCtrl(self.Ana_Panel, value=Gecerli_Metin, style=Yeni_Stil)
        # Yeni oluşturulan metin kutusunu yatay düzenleyicinin en başına (0. indeks) tekrar yerleştiriyoruz.
        self.Anahtar_Yatay_Kutu.Insert(0, self.Api_Metin_Kutusu, 1, wx.EXPAND | wx.RIGHT, 5)
        # Buton üzerindeki yazıyı güncelliyoruz.
        self.Goster_Gizle_Butonu.SetLabel(Yeni_Etiket)
        # Değişen nesne boyutlarına göre ana panel yerleşimini yeniden hesaplatıp çizdiriyoruz.
        self.Ana_Panel.Layout()
        # Ekran okuyucuun odağını kaybolmaması için yeniden yeni üretilen metin kutusuna kuruyoruz.
        self.Api_Metin_Kutusu.SetFocus()

    # API anahtarı metin giriş alanını el ile tamamen sıfırlayan metot.
    def Anahtar_Metnini_Sil(self, Olay):
        # Metin kutusunun içerisindeki değeri boş string ile değiştiriyoruz.
        self.Api_Metin_Kutusu.SetValue("")

    # Form üzerindeki verileri toplayıp JSON dosyasına kalıcı olarak yazan metot.
    def Ayarlari_Kaydet(self, Olay):
        # Form bileşenlerinden okunan güncel değerlerle yeni bir ayar sözlüğü şablonu oluşturuyoruz.
        Guncel_Ayarlar_Seti = \
        {
            # API anahtarı metnini alıp sağındaki solundaki boşlukları temizleyerek sözlüğe ekliyoruz.
            "api_key": self.Api_Metin_Kutusu.GetValue().strip(),
            # Zaman damgası onay kutusunun durumunu (True/False) alıp sözlüğe yazıyoruz.
            "show_timestamp": self.Zaman_Damgasi_Onay_Kutusu.GetValue(),
            # Otomatik mesaj seslendirme onay kutusunun anlık durumunu ekliyoruz.
            "auto_read": self.Otomatik_Oku_Onay_Kutusu.GetValue(),
            # Son mesaja odaklanma tercihinin durumunu sözlüğe aktarıyoruz.
            "focus_last": self.Sona_Odaklan_Onay_Kutusu.GetValue(),
            # Yenileme hızı spin kutusundan seçilen sayısal saniye değerini ekliyoruz.
            "refresh_rate": self.Sure_Ayar_Kutusu.GetValue()
        }
        # Dosya yazma eylemini korumalı hata kontrol bloğu altında deniyoruz.
        try:
            # NVDA yapılandırma klasöründeki hedef ayar dosyasını UTF-8 modunda yazma amaçlı açıyoruz.
            with open(Ayar_Dosyasi, "w", encoding="utf-8") as Dosya:
                # Ayarlar sözlüğünü girintili (indent=4) ve Türkçe karakterleri bozmadan (ensure_ascii=False) JSON olarak yazıyoruz.
                json.dump(Guncel_Ayarlar_Seti, Dosya, indent=4, ensure_ascii=False)
            
            # Kullanıcıya ayarların başarıyla kaydedildiğini bildiren ekran okuyucu mesajı geçiyoruz.
            ui.message(_("Ayarlar kaydedildi."))
            # Ayarlar penceresi görevini başarıyla tamamladığı için pencereyi kapatıp yok ediyoruz.
            self.Destroy()
            
            # Değişen ayarların ana ekrana da anlık yansıması için ana pencere sınıfını içe aktarıyoruz.
            from .Main_Window import Youtube_Canli_Sohbet_Penceresi
            # Ana ekranın sistemde açık olup olmadığını kontrol etmek için bayrak değişken açıyoruz.
            Ana_Ekran_Acik_Mi = False
            # NVDA ana ekranına bağlı olan tüm açık çocuk pencereleri döngü ile denetliyoruz.
            for Cocuk_Pencere in gui.mainFrame.GetChildren():
                # Eğer çocuk pencerelerden biri ana sohbet ekranı sınıfından bir örnek ise şart sağlanır.
                if isinstance(Cocuk_Pencere, Youtube_Canli_Sohbet_Penceresi):
                    # Açık olan ana sohbet ekranının ayar hafızasını yeni güncellediğimiz verilerle yeniliyoruz.
                    Cocuk_Pencere.Ayarlar_Sozlugu = Cocuk_Pencere.Mevcut_Ayarlari_Getir()
                    # Ana ekranı pencerelerin en üstüne yükseltiyoruz.
                    Cocuk_Pencere.Raise()
                    # Ekran okuyucu odağını ana ekrana odaklıyoruz.
                    Cocuk_Pencere.SetFocus()
                    # Ana ekranın açık olduğunu onaylayıp bayrağı True yapıyoruz.
                    Ana_Ekran_Acik_Mi = True
                    # Aranan pencere bulunduğu için döngüden çıkış yapıyoruz.
                    break
            
            # Eğer ilk kurulumsa ve arka planda açık bir ana sohbet ekranı bulunamadıysa çalışacak şart.
            if not Ana_Ekran_Acik_Mi:
                # NVDA sistem açılır pencere hazırlık rutinini çalıştırıyoruz.
                gui.mainFrame.prePopup()
                # Sıfırdan yeni bir ana canlı sohbet pencere diyalogu oluşturuyoruz.
                Diyalog = Youtube_Canli_Sohbet_Penceresi(gui.mainFrame)
                # Yeni oluşturulan ana ekranı görünür hale getiriyoruz.
                Diyalog.Show()
                # Açılır pencere sonrası NVDA rutin sistem işlemlerini DÜZELTİLMİŞ ŞEKİLDE çalıştırıyoruz.
                gui.mainFrame.postPopup()

        # Dosyaya yazma veya yenileme anında beklenmedik bir sistem hatası çıkarsa yakalıyoruz.
        except Exception as Hata:
            # Oluşan hatayı ekrana uyarı mesajı olarak basıyoruz.
            ui.message(f"Hata: {Hata}")

    # Tüm ayar bileşenlerini fabrika ayarlarına döndürüp kaydeden sıfırlama metodu.
    def Varsayilanlara_Dondur(self, Olay):
        # API anahtarı alanını temizliyoruz.
        self.Api_Metin_Kutusu.SetValue("")
        # Zaman damgası onay kutusunu varsayılan kapalı (False) yapıyoruz.
        self.Zaman_Damgasi_Onay_Kutusu.SetValue(False)
        # Otomatik seslendirmeyi varsayılan açık (True) konumuna getiriyoruz.
        self.Otomatik_Oku_Onay_Kutusu.SetValue(True)
        # Sona odaklanmayı varsayılan kapalı (False) duruma alıyoruz.
        self.Sona_Odaklan_Onay_Kutusu.SetValue(False)
        # İstek periyodu süresini varsayılan fabrika değeri olan 10 saniyeye ayarlıyoruz.
        self.Sure_Ayar_Kutusu.SetValue(10)
        # Yeni fabrika değerlerini json dosyasına kaydetmesi için kaydetme fonksiyonunu el ile tetikliyoruz.
        self.Ayarlari_Kaydet(None)

    # Klavye tuş basımlarında Escape tuşunu yakalayıp pencereyi kapatan metot.
    def Penceyi_Kapat_Klavye(self, Olay):
        # Basılan tuş kodunun ESC tuşu olup olmadığını sorguluyoruz.
        if Olay.GetKeyCode() == wx.WXK_ESCAPE:
            # Eğer ESC tuşuna basıldıysa pencereyi kapatıp bellekten siliyoruz.
            self.Destroy()
        # Diğer tuşların normal çalışmasını sürdürmesi için devrediyoruz.
        else:
            # Olayı sistemin zincirindeki bir sonraki dinleyiciye aktarıyoruz.
            Olay.Skip()