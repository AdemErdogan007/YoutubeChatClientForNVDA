# utils.py - Ortak Araçlar ve MANUEL Dil Yönetimi

import wx
import os
import json
import webbrowser
import shutil
import globalVars
import gettext  # Python'un standart çeviri kütüphanesi
import languageHandler # NVDA'nın dilini öğrenmek için
from datetime import datetime

# --- SABİTLER ---
YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3/"

# --- AYAR DOSYASI YOLLARI ---
OLD_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "settings.json")
CONFIG_FILE = os.path.join(globalVars.appArgs.configPath, "YoutubeChatClient_Settings.json")

# --- MANUEL ÇEVİRİ SİSTEMİ ---
def _(msg):
    """
    NVDA'nın addonHandler'ını atlayarak doğrudan locale klasöründen
    dil dosyasını okuyan sağlam fonksiyon.
    """
    try:
        # 1. Klasör yollarını hesapla
        # Mevcut dosya: .../addons/YoutubeChatClient/globalPlugins/YoutubeChatClient/utils.py
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # İki üst klasöre çıkıp 'locale' klasörünü buluyoruz:
        # .../addons/YoutubeChatClient/locale
        addon_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
        locale_path = os.path.join(addon_root, "locale")

        # 2. Kullanıcının dilini öğren (Örn: 'en_US', 'tr_TR')
        lang = languageHandler.getLanguage()
        lang_base = lang.split('_')[0] # Sadece 'en' veya 'tr' kısmı
        
        # 3. Çeviriyi yüklemeyi dene
        # Önce tam dile (en_US) bakar, bulamazsa ana dile (en) bakar.
        # domain='nvda' -> nvda.mo dosyasını arar.
        t = gettext.translation('nvda', localedir=locale_path, languages=[lang, lang_base], fallback=True)
        
        # 4. Çevrilmiş metni döndür
        return t.gettext(msg)
        
    except Exception as e:
        # Herhangi bir hata olursa (dosya yoksa vb.) orijinal metni döndür
        return msg
# -----------------------------

def check_and_migrate_settings():
    if os.path.exists(OLD_CONFIG_FILE) and not os.path.exists(CONFIG_FILE):
        try:
            shutil.move(OLD_CONFIG_FILE, CONFIG_FILE)
        except:
            try: shutil.copy2(OLD_CONFIG_FILE, CONFIG_FILE); os.remove(OLD_CONFIG_FILE)
            except: pass

def read_doc_file(filename):
    base_path = os.path.dirname(__file__)
    doc_root = os.path.abspath(os.path.join(base_path, "..", "..", "doc"))
    lang = languageHandler.getLanguage()
    langs_to_try = [lang, lang.split('_')[0], 'en', 'tr']
    
    for l in langs_to_try:
        file_path = os.path.join(doc_root, l, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception as e: return f"Hata: {e}"
    return f"Dosya bulunamadı: {filename}"

def open_readme():
    base_path = os.path.dirname(__file__)
    doc_root = os.path.abspath(os.path.join(base_path, "..", "..", "doc"))
    lang = languageHandler.getLanguage()
    langs_to_try = [lang, lang.split('_')[0], 'en', 'tr']
    for l in langs_to_try:
        file_path = os.path.join(doc_root, l, "readme.html")
        if os.path.exists(file_path):
            webbrowser.open(f"file://{file_path}")
            return

def load_settings():
    if not os.path.exists(CONFIG_FILE) and os.path.exists(OLD_CONFIG_FILE):
        check_and_migrate_settings()
    default = { "api_key": "", "auto_read": True, "refresh_rate": 10, "show_timestamp": False, "focus_last": False }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return {**default, **json.load(f)}
        except: pass
    return default

class BaseDialog(wx.Dialog):
    def __init__(self, parent, title, size):
        super(BaseDialog, self).__init__(parent, title=title, size=size, style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX)
        self.Center()

    def add_copyright(self, sizer, panel):
        sizer.Add(wx.StaticLine(panel), 0, wx.EXPAND | wx.ALL, 5)
        current_year = datetime.now().year
        base_year = 2025
        year_str = str(base_year) if current_year <= base_year else f"{base_year} / {current_year}"
        text = _("Copyright © {year}, ADEM ERDOĞAN (ERDOĞAN TEKNOLOJİ VE PROGRAMCILIK)").format(year=year_str)
        btn = wx.Button(panel, label=text)
        btn.Bind(wx.EVT_BUTTON, lambda e: webbrowser.open("https://erdoganteknoloji.com/"))
        sizer.Add(btn, 0, wx.EXPAND | wx.ALL, 2)