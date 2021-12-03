# subtitle_ocr_translate
Aplikacja GUI napisana w Pythonie pozwalająca na łatwe tłumaczenie napisów po niemiecku serialów dosępnych w internecie oraz zapisywanie nowych słówek i tłumaczeń.
Aplikacja tworzy zrzut ekranu o wymiarach i pozycji, które należy ustalić przy pomocy screenshot_adjust.pyw i ręcznie wpisać w tranlate_git.pyw.
Następnie aplikacja rozpoznaje słowa na danym zrzucie ekranu i pozwala użytkownikowi na wybór słowa do tłumaczenia.
Wybrane słowo jest tłumaczone przy użyciu API słownika internetowego PONS.
Użytkowik może wybrać tłumaczenie które ma być zapamiętane do pliku txt, którego format umożliwia szybki import do quizlet.com.

Aplikacja do działania wymaga założenia konta na https://en.pons.com/p/online-dictionary/developers/api utworzenia konta i umieszczenia uzyskanego klucza API o nazwie "secret"
w pliku config.txt:
<code> api_key= secret </code>
