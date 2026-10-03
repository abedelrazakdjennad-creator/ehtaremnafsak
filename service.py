# service.py

import time
import threading


class BackgroundVoiceService:

    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            # مكان تشغيل نظام الاستماع في الخلفية
            # سيتم ربطه بـ Android Foreground Service
            # في الخطوة التالية.

            time.sleep(1)


_service = None


def start_service():
    global _service

    if _service is None:
        _service = BackgroundVoiceService()

    _service.start()


def stop_service():
    global _service

    if _service is not None:
        _service.stop()