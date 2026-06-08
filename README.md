# Türkçe : NVDA İçin Youtube Canlı Yayın Sohbet İstemcisi

Bu eklenti, görme engelli kullanıcıların YouTube canlı yayınlarındaki sohbet akışını, Super Chat bağışlarını, Super Sticker gönderimlerini ve kanal üyeliği bildirimlerini NVDA ekran okuyucusu aracılığıyla, tam erişilebilir bir arayüz üzerinden takip etmelerini sağlar.
NVDA 2026.1 ve sonrası 64-bit sürümlerle tam uyumlu olarak çalışan bu istemci, arka planda sessizce veri çekerek sistem performansınızı etkilemez ve kesintisiz bir deneyim sunar.
Gelen yeni mesajları otomatik olarak seslendirme, mesajlara zaman damgası ekleme, listede otomatik odaklanma ve kişiselleştirilebilir API istek süresi gibi gelişmiş özellikler barındırır.
Ayrıca Türkçe, İngilizce ve Almanca olmak üzere tam kapsamlı çoklu dil desteğine sahiptir.

> ⚠️ **Önemli Tavsiye:** Eklentinin en güncel, güvenli ve kararlı sürümünü **NVDA Eklenti Mağazası (Add-on Store)** içerisinden "Youtube Chat Client For NVDA" adıyla aratarak yüklemeniz önemle tavsiye edilir.
Mağaza üzerinden yapılan kurulumlar, gelecekteki güncellemeleri otomatik olarak almanızı sağlayacaktır.

## Kurulum ve İlk Adımlar

### Eklenti İndirme Bağlantısı (Manuel Kurulum) : 
https://github.com/AdemErdogan007/YoutubeChatClientForNVDA/releases/download/V1.7/Youtube-Chat-Client-For-NVDA-V1.7.nvda-addon

* İndirdiğiniz eklentiyi NVDA açıkken çalıştırın ve gelen uyarıyı "Evet" olarak yanıtlayın.
* Kurulum tamamlandığında NVDA'yı yeniden başlatmanız istenecektir. Eklenti, NVDA'nın dilini (Türkçe, İngilizce veya Almanca) otomatik olarak algılayacaktır.
* <kbd> NVDA + Shift + CTRL + Y </kbd> tuşlarına basarak veya NVDA Araçlar menüsünden eklentiyi çalıştırın.
* İlk açılışta API Anahtarı girmeniz istenecektir. Sistem sizi otomatik olarak Ayarlar penceresine yönlendirecektir.
* Google Cloud Console'dan aldığınız YouTube Data v3 API anahtarını buraya yapıştırın ve **"Ayarları Kaydet"** butonuna basın.

## YouTube Data API v3 Anahtarı Nasıl Alınır? (Detaylı Rehber)

Bu rehber, eklentinin YouTube sohbetlerine bağlanabilmesi için gereken ücretsiz API anahtarını adım adım nasıl alacağınızı anlatmaktadır.
Hiçbir teknik bilginiz olmasa bile bu adımları sırasıyla takip ederek anahtarınızı kolayca oluşturabilirsiniz.
Not : API anahtarı size özeldir. Hiç bir kimse ile paylaşmayınız.

### Adım 1: Google Cloud Platform'a Giriş Yapmak
* Eklentideki "Google Cloud Console'u Tarayıcıda Aç" butonuna basın veya tarayıcınızdan "https://console.cloud.google.com" adresine gidin.
* Mevcut bir Google (Gmail) hesabınızla giriş yapın.
Sisteme ilk kez giriyorsanız ekranda bir sözleşme veya karşılama ekranı çıkabilir, onaylayarak devam edin.

### Adım 2: Yeni Bir Proje Oluşturmak
* Ekranın üst kısmında yer alan "Proje Seçin" (Select a project) butonuna tıklayın.
Açılan pencerenin sağ üst köşesindeki "Yeni Proje" (New Project) butonunu bulup basın.
* Proje Adı (Project Name) kısmına eklentiyi hatırlayacağınız basit bir isim yazın (Örneğin: "NVDA Youtube Sohbet").
* Alt kısımdaki "Oluştur" (Create) butonuna basın.
Projenin oluşturulması birkaç saniye sürebilir, tamamlanmasını bekleyin.

