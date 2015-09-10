from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
from kivy.adapters.listadapter import ListAdapter
from kivy.properties import StringProperty


class SampleData(object):
    def __init__(self, name, artist):
        self.name = name
        self.artist = artist


class OverviewWidget(StackLayout):
    list = ObjectProperty(None)

    def __init__(self, **kwargs):
        StackLayout.__init__(self, **kwargs)

        list_item_args_converter = lambda row_index, obj: {
            'artist': obj.artist,
            'name': obj.name,
            'size_hint_y': None,
            'height': 25
        }

        # self.ids.list.item_strings = ["Test 123"]
        self.ids.list.adapter = ListAdapter(data=[SampleData("Test Song", "Test Artist")],
                                            template='OverviewEntry',
                                            args_converter=list_item_args_converter)
