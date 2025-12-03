# Türkçe : NVDA İçin Youtube Canlı Yayın Sohbet İstemcisi

Bu eklenti, YouTube canlı yayınlarındaki sohbet mesajlarını, Super Chat bağışlarını ve üyelik olaylarını erişilebilir bir arayüz ile takip etmenizi sağlar.

## Kurulum ve İlk Adımlar

### Eklenti İndirme Bağlantısı : 
https://github.com/AdemErdogan007/YoutubeChatClientForNVDA/releases/download/V1.6/Youtube-Chat-Client-For-NVDA-V1.6.nvda-addon

İndirdiğiniz eklentiyi NVDA açıkken çalıştırın ve gelen uyarıyı "Evet" olarak yanıtlayın.

Kurulum tamamlandığında NVDA'yı yeniden başlatmanız istenecektir.

"Evet" seçeneğini tıklayın ve NVDA yeniden başlasın.

NVDA + Shift + CTRL + Y tuşlarına basarak veya NVDA Araçlar menüsünden eklentiyi çalıştırın.

İlk açılışta API Anahtarı girmeniz istenecektir.

Sizi otomatik olarak Ayarlar penceresine yönlendirir.

Google Cloud Console'dan aldığınız YouTube Data v3 API anahtarını buraya yapıştırın ve "Ayarları Kaydet" butonuna basın.

API anahtarını nasıl alacağınızı bilmiyorsanız "API Anahtarı Nasıl Alınır" adlı butona tıklayın ve açılan pencerede ki rehberi inceleyin.

## Ana Pencere Kullanımı

### URL Alanı :

Takip etmek istediğiniz yayının linkini buraya yapıştırın.

### Seçenekler Menüsü :

Ayarlar, Sürüm Geçmişi, API Rehberi, Hakkında ve Web Sitesi adlı menü elemanlarına bu menüden ulaşabilirsiniz.

### Başlat/Durdur :

Sohbet akışını kontrol eder.

### Sohbet Listesi :

Mesajlar buraya düşer.

Yön tuşları ile gezebilirsiniz.

## Ayarlar Penceresi

### API Anahtarı :

Güvenlik gereği yıldızlı görünür.

"Göster" butonu ile içeriği görebilir, "Sil" butonu ile temizleyebilirsiniz.

### Zaman Damgası :

Mesajların başında saatin yazıp yazmayacağını belirler.

### Otomatik Seslendirme :

Yeni mesaj geldiğinde NVDA'nın otomatik okuyup okumayacağını belirler.

### Odağı Son Mesaja Taşı :

Önemli! Eğer eski mesajları inceliyorsanız bunu kapatın.

Açık olursa her yeni mesajda imleç en sona gider.

### API İstek Süresi :

YouTube'dan verilerin kaç saniyede bir çekileceğini belirler (Varsayılan 10 saniye).

### Varsayılanlara Dön :

Tüm ayarları ilk kurulum haline getirir.


# English : Youtube Live Stream Chat Client for NVDA

This plugin allows you to track chat messages, Super Chat donations, and membership events in YouTube live broadcasts with an accessible interface.

## Installation and First Steps

### Plugin Download Link :

https://github.com/AdemErdogan007/YoutubeChatClientForNVDA/releases/download/V1.6/Youtube-Chat-Client-For-NVDA-V1.6.nvda-addon

Run the plug-in you downloaded while NVDA is open and answer the warning with "Yes".

Once the installation is complete, you will be asked to restart NVDA.

Click "Yes" and NVDA will restart.

Run the plug-in by pressing NVDA + Shift + CTRL + Y or from the NVDA Tools menu.

You will be asked to enter the API Key at first startup.

It will automatically redirect you to the Settings window.

Paste the YouTube Data v3 API key you received from Google Cloud Console here and press the "Save Settings" button.

If you do not know how to get the API key, click on the button called "How to Get API Key" and review the guide in the window that opens.

## Main Window Usage

### URL Field :

Paste the link of the publication you want to follow here.

### Options Menu :

You can access the menu elements called Settings, Version History, API Guide, About and Website from this menu.

### Start/Stop :

Controls the chat flow.

### Chat List :

Messages drop here.

You can navigate with the arrow keys.

## Settings Window

### API Key :

It appears with a star for security reasons.

You can see the content with the "Show" button and clear it with the "Delete" button.

### Timestamp :

It determines whether the time will be written at the beginning of the messages.

### Automatic Voiceover :

Determines whether NVDA automatically reads a new message when it arrives.

### Move Focus to Last Message :

Important! If you are reviewing old messages, turn it off.

If on, the cursor moves to the end with each new message.

### API Request Time :

Determines how many seconds to pull data from YouTube (Default 10 seconds).

### Return to Defaults :

Returns all settings to initial setup.