### Adım 3: YouTube API'sini Etkinleştirmek
* Projeniz oluştuktan sonra sol taraftaki gezinme menüsünden "API'ler ve Hizmetler" (APIs & Services) seçeneğine, ardından "Kitaplık" (Library) sekmesine tıklayın.
* Karşınıza çıkan arama kutusuna "YouTube Data API v3" yazın ve aratın.
* Çıkan arama sonuçlarından "YouTube Data API v3" bağlantısına tıklayın.
* Açılan sayfada yer alan "Etkinleştir" (Enable) butonuna basın.
Bu işlem, oluşturduğunuz projenize YouTube canlı sohbet verilerini çekme yetkisi verecektir.

### Adım 4: API Anahtarını Üretmek
* API etkinleştirildikten sonra yönlendirildiğiniz sayfada veya sol menüde yer alan "Kimlik Bilgileri" (Credentials) sekmesine tıklayın.
* Ekranın üst kısmındaki "Kimlik Bilgileri Oluştur" (Create Credentials) butonuna basın.
* Açılan küçük menüden "API Anahtarı" (API Key) seçeneğini seçin.

### Adım 5: Anahtarı Kopyalamak ve Eklentiye Eklemek
* Ekranda "API Anahtarı Oluşturuldu" şeklinde bir pencere açılacak ve "AIza" harfleriyle başlayan karmaşık, uzun bir kod belirecektir.
* Bu uzun metin sizin API anahtarınızdır. Metnin yanındaki kopyala butonuna basarak veya metni tamamen seçerek kopyalayın.
* Şimdi NVDA eklenti ayarlarına geri dönün ve kopyaladığınız bu anahtarı "Google API Anahtarı" kutusuna yapıştırıp ayarları kaydedin.

> 🔒 **Önemli Güvenlik Notu:**
Bu anahtar tamamen size özeldir.
Lütfen başkalarıyla veya açık platformlarda paylaşmayın.
Google bu hizmeti kişisel kullanım için tamamen ücretsiz sunmaktadır ve eklentinin mesaj çekmesi için ayrılan günlük kota kişisel kullanım için fazlasıyla yeterlidir.

## Ana Pencere Kullanımı

* **URL Alanı:** Takip etmek istediğiniz YouTube canlı yayınının linkini buraya yapıştırın.
* **Seçenekler Menüsü:** Ayarlar, Sürüm Geçmişi, API Rehberi, Hakkında ve Web Sitesi gibi tüm alt pencerelere bu menüden hızlıca ulaşabilirsiniz.
* **Başlat/Durdur:** Sohbet akışını başlatır or durdurur.
Akış arka planda NVDA'yı yormadan çalışır.
* **Sohbet Listesi:** Gelen mesajlar erişilebilir bir liste halinde buraya düşer.
Yön tuşları ile mesajlar arasında gezinebilirsiniz.

## Ayarlar Menüsü

* **API Anahtarı:** Güvenlik gereği maskelenmiş (yıldızlı) olarak görünür.
"Göster" butonu ile içeriği okuyabilir, "Sil" butonu ile anında temizleyebilirsiniz.
* **Zaman Damgası:** Mesajların başında gönderilme saatinin yazıp yazmayacağını belirler.
* **Otomatik Seslendirme:** Yeni mesaj geldiğinde ekran okuyucunun mesajı otomatik olarak okuyup okumayacağını kontrol eder.
* **Odağı Son Mesaja Taşı:** (Önemli!) Eğer eski mesajları okumak için listede yukarı çıkıyorsanız bu ayarı kapatın.
Açık olması durumunda, gelen her yeni mesajda ekran okuyucu odağı zorunlu olarak listenin en sonuna taşır.
* **API İstek Süresi:** YouTube sunucularından verilerin kaç saniyede bir çekileceğini belirler (Varsayılan 10 saniyedir).
Bu değeri çok düşük tutarsanız günlük API limitiniz çok kısa sürede dolacaktır.
5 ila 15 saniye aralığında kullanmanız tavsiye edilir.
* **Varsayılanlara Dön:** Yaptığınız tüm değişiklikleri sıfırlayarak ayarları ilk kurulum haline geri getirir.

