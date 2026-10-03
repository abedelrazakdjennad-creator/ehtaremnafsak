# android_service.py

from jnius import autoclass


class AndroidService:

    def __init__(self):
        self.service = None

    def start(self):

        try:
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

            print(
                "Android background service started."
            )

        except Exception as error:

            print(
                "Could not start Android service:",
                error
            )

    def stop(self):

        try:

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            print(
                "Android background service stopped."
            )

        except Exception as error:

            print(
                "Could not stop Android service:",
                error
            )


android_service = AndroidService()