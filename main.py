from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.navigationdrawer import MDNavigationDrawer, NavigationLayout
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.label import MDLabel
from kivymd.uix.list import OneLineIconListItem, MDList, IconLeftWidget
from kivymd.theming import ThemableBehavior
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image


class MyMDLabel(MDLabel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = self.texture_size[1]


class ContentNavigationDrawer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = "8dp"
        self.spacing = "16dp"
        al = AnchorLayout(anchor_x="left", size_hint_y=None)
        img = Image(size_hint=(None, None), size=("56dp", "56dp"), source="data/logo.png")
        al.height = img.height
        al.add_widget(img)
        scrollview = ScrollView()
        scrollview.add_widget(DrawerList())
        self.add_widget(al)
        self.add_widget(MyMDLabel(text='test app', font_style='Button'))
        self.add_widget(MyMDLabel(text='testemail@gmail.com', font_style='Caption'))
        self.add_widget(scrollview)


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))
    theme_text_color = "Custom"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(IconLeftWidget(icon=self.icon, theme_text_color="Custom", text_color=self.text_color))

    def on_release(self):
        self.parent.set_color_item(self)


class DrawerList(ThemableBehavior, MDList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        icons_item = {
            "folder": "My files",
            "account-multiple": "Shared with me",
            "star": "Starred",
            "history": "Recent",
            "checkbox-marked": "Shared with me",
            "upload": "Upload",
        }
        for icon_name in icons_item.keys():
            self.add_widget(ItemDrawer(icon=icon_name, text=icons_item[icon_name]))

    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""
        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class MainScreen(Screen):
    def __init__(self, nav_drawer, **kw):
        super().__init__(**kw)
        self.nav_drawer = nav_drawer

    def on_enter(self, *args):
        root = BoxLayout(orientation='vertical')
        toolbar = MDToolbar(title='Меню')
        toolbar.right_action_items = [["dots-vertical", lambda x: self.nav_drawer.set_state('toggle')]]
        root.add_widget(toolbar)
        root.add_widget(Widget())
        self.add_widget(root)


class MobileShop(MDApp):
    def build(self):
        nav_lay = NavigationLayout()
        nav_drawer = MDNavigationDrawer()
        nav_drawer.add_widget(ContentNavigationDrawer())
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main_menu', nav_drawer=nav_drawer))
        sm.current = 'main_menu'
        nav_lay.add_widget(sm)
        nav_lay.add_widget(nav_drawer)
        return nav_lay


MobileShop().run()
