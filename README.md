Консольное приложение для выгрузки брендов и картинок по API.

Установка и использование

1. Скачать приложение в необходимую директорию .
2. Запустить из командной строки основной файл main.py.
3. Параметром необходимо передать название директории.

Результат запуска

В директории где находится файл main.py будет создана папка
с именем, переданного в качестве аргумента программе.
В новой директории будут созданы два файла:
brands.xlsx и products.xlsx - с основной информацией о товарах полученной через API.
Так же в ней будет создана отдельная директория 'images' содержащая упорядоченные по id продукта именами картинок.
Конечный вывод будет представлен мини отчетом.

Пример использования

Python 3.7.3 on linux

user@user:~$ python3 main.py
>>> main.py: error: the following arguments are required: name_of_directory

user@user:~$ python3 main.py dir_name
>>> ... information about creating files in dir_name ...