## Sürüm Geçmişi (Changelog)

### v1.7 (2026.06.06)
* **Mimari Güncelleme:** Eklenti tamamen NVDA 2026.1, 64-Bit mimarisi ve Python 3.13 standartlarına %100 uyumlu hale getirildi.
* **İyileştirme:** Tüm arayüz ve diyalog bileşenleri ekran okuyucular için en üst düzey WCAG erişilebilirlik standartlarına göre güncellendi.
* **Düzeltme:** Ana sohbet penceresi açılırken ve ayarlar kaydedildikten sonra NVDA'nın çökmesine neden olan geçersiz "PostPopup" çağırma hatası tamamen giderildi.
* **İyileştirme:** Kod altyapısı katı modüler yapıya geçirilerek arayüz (ön plan) ve çekirdek (arka plan) mantığı tamamen izole edildi.
* **İyileştirme:** Tüm değişken, fonksiyon, sınıf ve dosya isimlendirmeleri Türkçe karakter içermeyen PascalCase standartlarına göre yeniden düzenlendi.
* **Güncelleme:** Tüm kod mimarisine istisnasız her satır için detaylı Türkçe açıklamalar eklenerek geliştirici okunabilirliği en üst seviyeye çıkarıldı.
* **Güncelleme:** API anahtarı alma rehberi ayrıntılı şekilde güncellendi.
* **Güncelleme:** Readme dosyası görsel olarak iyileştirildi ve iletişim bilgileri eklendi.

### v1.6
* **Yeni Özellik:** Tam kapsamlı çoklu dil desteği (Türkçe, İngilizce ve Almanca) eklendi.
* **İyileştirme:** Eklenti dilini NVDA'nın diline göre otomatik ve hatasız algılayan gelişmiş dil yönetim sistemi entegre edildi.
* **Düzeltme:** Pencerelerin bazen ekranda görünmemesine neden olan bellek yönetimi (Garbage Collection) sorunu giderildi.
* **Düzeltme:** Kod mimarisindeki döngüsel içe aktarma (Circular Import) hataları tamamen temizlendi.

### v1.5.2
* **Güvenlik:** Ayar dosyası (settings.json), veri güvenliği için NVDA'nın kullanıcı yapılandırma klasörüne taşındı.
* **İyileştirme:** Ayar dosyası artık okunabilir (girintili) JSON formatında kaydediliyor.

### v1.5
* **Mimari Değişikliği:** Kod yapısı tek dosyadan çıkarılıp, profesyonel modüler bir yapıya geçirildi.
* **Yeni Özellik:** "Seçenekler" menüsü eklendi.
* **Yeni Özellik:** Ayarlar gelişmiş bir pencereye taşındı.
* **Güvenlik:** API Anahtarı giriş alanı maskelendi ve "Göster/Gizle" butonu eklendi.
* **Yeni Özellik:** "Yeni mesaj geldiğinde odağı son mesaja taşı" ayarı eklendi.
* **Yeni Özellik:** "Varsayılana Döndür" butonu eklendi.
* **Kolaylık:** API Rehberi penceresine tek tıkla "Google Cloud Console'u Tarayıcıda Aç" butonu eklendi.

### v1.4
* Pencere taşıma ve boyutlandırma sorunu giderildi.
* Sohbet listesine yatay kaydırma çubuğu eklendi.
* Mesajlarda zaman damgasını açıp kapatma ayarı eklendi.

### v1.3
* Sürüm geçmişi özelliği eklendi.

### v1.2
* Web sitesine yönlendiren telif hakkı butonu eklendi.
* Dinamik yıl hesaplama özelliği eklendi.

### v1.1
* Super Chat, Super Sticker ve Üyelik bildirimleri desteği eklendi.
* Ayarları hatırlama özelliği eklendi.

### v1.0
* İlk sürüm yayınlandı.

## İletişim ve Sosyal Medya

Projelerimizden haberdar olmak, destek almak veya bizimle iletişime geçmek için aşağıdaki bağlantıları kullanabilirsiniz:

