find ./srclib/ -name '*.py' | xargs xgettext -d base --join-existing -o locales/en/LC_MESSAGES/messages.po
find ./srclib/ -name '*.py' | xargs xgettext -d base --join-existing -o locales/ru/LC_MESSAGES/messages.po
msgfmt -o locales/en/LC_MESSAGES/messages.mo locales/en/LC_MESSAGES/messages.po
msgfmt -o locales/ru/LC_MESSAGES/messages.mo locales/ru/LC_MESSAGES/messages.po
