from kivy.app import App
from overviewwidget import OverviewWidget


class MusicBoxApp(App):
    def build(self):
        return OverviewWidget()

if __name__ == '__main__':
    MusicBoxApp().run()
