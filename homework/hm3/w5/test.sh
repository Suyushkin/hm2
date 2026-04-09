#!/bin/bash

# Скрипт для проверки кода и тестов дешифратора

echo "=== Запуск статического анализатора pylint ==="
# Сохраняем результат в JSON-файл
pylint decrypt.py --output-format=json > pylint_report.json
pylint_exit=$?
# Выводим отчёт в консоль
pylint decrypt.py

echo -e "\n=== Запуск юнит-тестов ==="
python -m unittest test_decrypt.py
tests_exit=$?

echo -e "\n=== Результат ==="
if [ $pylint_exit -eq 0 ] && [ $tests_exit -eq 0 ]; then
    echo "OK"
else
    echo "Имеются ошибки"
    exit 1
fi