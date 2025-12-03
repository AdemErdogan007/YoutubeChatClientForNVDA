# How_to_Use_Window.py - API Anahtarı Alma Rehberi Penceresi

import wx
import webbrowser
# DİKKAT: _ fonksiyonunu utils'ten çekiyoruz
from .utils import BaseDialog, read_doc_file, _

class ApiGuideDialog(BaseDialog):
    def __init__(self, parent):
        # Başlık çevrildi
        super(ApiGuideDialog, self).__init__(parent, _("API Anahtarı Alma Rehberi"), (600, 550))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Metin dosyası utils içindeki mantığa göre (tr/en) otomatik seçilecek
        text = read_doc_file("api_guide.txt")
        
        txt_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, value=text)
        vbox.Add(txt_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        # Konsol butonu çevrildi
        btn_console = wx.Button(panel, label=_("Google Cloud Console'u Tarayıcıda Aç"))
        btn_console.Bind(wx.EVT_BUTTON, lambda e: webbrowser.open("https://console.cloud.google.com/"))
        vbox.Add(btn_console, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        # Kapat butonu çevrildi
        btn_close = wx.Button(panel, id=wx.ID_OK, label=_("Kapat"))
        vbox.Add(btn_close, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        self.add_copyright(vbox, panel)
        panel.SetSizer(vbox)