Опис проекту
1) Постановка і аналіз задачі
Першим пунктом в нашій роботі було обрати гру з-поміж можливих варіантів. Ми обрали популярну гру tetris. 
Нам треба зробити гру, в якій була б можливість обрати рівень проходження гри. Також в грі повинно бути хоча б 5 дій від користувача.
Суть гри tetris полягає в тому, що зверху ігрового екрана падають різні фігурки. Для того щоб не програвати, треба зробити так, щоб 
ні одна з фігур не досягла верхньої межі ігрового поля. При цьому якщо якась горизонтальна лінія ігрового поля повністю заповнена 
квадратиками с фігурок - ці квадратики зникають.


2)Розподіл ролей у команді:


Антон Маринич зробив:
  1. Саму механіку гри (фігурки, рух фігурок, поворот фігурок, прискорення фігурок, система рахування очок, рахування рекорду)
  2. Знайшов картинки для фону.
  3. Текст мануалу до гри.
  4. Опис і звіт до гри.
  
Антон Гоголь зробив:
  1. Механіку вибора рівня та  різні рівні.
  2. Обробку кінця гри з вибором для користувача.
  3. Кнопку для можливості продивитись мануал по грі.
  4. Рендер контенту на екрані
  
3) Опис технічних засобів розробки:

Для реалізації гри ми використали мову програмування pyhon і біліотеку pygame.
Ця бібліотека допомагає зручно і лаконічно реалізовувати ігрові механіки.

