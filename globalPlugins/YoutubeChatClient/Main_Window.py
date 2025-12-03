# Main_Window.py - Ana Sohbet Ekranı

import wx
import json
import threading
import time
import urllib.request
import urllib.parse
import speech
import ui
import addonHandler
import webbrowser
# DİKKAT: _ fonksiyonunu utils'ten çekiyoruz
from .utils import BaseDialog, load_settings, YOUTUBE_API_BASE, open_readme, _
from .Settings_Window import SettingsDialog
from .Version_History_Window import VersionHistoryDialog
from .How_to_Use_Window import ApiGuideDialog
from .About_Window import AboutDialog

class YouTubeChatDialog(BaseDialog):
    def __init__(self, parent):
        try:
            version = addonHandler.getCodeAddon().manifest.get("version", "1.0")
        except: version = "1.0"
        
        super(YouTubeChatDialog, self).__init__(parent, _("Youtube Canlı Sohbet İstemcisi - v{version}").format(version=version), (550, 700))
        
        self.is_running = False
        self.next_page_token = None
        self.last_messages = set()
        self.settings = load_settings()
        self.init_ui()

    def load_settings(self):
        return load_settings()

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # --- Üst Kısım ---
        hbox_top = wx.BoxSizer(wx.HORIZONTAL)
        hbox_top.AddStretchSpacer()
        self.btn_options = wx.Button(panel, label=_("Seçenekler"))
        self.btn_options.Bind(wx.EVT_BUTTON, self.on_options_menu)
        hbox_top.Add(self.btn_options, 0, wx.ALL, 5)
        vbox.Add(hbox_top, 0, wx.EXPAND)

        # --- URL ---
        vbox.Add(wx.StaticText(panel, label=_("YouTube Canlı Yayın URL'si:")), 0, wx.EXPAND | wx.ALL, 5)
        self.txt_url = wx.TextCtrl(panel)
        vbox.Add(self.txt_url, 0, wx.EXPAND | wx.ALL, 5)

        # --- Butonlar ---
        hbox_btns = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_start = wx.Button(panel, label=_("Sohbet Akışını Başlat"))
        self.btn_stop = wx.Button(panel, label=_("Sohbet Akışını Durdur"))
        self.btn_stop.Disable()
        self.btn_start.Bind(wx.EVT_BUTTON, self.on_start)
        self.btn_stop.Bind(wx.EVT_BUTTON, self.on_stop)
        
        hbox_btns.Add(self.btn_start, 1, wx.ALL, 5)
        hbox_btns.Add(self.btn_stop, 1, wx.ALL, 5)
        vbox.Add(hbox_btns, 0, wx.EXPAND | wx.ALL, 5)

        # --- Liste ---
        vbox.Add(wx.StaticText(panel, label=_("Sohbet Akışı:")), 0, wx.EXPAND | wx.ALL, 5)
        self.list_box = wx.ListBox(panel, style=wx.LB_SINGLE | wx.HSCROLL)
        vbox.Add(self.list_box, 1, wx.EXPAND | wx.ALL, 5)

        self.status_text = wx.StaticText(panel, label=_("Hazır."))
        vbox.Add(self.status_text, 0, wx.EXPAND | wx.ALL, 5)
        
        self.add_copyright(vbox, panel)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_escape)

    def on_options_menu(self, event):
        menu = wx.Menu()
        item_settings = menu.Append(wx.ID_ANY, _("Ayarlar"))
        self.Bind(wx.EVT_MENU, lambda e: self.open_dialog(SettingsDialog), item_settings)

        item_history = menu.Append(wx.ID_ANY, _("Sürüm Geçmişi"))
        self.Bind(wx.EVT_MENU, lambda e: self.open_dialog(VersionHistoryDialog), item_history)

        item_usage = menu.Append(wx.ID_ANY, _("Nasıl Kullanılır?"))
        self.Bind(wx.EVT_MENU, lambda e: open_readme(), item_usage)

        item_guide = menu.Append(wx.ID_ANY, _("API Anahtarı Nasıl Alınır?"))
        self.Bind(wx.EVT_MENU, lambda e: self.open_dialog(ApiGuideDialog), item_guide)

        item_about = menu.Append(wx.ID_ANY, _("Eklenti Hakkında"))
        self.Bind(wx.EVT_MENU, lambda e: self.open_dialog(AboutDialog), item_about)

        item_web = menu.Append(wx.ID_ANY, _("Web Sitesini Ziyaret Et"))
        self.Bind(wx.EVT_MENU, lambda e: webbrowser.open("https://erdoganteknoloji.com/"), item_web)
        
        self.PopupMenu(menu)
        menu.Destroy()

    def open_dialog(self, dialog_class):
        dlg = dialog_class(self)
        dlg.ShowModal()
        dlg.Destroy()
        if dialog_class == SettingsDialog:
            self.settings = self.load_settings()

    def on_escape(self, event):
        if event.GetKeyCode() == wx.WXK_ESCAPE: self.Destroy()
        else: event.Skip()

    def on_start(self, event):
        self.settings = self.load_settings()
        api_key = self.settings.get("api_key", "").strip()
        url = self.txt_url.GetValue().strip()
        
        if not api_key:
            ui.message(_("API Anahtarı eksik. Lütfen ayarlardan giriniz."))
            return
        
        video_id = self.get_video_id(url)
        if not url or not video_id:
            ui.message(_("Geçersiz YouTube URL'si."))
            return

        self.is_running = True
        self.btn_start.Disable()
        self.btn_stop.Enable()
        self.list_box.Clear()
        self.last_messages.clear()
        self.next_page_token = None
        refresh_rate = self.settings.get("refresh_rate", 10)
        threading.Thread(target=self.worker_thread, args=(api_key, video_id, refresh_rate), daemon=True).start()

    def on_stop(self, event):
        self.is_running = False
        self.btn_start.Enable()
        self.btn_stop.Disable()
        wx.CallAfter(self.status_text.SetLabel, _("Durduruldu."))

    def get_video_id(self, url):
        query = urllib.parse.urlparse(url)
        if query.hostname == 'youtu.be': return query.path[1:]
        if query.hostname in ('www.youtube.com', 'youtube.com'):
            if query.path == '/watch': return urllib.parse.parse_qs(query.query).get('v', [None])[0]
            if query.path[:7] == '/embed/': return query.path.split('/')[2]
            if query.path[:3] == '/v/': return query.path.split('/')[2]
        return None

    def worker_thread(self, api_key, video_id, interval):
        wx.CallAfter(self.status_text.SetLabel, _("Bağlanıyor..."))
        chat_id = self.fetch_live_chat_id(api_key, video_id)
        if not chat_id:
            wx.CallAfter(ui.message, _("Canlı sohbet bulunamadı."))
            wx.CallAfter(self.on_stop, None)
            return
        
        wx.CallAfter(self.status_text.SetLabel, _("Sohbet Bağlandı."))
        while self.is_running:
            try:
                self.fetch_messages(api_key, chat_id)
                time.sleep(interval)
            except Exception as e:
                time.sleep(interval * 2)

    def fetch_live_chat_id(self, api_key, video_id):
        url = f"{YOUTUBE_API_BASE}videos?part=liveStreamingDetails&id={video_id}&key={api_key}"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                items = data.get("items", [])
                if items: return items[0].get("liveStreamingDetails", {}).get("activeLiveChatId")
        except: pass
        return None

    def fetch_messages(self, api_key, chat_id):
        url = f"{YOUTUBE_API_BASE}liveChat/messages?liveChatId={chat_id}&part=snippet,authorDetails&key={api_key}"
        if self.next_page_token: url += f"&pageToken={self.next_page_token}"
        try:
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode('utf-8'))
                self.next_page_token = data.get("nextPageToken")
                new_messages = []
                show_time = self.settings.get("show_timestamp", False)

                for item in data.get("items", []):
                    if item["id"] not in self.last_messages:
                        snippet = item["snippet"]
                        author = item["authorDetails"]["displayName"]
                        msg_type = snippet.get("type")
                        t_str = snippet["publishedAt"][11:19]
                        display_text = ""
                        prefix = ""

                        if msg_type == "textMessageEvent": display_text = snippet.get("displayMessage", "")
                        elif msg_type == "superChatEvent":
                            d = snippet.get("superChatDetails", {})
                            prefix = f"[SUPER CHAT {d.get('amountDisplayString', '')}]"
                            display_text = d.get("userComment", "")
                        elif msg_type == "superStickerEvent":
                            d = snippet.get("superStickerDetails", {})
                            prefix = f"[SUPER STICKER {d.get('amountDisplayString', '')}]"
                            display_text = d.get("superStickerMetadata", {}).get("altText", "Sticker")
                        elif msg_type == "newSponsorEvent":
                            display_text = snippet.get("displayMessage", _("Yeni Üye Oldu!"))
                            prefix = _("[YENİ ÜYELİK]")
                        elif msg_type == "memberMilestoneChatEvent":
                            d = snippet.get("memberMilestoneChatDetails", {})
                            prefix = _("[ÜYELİK {month}. AY]").format(month=d.get('memberMonth', '?'))
                            display_text = d.get("userComment", "") or snippet.get("displayMessage", "")

                        if not display_text and not prefix: display_text = snippet.get("displayMessage", "")

                        if show_time: final_msg = f"[{t_str}] {prefix} {author}: {display_text}"
                        else: final_msg = f"{prefix} {author}: {display_text}"

                        new_messages.append(final_msg)
                        self.last_messages.add(item["id"])
                
                if new_messages: wx.CallAfter(self.update_list_ui, new_messages)
        except: pass

    def update_list_ui(self, messages):
        count = self.list_box.GetCount()
        selection = self.list_box.GetSelection()
        is_at_bottom = (selection == count - 1) or (selection == wx.NOT_FOUND)
        force_focus = self.settings.get("focus_last", False)
        auto_read = self.settings.get("auto_read", True)

        for msg in messages:
            self.list_box.Append(msg)
            if auto_read: speech.speakMessage(msg)
        
        if force_focus or is_at_bottom:
            self.list_box.SetSelection(self.list_box.GetCount() - 1)