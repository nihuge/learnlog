from learnlogs.models import I18n


class Module():
    def __init__(self):
        self.I18n = I18n

    def trans(self, text, luagange):
        transed = self.I18n.objects.get(language=luagange,
                                        untranslated_text=text)
        return transed.translated_text
