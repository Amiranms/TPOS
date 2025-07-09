#!/bin/bash

# предположение: этого делать не нужно
# в противно случае - раскомментировать 3 строки снизу
#echo "Установка системных пакетов..."
#sudo apt-get update
#sudo apt-get install -y python3 python3-pip tmux

# Установка Python-зависимостей
echo "Установка Python-зависимостей..."
pip3 install libtmux click uuid
echo "Все зависимости установлены."