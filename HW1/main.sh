#!/bin/bash

if [ ! -f ./main.py ]; then
    echo "Ошибка: Python-скрипт main.py не найден."
    exit 1
fi

python3 main.py "$@"