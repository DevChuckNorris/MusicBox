from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty


class OverviewWidget(StackLayout):
    list = ObjectProperty(None)

    def __init__(self, **kwargs):
        StackLayout.__init__(self, **kwargs)
        self.ids.list.item_strings = ["Hallo 123", "Weil Baum"]
