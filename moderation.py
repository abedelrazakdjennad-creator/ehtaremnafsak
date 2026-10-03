# moderation.py

import re


# كلمات وعبارات مسيئة شائعة.
# هذه القائمة مجرد بداية ويمكن توسيعها لاحقًا.
BAD_WORDS = {
    "حمار",
    "حمّار",
    "فرخ",
    "رخيس",
    "رخيص",
}


def normalize_text(text):
    if not text:
        return ""

    text = text.lower().strip()

    # توحيد بعض أشكال الحروف العربية
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ى": "ي",
        "ة": "ه",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # إزالة علامات الترقيم
    text = re.sub(r"[^\w\s\u0600-\u06FF]", " ", text)

    # إزالة المسافات الزائدة
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def contains_bad_language(text):
    """
    يرجع True إذا وجد كلمة مسيئة معروفة.
    """

    text = normalize_text(text)

    if not text:
        return False

    words = set(text.split())

    for bad_word in BAD_WORDS:
        normalized_bad = normalize_text(bad_word)

        if normalized_bad in words:
            return True

    return False


def should_respond(text):
    """
    الدالة التي يستعملها التطبيق لتحديد
    هل يجب أن يرد أم لا.
    """

    return contains_bad_language(text)


def get_response():
    return "احترم نفسك تحترم يا أخي"