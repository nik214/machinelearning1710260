import sys
import os
# os.environ["KIVY_NO_CONSOLELOG"] = '1'

from kivy.config import Config

Config.set('kivy', 'exit_on_escape', '0')
from kivy.app import App
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.properties import ColorProperty
import json
from kivy.logger import Logger
from kivymd.app import MDApp
from tokens import cmc_token


class ChatBot(MDApp):
    name = "Chat Bot"
    theme = 'Light'
    bg_color = ColorProperty([0.97, 0.97, 0.97, 1])
    text_color = ColorProperty([0, 0, 0, 1])

    def build(self):
        self.title = "Bitbot"
        self.app_settings_folder = os.path.join(getattr(self, 'user_data_dir'), 'database')
        self.app_settings = os.path.join(self.app_settings_folder, 'config.json')
        self.logger = Logger

        from screens.home import home
        from screens.chat import chat

        self.root = ScreenManager()
        self.home = home.Home()
        self.chat = chat.Chat()
        self.screens = {
            "home": self.home,
            "chat": self.chat,
        }
        self.screen_history = []
        Window.bind(on_key_up=self.back_button)
        Window.softinput_mode = "below_target"
        self.root.transition = NoTransition()
        self.get_theme()
        self.switch_screen("home")

    def on_pause(self):
        self.set_theme()

    def on_stop(self):
        self.set_theme()

    def switch_screen(self, screen_name):
        self.root.switch_to(self.screens.get(screen_name))
        self.screen_history.append(screen_name)

    def back_button(self, instance, keyboard, *args):
        if keyboard in (1001, 27):
            self.screen_history.pop()
            if self.screen_history != []:
                self.root.switch_to(self.screens.get(self.screen_history[-1]))
            else:
                self.stop()
            return True

    def get_theme(self):
        if os.path.exists(self.app_settings):
            try:
                with open(self.app_settings, 'r') as fp:
                    self.theme = json.load(fp).get("theme")
            except BaseException as e:
                self.logger.error(e)
        else:
            if not os.path.isdir(self.app_settings_folder):
                os.makedirs(self.app_settings_folder)
            self.set_theme()
        if self.theme == "Dark":
            self.home.ids.theme_switch.active = True
        elif self.theme == "Light":
            pass

    def set_theme(self):
        try:
            with open(self.app_settings, 'w+') as fp:
                json.dump({"theme": self.theme}, fp)
        except BaseException as e:
            self.logger.error(e)

    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(os.path.dirname(sys.argv[0]))

        return os.path.join(base_path, relative_path)


resource_add_path(ChatBot.resource_path(os.path.join('screens', 'home')))
resource_add_path(ChatBot.resource_path(os.path.join('screens', 'chat')))

if __name__ == "__main__":
    ChatBot().run()
