"""
Консольная утилита lsof (List Open Files) выводит информацию о том, какие файлы используют какие-либо процессы.
Эта команда может рассказать много интересного, так как в Unix-подобных системах всё является файлом.

Но нам пока нужна лишь одна из её возможностей.
Запуск lsof -i :port выдаст список процессов, занимающих введённый порт.
Например, lsof -i :5000.

Как мы с вами выяснили, наш сервер отказывается запускаться, если кто-то занял его порт. Напишите функцию,
которая на вход принимает порт и запускает по нему сервер. Если порт будет занят,
она должна найти процесс по этому порту, завершить его и попытаться запустить сервер ещё раз.
"""


import os
import signal
import shlex
import subprocess

from typing import List
from flask import Flask


app = Flask(__name__)


def get_pids(port: int) -> List[int]:
    """
    Возвращает список PID процессов, занимающих переданный порт
    @param port: порт
    @return: список PID процессов, занимающих порт
    """
    if not isinstance(port, int):
        raise ValueError

    pids: List[int] = []

    # команда процесса:
    command = f'lsof -i :{port}'

    # токенизация команды:
    token_command = shlex.split(command)
    # print(token_command)

    # выполнение команды:
    process = subprocess.run(
        token_command,
        stdout=subprocess.PIPE,
        text=True
    )

    # чтение вывода команды:
    output = process.stdout
    # print(output)

    # помещаем каждую строку в список:
    lines = output.splitlines()
    # print(lines)

    # срезаем строку 0 (заголовки) и каждую следующую строку разделяем на элементы:
    for line in lines[1:]:
        columns = line.split()
        # print(columns)

        # извлекаем PID и ложим в список:
        pid = int(columns[1])
        pids.append(pid)

    print(f'Port {port}: PID = {pids}')
    return pids


def free_port(port: int) -> None:
    """
    Завершает процессы, занимающие переданный порт
    @param port: порт
    """
    # получаем список PID нашего порта:
    pids: List[int] = get_pids(port)

    # убиваем процессы порта:
    for pid in pids:
        try:
            # subprocess.run(['kill', '-9', str(pid)])
            os.kill(pid, signal.SIGKILL)
            print(f'PID {pid} successfully killed!')
        except Exception as exc:
            print(f'ERROR kill PID {pid}: {exc}')


def run(port: int) -> None:
    """
    Запускает flask-приложение по переданному порту.
    Если порт занят каким-либо процессом, завершает его.
    @param port: порт
    """
    free_port(port)
    app.run(port=port)


if __name__ == '__main__':
    run(5000)