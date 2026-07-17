# Тесты

Установка зависимостей:

```
pip install -r requirements-dev.txt
```

Запуск всех тестов:

```
python3 -m unittest discover -s tests/unit/ -p '*test.py'
```

Запуск одного файла с тестами:

```
python3 -m unittest tests/unit/model/graph_test.py
```

Отчёт о покрытии, результат в __htmlcov/index.html__:

```
coverage run -m unittest discover -s tests/unit/ -p '*test.py'; coverage html
```

Тест __tests/unit/app/graph_plan_test.py__ строит диаграмму и требует установленного
[graphviz](https://graphviz.org/download/). Без него тест пропускается.
