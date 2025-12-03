# __init__.py - Eklenti Giriş Noktası

import globalPluginHandler
import gui
import wx
import ui
# DİKKAT: _ fonksiyonunu utils'ten çekiyoruz
from .utils import load_settings, check_and_migrate_settings, _
from .Main_Window import YouTubeChatDialog
from .Settings_Window import SettingsDialog

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    # Kategori ismini çeviriye uygun hale getirdik
    scriptCategory = _("Youtube Canlı Sohbet İstemcisi")

    def __init__(self):
        super(GlobalPlugin, self).__init__()
        try:
            check_and_migrate_settings()
        except Exception as e:
            globalPluginHandler.log.error(f"YoutubeChatClient Hata: {e}")

        wx.CallAfter(self.createMenu)

    def createMenu(self):
        try:
            self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
            # Menü öğelerini çeviri fonksiyonu içine aldık
            self.menuItem = self.toolsMenu.Append(wx.ID_ANY, 
                                                  _("Youtube Canlı Sohbet İstemcisi"), 
                                                  _("YouTube canlı sohbet penceresini açar"))
            gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onMenuCommand, self.menuItem)
        except Exception as e:
            globalPluginHandler.log.error(f"YoutubeChatClient Menü Hatası: {e}")

    def onMenuCommand(self, event):
        wx.CallAfter(self._check_and_show)

    def script_openChatDialog(self, gesture):
        wx.CallAfter(self._check_and_show)

    def _check_and_show(self):
        settings = load_settings()
        api_key = settings.get("api_key", "").strip()
        
        if not api_key:
            # Mesaj kutusundaki metinler çevrildi
            dlg = wx.MessageDialog(gui.mainFrame, 
                                   _("API Anahtarı bulunamadı. Ayarlar menüsüne gidip bir anahtar girmek ister misiniz?"),
                                   _("Eksik Yapılandırma"), wx.YES_NO | wx.ICON_WARNING)
            if dlg.ShowModal() == wx.ID_YES:
                self._open_window(SettingsDialog)
            dlg.Destroy()
        else:
            self._open_window(YouTubeChatDialog)

    def _open_window(self, window_class):
        for child in gui.mainFrame.GetChildren():
            if isinstance(child, window_class):
                child.Raise()
                child.SetFocus()
                return
        
        gui.mainFrame.prePopup()
        dlg = window_class(gui.mainFrame)
        dlg.Show()
        dlg.PostPopup()

    script_openChatDialog.__doc__ = _("YouTube Canlı Sohbet arayüzünü başlatır.")
    __gestures = {"kb:NVDA+shift+control+y": "openChatDialog"}

    def terminate(self):
        try: self.toolsMenu.Remove(self.menuItem)
        except: pass
        super(GlobalPlugin, self).terminate()