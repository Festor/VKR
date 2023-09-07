# VKR
Задача: Реализовать и протестировать инструмент автоматизации поиска закладок на демонстрационном примере.

Разработанный модуль содержит:

* Демонстрационный пример - приложение, моделирующее как безопасное поведение, так и срабатывание программной закладки при особом условии.
* Для обеспечения совместимости графического приложения Windows с фаззером разработана оснастка, передающая параметры от фаззера к тестируемому приложению и ограничивающая время его работы.
* Разработан модуль фаззера, позволяющий генерировать случайные параметры и вызывать с ними тестируемое приложение через оснастку и модуль динамической инструментации, собирать и каталогизировать отчёты о покрытии блоков кода приложения.
* Разработан плагин для Cutter, автоматизирующий разметку блоков графа в дизассемблере цветом по показателям покрытия, собранного в ходе фаззинга.



## Usage
Для генерации файла покрытия по результату события фаззера применяется инструмент DynamoRIO - https://dynamorio.org/

<br>

## Схема средства автоматизации

<img src='https://github.com/Festor/VKR/tree/main/scheme.png'>

<br>

## Описание работы модулей

<img src='https://github.com/Festor/VKR/tree/main/screenshot.png'>

<br>

## Результат

<br>

## Карта покрытия в Cutter

<img src='https://github.com/Festor/VKR/tree/main/screenshot.png'>

<br>


