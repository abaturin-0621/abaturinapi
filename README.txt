Тестирование реализовано с помощью pytest
Для запуска тестов нужно запустить приложение (app.py)

Не покрыты эндпоинты /send, /get , /items

Сервер по умолчанию http://127.0.0.1:5000/api
Swagger http://127.0.0.1:5000/swagger


$FULLPATH -располжение проекта
$TESTPATREPORT   - путь к отчету о тестировании

запуск тестов
pytest -rxXspP {$FULLPATH}\gitapi\tests --html={$TESTPATREPORT}\reports\report_final.html --self-contained-html
