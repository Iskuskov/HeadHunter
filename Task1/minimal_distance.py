# -*- coding: utf-8

__author__ = 'iskuskov'
__email__ = 'iskuskov@gmail.com'

import sys
import math
from operator import itemgetter


def distance(a, b):
    """Возвращает евклидово расстояние."""
    return math.sqrt( ((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2) )


def min_distance_bruteforce(points):
    """Возвращает минимальное расстояние путем полного перебора."""
    
    len_points = len(points)
    # Не имеет смысла при числе точек меньше 2
    # assert len_points >= 2
    if (len_points < 2): return float('inf')
    
    return min(distance(points[i], points[j]) 
        for i in range(len_points - 1) 
        for j in range(i + 1, len_points))


def split_points(points_x, points_y):
    """Разделяет массивы точек.
    
    points_x -- массив точек, отсортированных по координате x
    points_y -- массив точек, отсортированных по координате y
    """
    
    # Разделяем точки на 2 примерно равных множества (в зависимости от четности количества)
    mid = len(points_x) // 2
    
    # Разбиваем массив точек points_x; полученные массивы остаются отсортированными
    points_x_l, points_x_r = points_x[:mid], points_x[mid:]
    
    # Координаты x вертикальной прямой, разделяющей точки
    median = points_x_l[-1][0]
    
    # Разбиваем массив точек points_y; полученные массивы остаются отсортированными
    points_y_l, points_y_r = [], []
    for point_y in points_y:
        if point_y[0] <= median:
            points_y_l.append(point_y)
        else:
            points_y_r.append(point_y)
        
    return median, points_x_l, points_x_r, points_y_l, points_y_r


def min_distance_recursive(points_x, points_y):
    """Возвращает минимальное расстояние рекурсивно.
    
    points_x -- массив точек, отсортированных по координате x
    points_y -- массив точек, отсортированных по координате y
    """
    
    # 1. Если точек не более 3, используем полный перебор
    if len(points_x) <= 3:
        return min_distance_bruteforce(points_x)
    
    # 2. Если точек не более 3, используем рекурсию
    else:
        # 2.1. Разделяем точки вертикальной прямой
        median, points_x_l, points_x_r, points_y_l, points_y_r = split_points(points_x, points_y)

        # 2.2. Рекурсивный поиск минимального расстояния в правой и левой частях относительно прямой
        min_dist_l = min_distance_recursive(points_x_l, points_y_l)
        min_dist_r = min_distance_recursive(points_x_r, points_y_r)
        min_dist = min(min_dist_l, min_dist_r)

        # 2.3. Проверяем, не принадлежат ближайшие точки разным частям относительно прямой
        
        # 2.3.1. Убираем точки, не лежащие в пределах допустимой полосы ±min_dist относительно прямой
        points_y_strip = [point_y for point_y in points_y if abs(point_y[0] - median) < min_dist]
        
        # 2.3.2. В полученном массиве отыскиваем пары точек, лежащих ближе, чем найденные в рекусивных вызовах
        # Примечание: достаточно рассмотреть лишь 7 точек, расположенных в полученном массиве после текущей
        len_points_y_strip = len(points_y_strip)
        max_comp = 7
        for i in range(len_points_y_strip - 1):
            for j in range(i + 1, min(i + 1 + max_comp, len_points_y_strip)):
                curr_dist = distance(points_y[i], points_y[j])
                # 2.3.3. Если условие выполняется, нашли точки, лежащих ближе, чем найденные в рекусивных вызовах
                if curr_dist < min_dist:
                    min_dist = curr_dist

        return min_dist
    
    
def min_distance(points):

    # Формируем массивы точек, отсортированных по координате X и Y соотвественно
    # Предварительная сортировка необходима для улучшения производительности алгоритма
    points_x = sorted(points,   key=itemgetter(0))
    points_y = sorted(points_x, key=itemgetter(1))

    # Запускаем рекурсивную функцию для получения минимального расстояния
    return min_distance_recursive(points_x, points_y)


def main():
    # Считываем данные
    content = []
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        try:
            with open(filename) as f:
                content = f.readlines()
        except IOError as e:
            print ("I/O error({0}): {1}".format(e.errno, e.strerror))
            sys.exit(1)
    else:
        while True:
            line = raw_input('')
            if not line: break
            content.append(line)
          
    # Формируем массив точек
    try:
        points = []
        for line in content:
            digits = [int(n) for n in line.split()]
            points.append((digits[0], digits[1]))
    except ValueError:
        print ('Invalid Value')
        sys.exit(1)
     
    # Результат
    min_dist = min_distance(points)
    print min_dist

if __name__ == '__main__':
    main()