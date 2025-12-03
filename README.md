# YoutubeChatClientForNVDA
NVDA için erişilebilir YouTube Canlı Yayın Sohbet İstemcisi. / Accessible YouTube Live Stream Chat Client for NVDA.

<!DOCTYPE html>
<html lang="tr">
	<head>
		<meta charset="UTF-8">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
		<title>
			YouTube Canlı Sohbet İstemcisi - Yardım 
		</title>
		<link rel="stylesheet" href="style.css">
	</head>
	
	<body>
		<div class="container">
			<h1>
				YouTube Canlı Sohbet İstemcisi
			</h1>
			<p class="intro">
				Bu eklenti, YouTube canlı yayınlarındaki sohbet mesajlarını, Super Chat bağışlarını ve üyelik olaylarını erişilebilir bir arayüz ile takip etmenizi sağlar.
			</p>

			<div class="card">
				<h2>
					Kurulum ve İlk Adımlar
				</h2>
				<ol>
					<li>
						Eklentiyi yükledikten sonra NVDA'yı yeniden başlatın.
					</li>
					<li>
						<kbd> NVDA + Shift + CTRL + Y </kbd> tuşlarına basarak veya NVDA Araçlar menüsünden eklentiyi çalıştırın.
					</li>
					<li>
						İlk açılışta <strong> API Anahtarı </strong> girmeniz istenecektir. Sizi otomatik olarak Ayarlar penceresine yönlendirir.
					</li>
					<li>
						Google Cloud Console'dan aldığınız YouTube Data v3 API anahtarını buraya yapıştırın ve <strong> "Ayarları Kaydet" </strong> butonuna basın.
					</li>
				</ol>
			</div>

			<div class="card">
				<h2>
					Ana Pencere Kullanımı
				</h2>
				<ul>
					<li>
						<strong> URL Alanı: </strong> Takip etmek istediğiniz yayının linkini buraya yapıştırın.
					</li>
					<li>
						<strong> Seçenekler Menüsü: </strong> Ayarlar, Sürüm Geçmişi, API Rehberi, Hakkında ve Web Sitesi butonlarına bu menüden ulaşabilirsiniz.
					</li>
					<li>
						<strong> Başlat/Durdur: </strong> Sohbet akışını kontrol eder.
					</li>
					<li>
						<strong> Sohbet Listesi: </strong> Mesajlar buraya düşer. Yön tuşları ile gezebilirsiniz.
					</li>
				</ul>
			</div>

			<div class="card">
				<h2>
					Ayarlar Menüsü
				</h2>
				<ul>
					<li>
						<strong> API Anahtarı: </strong> Güvenlik gereği yıldızlı görünür. "Göster" butonu ile içeriği görebilir, "Sil" butonu ile temizleyebilirsiniz.
					</li>
					<li>
						<strong> Zaman Damgası: </strong> Mesajların başında saatin yazıp yazmayacağını belirler.
					</li>
					<li>
						<strong> Otomatik Seslendirme: </strong> Yeni mesaj geldiğinde NVDA'nın otomatik okuyup okumayacağını belirler.
					</li>
					<li>
						<strong> Odağı Son Mesaja Taşı: </strong>
						<span class="important"> Önemli! </span> Eğer eski mesajları inceliyorsanız bunu kapatın.
						<br>
						Açık olursa her yeni mesajda imleç en alta atar.
					</li>
					<li>
						<strong> API İstek Süresi: </strong> YouTube'dan verilerin kaç saniyede bir çekileceğini belirler (Varsayılan 10 saniye).
					</li>
					<li>
						<strong> Varsayılanlara Dön: </strong> Tüm ayarları ilk kurulum haline getirir.
					</li>
				</ul>
			</div>

			<div class="footer">
				<p>
					<strong> Geliştirici: </strong> ADEM ERDOĞAN (ERDOĞAN TEKNOLOJİ VE PROGRAMCILIK).
				</p>
				<p>
					<a href="https://erdoganteknoloji.com/" class="copyright-link" target="_blank">
						Copyright © <span id="copyright-year"> 2025 </span> ADEM ERDOĞAN (ERDOĞAN TEKNOLOJİ VE PROGRAMCILIK) Tüm Hakları Saklıdır.
					</a>
				</p>
			</div>
		</div>

		<script>
			const currentYear = new Date().getFullYear();
			const baseYear = 2025;
			const yearSpan = document.getElementById('copyright-year');
			
			if (currentYear > baseYear)
			{
				yearSpan.textContent = baseYear + " / " + currentYear;
			}
			else
			{
				yearSpan.textContent = baseYear;
			}
		</script>
	</body>
</html>
