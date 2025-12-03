# Version_History_Window.py - Sürüm Geçmişi Penceresi

import wx
# DİKKAT: _ fonksiyonunu utils'ten çekiyoruz
from .utils import BaseDialog, read_doc_file, _

class VersionHistoryDialog(BaseDialog):
    def __init__(self, parent):
        # Başlık çevrildi
        super(VersionHistoryDialog, self).__init__(parent, _("Sürüm Geçmişi"), (500, 400))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Metin dosyası utils içindeki mantığa göre (tr/en) otomatik seçilecek
        text = read_doc_file("changelog.txt")
        
        txt_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2, value=text)
        vbox.Add(txt_ctrl, 1, wx.EXPAND | wx.ALL, 10)
        
        # Buton etiketi çevrildi
        btn_close = wx.Button(panel, id=wx.ID_OK, label=_("Kapat"))
        vbox.Add(btn_close, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        
        self.add_copyright(vbox, panel)
        panel.SetSizer(vbox)