* **Web Sitesi:** https://erdoganteknoloji.com.tr/
* **YouTube Kanalı:** https://youtube.com/@erdoganteknoloji/
* **Instagram Hesabı:** https://instagram.com/erdoganteknoloji/
* **WhatsApp Kanalı:** https://www.whatsapp.com/channel/0029VaAHWDT7DAWvB9s8A406/
* **E-Posta :** erdoganteknoloji.com@gmail.com

---

# English : Youtube Live Stream Chat Client for NVDA

This plugin allows visually impaired users to track chat streams, Super Chat donations, Super Sticker submissions, and channel membership notifications in YouTube live broadcasts through the NVDA screen reader via a fully accessible interface. Running fully compatible with NVDA 2026.1 and later 64-bit versions, this client pulls data silently in the background without affecting your system performance, offering an uninterrupted experience. It includes advanced features such as automatic reading of new messages, adding timestamps to messages, automatic focusing on the list, and personalizable API request intervals. It also features comprehensive multi-language support including Turkish, English, and German.

> ⚠️ **Important Recommendation:** It is highly recommended to install the latest, secure, and stable version of the add-on directly from the **NVDA Add-on Store** by searching for "Youtube Chat Client For NVDA". Installing through the store ensures that you will receive future updates automatically.

## Installation and First Steps

### Plugin Download Link (Manual Installation) :
https://github.com/AdemErdogan007/YoutubeChatClientForNVDA/releases/download/V1.7/Youtube-Chat-Client-For-NVDA-V1.7.nvda-addon

* Run the plug-in you downloaded while NVDA is open and answer the warning with "Yes".
* Once the installation is complete, you will be asked to restart NVDA. The add-on will automatically detect NVDA's language (Turkish, English, or German).
* Run the plug-in by pressing <kbd> NVDA + Shift + CTRL + Y </kbd> or from the NVDA Tools menu.
* You will be asked to enter the API Key at first startup. It will automatically redirect you to the Settings window.
* Paste the YouTube Data v3 API key you received from Google Cloud Console here and press the **"Save Settings"** button.

## How to Get YouTube Data API v3 Key? (Detailed Guide)

This guide explains step-by-step how to get the free API key required for the add-on to connect to YouTube chats. Even if you have no technical knowledge, you can easily create your key by following these steps in order. Note : Do not share your API key with anyone.

### Step 1: Logging into Google Cloud Platform
* Click the "Open Google Cloud Console in Browser" button in the add-on or go to "https://console.cloud.google.com" from your browser.
* Log in with an existing Google (Gmail) account. If you are entering the system for the first time, a contract or welcome screen may appear, accept and continue.

### Step 2: Creating a New Project
* Click the "Select a project" button at the top of the screen, then find and press the "New Project" button in the upper right corner of the opening window.
* Type a simple name that you will remember for the add-on in the "Project Name" field (e.g., "NVDA Youtube Chat").
* Press the "Create" button at the bottom. Project creation may take a few seconds, wait for it to complete.

### Step 3: Enabling the YouTube API
* Once your project is created, click on "APIs & Services" from the left navigation menu, then click on the "Library" tab.
* Type "YouTube Data API v3" into the search box that appears and search.
* Click on the "YouTube Data API v3" link from the search results.
* Press the "Enable" button on the page that opens. This process will authorize your created project to fetch YouTube live chat data.

### Step 4: Generating the API Key
* After the API is enabled, click on the "Credentials" tab on the page you are redirected to or on the left menu.
* Press the "Create Credentials" button at the top of the screen.
* Select the "API Key" option from the small dropdown menu.

### Step 5: Copying and Adding the Key to the Add-on
* A window titled "API Key Created" will open on the screen, and a complex, long code starting with the letters "AIza" will appear.
* This long text is your API key. Copy it by pressing the copy button next to the text or by selecting the text completely.
* Now go back to the NVDA add-on settings, paste this key into the "Google API Key" box, and save the settings.

> 🔒 **IMPORTANT SECURITY NOTE:** This key is completely unique to you. Please do not share it with others or on open platforms. Google offers this service completely free of charge for personal use, and the daily quota allocated for the add-on to pull messages is more than enough for personal use.

