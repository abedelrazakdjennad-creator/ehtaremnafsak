import time
import threading

from speech_listener import SpeechListener
from voice import VoiceResponse


class RespectService:

    def __init__(self):
        self.running = True
        self.voice = VoiceResponse()
        self.listener = SpeechListener(
            callback=self.on_speech
        )

    def start(self):
        self.listener.start()

        while self.running:
            time.sleep(1)

    def on_speech(self, text):

        if not self.running or not text:
            return

        text = str(text).strip().lower()

        if self.is_insult(text):
            self.voice.speak(
                "احترم نفسك تحترم يا أخي"
            )

    def is_insult(self, text):

        insults = [
            "حمار",
            "حمّار",
            "رخيص",
            "رخيس",
            "كلب",
            "كلبة",
            "غبي",
            "غبية",
            "بهيم",
            "بهيمة",
            "سفيه",
            "سفيهة"
        ]

        return any(
            word in text
            for word in insults
        )

    def stop(self):

        self.running = False

        try:
            self.listener.stop()
        except Exception:
            pass

        try:
            self.voice.stop()
        except Exception:
            pass


_service = None


def main():

    global _service

    _service = RespectService()

    try:
        _service.start()
    except Exception:
        _service.stop()


if __name__ == "__main__":
    main()