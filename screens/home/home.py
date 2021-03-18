from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp
app = MDApp.get_running_app()


class Home(MDScreen):
    def change_theme(self, instance):
        if instance.active:
            app.text_color = [1, 1, 1, 1]
            app.bg_color = [0.12, 0.12, 0.12, 1]
            app.theme_cls.theme_style = "Dark"
            app.theme = "Dark"
        else:
            app.text_color = [0, 0, 0, 1]
            app.bg_color = [0.97, 0.97, 0.97, 1]
            app.theme_cls.theme_style = "Light"
            app.theme = "Light"
        app.set_theme()

Builder.load_file('home.kv')