## Main Window Usage

* **URL Field:** Paste the link of the YouTube live stream you want to follow here.
* **Options Menu:** You can quickly access all sub-windows such as Settings, Version History, API Guide, About, and Website from this menu.
* **Start/Stop:** Starts or stops the chat stream. The stream runs in the background without straining NVDA.
* **Chat List:** Incoming messages drop here as an accessible list. You can navigate between messages with the arrow keys.

## Settings Menu

* **API Key:** Appears masked (starred) for security reasons. You can read the content with the "Show" button and clear it instantly with the "Delete" button.
* **Timestamp:** Determines whether the sending time will be written at the beginning of the messages.
* **Automatic Voiceover:** Controls whether the screen reader automatically reads a new message when it arrives.
* **Move Focus to Last Message:** (Important!) If you are moving up the list to read old messages, turn this setting off. If it is on, the screen reader forces the focus to the very end of the list with each new message.
* **API Request Time:** Determines how many seconds data will be pulled from YouTube servers (Default is 10 seconds). If you keep this value too low, your daily API limit will expire in a very short time. It is recommended to use between 5 and 15 seconds.
* **Return to Defaults:** Resets all changes you made and returns the settings to the initial installation state.

## Version History (Changelog)

### v1.7 (2026.06.06)
* **Architecture Update:** The add-on has been made 100% compatible with NVDA 2026.1, 64-Bit architecture, and Python 3.13 standards.
* **Improvement:** All interface and dialog components have been updated according to the highest WCAG accessibility standards for screen readers.
* **Fix:** Fixed an invalid "PostPopup" invocation error that caused NVDA to crash when opening the main chat window and after saving settings.
* **Improvement:** The code infrastructure has been transitioned to a strict modular structure, completely isolating the interface (front-end) and core (back-end) logic.
* **Improvement:** All variable, function, class, and file names have been reorganized according to PascalCase standards without Turkish characters.
* **Update:** Detailed Turkish explanations have been added for every single line without exception across the code architecture, maximizing developer readability.
* **Update:** The API key acquisition guide has been thoroughly updated.
* **Update:** Readme file visually improved and contact information added.

### v1.6
* **New Feature:** Added full multi-language support (Turkish, English, and German).
* **Improvement:** Integrated an advanced language management system that automatically and accurately detects the add-on language according to NVDA's language.
* **Fix:** Resolved a memory management (Garbage Collection) issue that sometimes caused windows not to appear on the screen.
* **Fix:** Circular import errors in the code architecture were completely cleaned.

### v1.5.2
* **Security:** The settings file (settings.json) was moved to NVDA's user configuration folder for data security.
* **Improvement:** The settings file is now saved in a readable (indented) JSON format.

### v1.5
* **Architecture Change:** The code structure was removed from a single file and transitioned into a professional modular structure.
* **New Feature:** Added "Options" menu.
* **New Feature:** Settings moved to an advanced window.
* **Security:** API Key input field masked and "Show/Hide" button added.
* **New Feature:** Added "Move focus to last message when a new message arrives" setting.
* **New Feature:** Added "Return to Defaults" button.
* **Convenience:** Added a one-click "Open Google Cloud Console in Browser" button to the API Guide window.

### v1.4
* Window moving and resizing issue resolved.
* Horizontal scrollbar added to the chat list.
* Added setting to toggle timestamp in messages.

### v1.3
* Version history feature added.

### v1.2
* Added copyright button redirecting to the website.
* Added dynamic year calculation feature.

### v1.1
* Added support for Super Chat, Super Sticker, and Membership notifications.
* Added feature to remember settings.

### v1.0
* Initial version released.

## Contact and Social Media

You can use the links below to stay informed about our projects, get support, or contact us:

* **Website:** https://erdoganteknoloji.com.tr/
* **YouTube Channel:** https://youtube.com/@erdoganteknoloji/
* **Instagram Account:** https://instagram.com/erdoganteknoloji/
* **WhatsApp Channel:** https://www.whatsapp.com/channel/0029VaAHWDT7DAWvB9s8A406/
* **E-Posta :** erdoganteknoloji.com@gmail.com
