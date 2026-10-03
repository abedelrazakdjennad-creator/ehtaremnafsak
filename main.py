from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.utils import platform


class ConfirmCard(ModalView):

    def __init__(self, app, **kwargs):
        super().__init__(
            size_hint=(None, None),
            size=(340, 220),
            background_color=(0, 0, 0, 0.55),
            auto_dismiss=False,
            **kwargs
        )

        self.app = app

        box = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=15
        )

        message = Label(
            text="هل تريد تفعيله كمسؤول والسماح له بهذه الأشياء؟",
            font_size="18sp",
            halign="center",
            valign="middle"
        )

        buttons = BoxLayout(
            orientation="horizontal",
            spacing=10,
            size_hint_y=None,
            height=55
        )

        yes = Button(
            text="نعم",
            font_size="18sp"
        )

        no = Button(
            text="لا",
            font_size="18sp"
        )

        yes.bind(on_release=self.accept)
        no.bind(on_release=self.reject)

        buttons.add_widget(yes)
        buttons.add_widget(no)

        box.add_widget(message)
        box.add_widget(buttons)

        self.add_widget(box)

    def accept(self, *args):
        self.dismiss()
        self.app.activate()

    def reject(self, *args):
        self.dismiss()


class MainApp(App):

    def build(self):

        self.enabled = False

        Window.clearcolor = (
            0.06,
            0.06,
            0.06,
            1
        )

        root = FloatLayout()

        self.button = Button(
            text="تفعيل",
            font_size="28sp",
            size_hint=(None, None),
            size=(220, 100),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.5
            }
        )

        self.button.bind(
            on_release=self.toggle
        )

        root.add_widget(
            self.button
        )

        return root

    def toggle(self, *args):

        if self.enabled:

            self.disable()

        else:

            card = ConfirmCard(self)
            card.open()

    def activate(self):

        if platform == "android":

            try:

                from android.permissions import (
                    request_permissions,
                    Permission
                )

                request_permissions([
                    Permission.RECORD_AUDIO
                ])

            except Exception as error:

                print(
                    "Permission error:",
                    error
                )

        self.enabled = True

        self.button.text = "إيقاف"

        self.start_background_service()

    def disable(self):

        self.enabled = False

        self.button.text = "تفعيل"

        self.stop_background_service()

    def start_background_service(self):

        if platform != "android":
            return

        try:

            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            Intent = autoclass(
                "android.content.Intent"
            )

            activity = PythonActivity.mActivity

            intent = Intent(
                activity,
                autoclass(
                    "org.kivy.android.PythonService"
                )
            )

            activity.startService(intent)

        except Exception as error:

            print(
                "Service start error:",
                error
            )

    def stop_background_service(self):

        if platform != "android":
            return

        try:

            from jnius import autoclass

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            print(
                "Background service stop requested"
            )

        except Exception as error:

            print(
                "Service stop error:",
                error
            )

    def on_stop(self):

        # لا نوقف الخدمة هنا،
        # لأن المطلوب أن تستمر بعد إغلاق التطبيق.
        pass


if __name__ == "__main__":
    MainApp().run()