# Settings_Window.py - Ayarlar Penceresi

import wx
import json
import ui
import gui
# DİKKAT: _ fonksiyonunu utils'ten çekiyoruz
from .utils import BaseDialog, load_settings, CONFIG_FILE, _
from .How_to_Use_Window import ApiGuideDialog

class SettingsDialog(BaseDialog):
    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent, _("Ayarlar - Youtube Canlı Sohbet İstemcisi"), (550, 450))
        self.settings = load_settings()
        self.init_ui()

    def init_ui(self):
        self.panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # --- API ---
        sb_api = wx.StaticBox(self.panel, label=_("API Yapılandırması"))
        sb_sizer_api = wx.StaticBoxSizer(sb_api, wx.VERTICAL)
        
        sb_sizer_api.Add(wx.StaticText(self.panel, label=_("Google API Anahtarı:")), 0, wx.EXPAND | wx.ALL, 5)
        
        self.hbox_key = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_api = wx.TextCtrl(self.panel, value=self.settings["api_key"], style=wx.TE_PASSWORD)
        self.hbox_key.Add(self.txt_api, 1, wx.EXPAND | wx.RIGHT, 5)
        
        self.btn_toggle = wx.Button(self.panel, label=_("Göster"))
        self.btn_toggle.Bind(wx.EVT_BUTTON, self.on_toggle_key)
        self.hbox_key.Add(self.btn_toggle, 0, wx.RIGHT, 5)

        self.btn_clear = wx.Button(self.panel, label=_("Sil"))
        self.btn_clear.Bind(wx.EVT_BUTTON, self.on_clear_key)
        self.hbox_key.Add(self.btn_clear, 0)
        
        sb_sizer_api.Add(self.hbox_key, 0, wx.EXPAND | wx.ALL, 5)
        
        btn_guide = wx.Button(self.panel, label=_("API Anahtarı Nasıl Alınır?"))
        btn_guide.Bind(wx.EVT_BUTTON, lambda e: ApiGuideDialog(self).ShowModal())
        sb_sizer_api.Add(btn_guide, 0, wx.ALL, 5)
        
        vbox.Add(sb_sizer_api, 0, wx.EXPAND | wx.ALL, 10)

        # --- Genel ---
        sb_gen = wx.StaticBox(self.panel, label=_("Genel Ayarlar"))
        sb_sizer_gen = wx.StaticBoxSizer(sb_gen, wx.VERTICAL)

        self.chk_timestamp = wx.CheckBox(self.panel, label=_("Sohbet mesajlarında zaman damgasını göster"))
        self.chk_timestamp.SetValue(self.settings["show_timestamp"])
        sb_sizer_gen.Add(self.chk_timestamp, 0, wx.ALL, 5)

        self.chk_auto_read = wx.CheckBox(self.panel, label=_("Yeni gelen mesajları seslendir"))
        self.chk_auto_read.SetValue(self.settings["auto_read"])
        sb_sizer_gen.Add(self.chk_auto_read, 0, wx.ALL, 5)
        
        self.chk_focus_last = wx.CheckBox(self.panel, label=_("Yeni mesaj geldiğinde odağı son mesaja taşı"))
        self.chk_focus_last.SetValue(self.settings["focus_last"])
        sb_sizer_gen.Add(self.chk_focus_last, 0, wx.ALL, 5)

        hbox_refresh = wx.BoxSizer(wx.HORIZONTAL)
        hbox_refresh.Add(wx.StaticText(self.panel, label=_("API İstek Süresi (Saniye):")), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.spin_rate = wx.SpinCtrl(self.panel, value=str(self.settings["refresh_rate"]), min=3, max=60)
        hbox_refresh.Add(self.spin_rate, 0)
        sb_sizer_gen.Add(hbox_refresh, 0, wx.ALL, 5)

        vbox.Add(sb_sizer_gen, 0, wx.EXPAND | wx.ALL, 10)

        # --- Butonlar ---
        hbox_actions = wx.BoxSizer(wx.HORIZONTAL)
        btn_save = wx.Button(self.panel, label=_("Ayarları Kaydet"))
        btn_save.Bind(wx.EVT_BUTTON, self.on_save)
        hbox_actions.Add(btn_save, 1, wx.RIGHT, 5)
        
        btn_reset = wx.Button(self.panel, label=_("Varsayılana Döndür"))
        btn_reset.Bind(wx.EVT_BUTTON, self.on_reset)
        hbox_actions.Add(btn_reset, 1, wx.LEFT, 5)
        
        vbox.Add(hbox_actions, 0, wx.EXPAND | wx.ALL, 10)
        vbox.AddStretchSpacer() 
        self.add_copyright(vbox, self.panel)
        self.panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_escape)

    def on_toggle_key(self, event):
        val = self.txt_api.GetValue()
        is_showing = self.btn_toggle.GetLabel() == _("Gizle (*)")
        new_style = 0 if not is_showing else wx.TE_PASSWORD
        new_label = _("Gizle (*)") if not is_showing else _("Göster")
        
        self.hbox_key.Detach(self.txt_api)
        self.txt_api.Destroy()
        self.txt_api = wx.TextCtrl(self.panel, value=val, style=new_style)
        self.hbox_key.Insert(0, self.txt_api, 1, wx.EXPAND | wx.RIGHT, 5)
        self.btn_toggle.SetLabel(new_label)
        self.panel.Layout()
        self.txt_api.SetFocus()

    def on_clear_key(self, event):
        self.txt_api.SetValue("")

    def on_save(self, event):
        new_settings = {
            "api_key": self.txt_api.GetValue().strip(),
            "show_timestamp": self.chk_timestamp.GetValue(),
            "auto_read": self.chk_auto_read.GetValue(),
            "focus_last": self.chk_focus_last.GetValue(),
            "refresh_rate": self.spin_rate.GetValue()
        }
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(new_settings, f, indent=4, ensure_ascii=False)
            
            ui.message(_("Ayarlar kaydedildi."))
            self.Destroy()
            
            from .Main_Window import YouTubeChatDialog
            main_window_open = False
            for child in gui.mainFrame.GetChildren():
                if isinstance(child, YouTubeChatDialog):
                    child.settings = child.load_settings()
                    child.Raise()
                    child.SetFocus()
                    main_window_open = True
                    break
            
            if not main_window_open:
                gui.mainFrame.prePopup()
                dlg = YouTubeChatDialog(gui.mainFrame)
                dlg.Show()
                dlg.PostPopup()

        except Exception as e:
            ui.message(f"Hata: {e}")

    def on_reset(self, event):
        self.txt_api.SetValue("")
        self.chk_timestamp.SetValue(False)
        self.chk_auto_read.SetValue(True)
        self.chk_focus_last.SetValue(False)
        self.spin_rate.SetValue(10)
        self.on_save(None)

    def on_escape(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE: self.Destroy()
        else: event.Skip()