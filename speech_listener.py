import threading
import time

try:
    from jnius import autoclass, PythonJavaClass, java_method
except ImportError:
    autoclass = None

    class PythonJavaClass:
        pass

    def java_method(*args, **kwargs):
        def decorator(function):
            return function
        return decorator


class RecognitionListener(PythonJavaClass):

    __javainterfaces__ = [
        "android/speech/RecognitionListener"
    ]

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    @java_method("(Landroid/os/Bundle;)V")
    def onReadyForSpeech(self, params):
        pass

    @java_method("()V")
    def onBeginningOfSpeech(self):
        pass

    @java_method("([F)V")
    def onRmsChanged(self, rms):
        pass

    @java_method("([B)V")
    def onBufferReceived(self, buffer):
        pass

    @java_method("()V")
    def onEndOfSpeech(self):
        pass

    @java_method("(I)V")
    def onError(self, error):
        if self.owner.running:
            self.owner.restart()

    @java_method("(Landroid/os/Bundle;)V")
    def onResults(self, results):

        if not self.owner.running:
            return

        try:

            matches = results.getStringArrayList(
                "results_recognition"
            )

            if matches:

                count = matches.size()

                if count > 0:

                    text = str(
                        matches.get(0)
                    ).strip()

                    if text:

                        callback = self.owner.callback

                        if callback:
                            callback(text)

        except Exception:
            pass

        if self.owner.running:
            self.owner.restart()

    @java_method("(Landroid/os/Bundle;)V")
    def onPartialResults(self, results):
        pass

    @java_method("(ILandroid/os/Bundle;)V")
    def onEvent(self, event_type, params):
        pass


class SpeechListener:

    def __init__(self, callback=None):

        self.callback = callback

        self.running = False

        self.recognizer = None

        self.listener = None

        self.activity = None

        self.SpeechRecognizer = None

        self.Intent = None

        self.restart_lock = threading.Lock()

    def start(self):

        if self.running:
            return

        self.running = True

        threading.Thread(
            target=self._initialize,
            daemon=True
        ).start()

    def _initialize(self):

        if autoclass is None:
            return

        try:

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            self.SpeechRecognizer = autoclass(
                "android.speech.SpeechRecognizer"
            )

            self.Intent = autoclass(
                "android.content.Intent"
            )

            self.activity = (
                PythonActivity.mActivity
            )

            if not self.SpeechRecognizer.isRecognitionAvailable(
                self.activity
            ):
                return

            self._create_recognizer()

            self._listen()

        except Exception:
            pass

    def _create_recognizer(self):

        try:

            if self.recognizer:
                self.recognizer.destroy()

        except Exception:
            pass

        self.recognizer = (
            self.SpeechRecognizer
            .createSpeechRecognizer(
                self.activity
            )
        )

        self.listener = RecognitionListener(
            self
        )

        self.recognizer.setRecognitionListener(
            self.listener
        )

    def _listen(self):

        if not self.running:
            return

        try:

            intent = self.Intent(
                "android.speech.action.RECOGNIZE_SPEECH"
            )

            intent.putExtra(
                "android.speech.extra.LANGUAGE",
                "ar-DZ"
            )

            intent.putExtra(
                "android.speech.extra.LANGUAGE_PREFERENCE",
                "ar-DZ"
            )

            intent.putExtra(
                "android.speech.extra.PARTIAL_RESULTS",
                True
            )

            intent.putExtra(
                "android.speech.extra.MAX_RESULTS",
                5
            )

            intent.putExtra(
                "android.speech.extra.SPEECH_INPUT_COMPLETE_SILENCE_LENGTH_MILLIS",
                1200
            )

            intent.putExtra(
                "android.speech.extra.SPEECH_INPUT_POSSIBLY_COMPLETE_SILENCE_LENGTH_MILLIS",
                800
            )

            self.recognizer.startListening(
                intent
            )

        except Exception:

            if self.running:
                self.restart()

    def restart(self):

        if not self.running:
            return

        if not self.restart_lock.acquire(
            blocking=False
        ):
            return

        def worker():

            try:

                time.sleep(0.4)

                if not self.running:
                    return

                try:

                    if self.recognizer:
                        self.recognizer.cancel()

                except Exception:
                    pass

                self._create_recognizer()

                time.sleep(0.1)

                self._listen()

            except Exception:
                pass

            finally:

                self.restart_lock.release()

        threading.Thread(
            target=worker,
            daemon=True
        ).start()

    def stop(self):

        self.running = False

        try:

            if self.recognizer:

                self.recognizer.stopListening()

                self.recognizer.cancel()

                self.recognizer.destroy()

        except Exception:
            pass

        self.recognizer = None

        self.listener = None