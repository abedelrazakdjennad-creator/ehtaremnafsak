try:
    from jnius import autoclass, PythonJavaClass, java_method
except ImportError:
    autoclass = None
    PythonJavaClass = object

    def java_method(*args, **kwargs):
        def decorator(function):
            return function
        return decorator


class TTSListener(PythonJavaClass):

    __javainterfaces__ = [
        "android/speech/tts/TextToSpeech$OnInitListener"
    ]

    def __init__(self, owner):
        super().__init__()
        self.owner = owner

    @java_method("(I)V")
    def onInit(self, status):

        try:

            TextToSpeech = autoclass(
                "android.speech.tts.TextToSpeech"
            )

            if status == TextToSpeech.SUCCESS:

                self.owner.ready = True

                # العربية
                Locale = autoclass(
                    "java.util.Locale"
                )

                arabic = Locale(
                    "ar",
                    "DZ"
                )

                result = self.owner.tts.setLanguage(
                    arabic
                )

                print(
                    "TTS ready:",
                    result
                )

        except Exception as error:

            print(
                "TTS initialization error:",
                error
            )


class VoiceResponse:

    def __init__(self):

        self.tts = None
        self.ready = False

        if autoclass is None:
            return

        try:

            TextToSpeech = autoclass(
                "android.speech.tts.TextToSpeech"
            )

            PythonActivity = autoclass(
                "org.kivy.android.PythonActivity"
            )

            activity = PythonActivity.mActivity

            self.listener = TTSListener(
                self
            )

            self.tts = TextToSpeech(
                activity,
                self.listener
            )

        except Exception as error:

            print(
                "TTS error:",
                error
            )

    def speak(self, text):

        if not text:
            return

        if not self.tts:
            return

        try:

            TextToSpeech = autoclass(
                "android.speech.tts.TextToSpeech"
            )

            # إلغاء الكلام السابق
            self.tts.stop()

            # جعل الرد يبدو مباشرًا وقويًا
            self.tts.setSpeechRate(
                1.05
            )

            self.tts.setPitch(
                0.85
            )

            self.tts.speak(
                str(text),
                TextToSpeech.QUEUE_FLUSH,
                None,
                "respect_warning"
            )

        except Exception as error:

            print(
                "Speak error:",
                error
            )

    def stop(self):

        try:

            if self.tts:

                self.tts.stop()
                self.tts.shutdown()

        except Exception:
            pass