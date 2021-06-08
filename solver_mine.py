#!/usr/bin/env python3

import sys
import math
import copy

from common import print_tour, read_input, format_tour
INF = 100100
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)
'''

'''
def is_cross(city_a1, city_a2, city_b1, city_b2):
    a1_x = city_a1[0]
    a1_y = city_a1[1]
    a2_x = city_a2[0]
    a2_y = city_a2[1]
    b1_x = city_b1[0]
    b1_y = city_b1[1]
    b2_x = city_b2[0]
    b2_y = city_b2[1]
    # x座標によるチェック
    if(a1_x >= a2_x):
        if ((a1_x < b1_x and a1_x < b2_x) or  (a2_x > b1_x and a2_x > b2_x)):
            return False
        else:
            if ((a2_x < b1_x and a2_x < b2_x) or  (a1_x > b1_x and a1_x > b2_x)):
                return False
    # y座標によるチェック
    if (a1_y >= a2_y):
        if ((a1_y < b1_y and a1_y < b2_y) or (a2_y > b1_y and a2_y > b2_y)):
            return False
    else:
        if ((a2_y < b1_y and a2_y < b2_y) or  (a1_y > b1_y and a1_y > b2_y)):
            return False
    if (((a1_x - a2_x) * (b1_y - a1_y) + (a1_y - a2_y) * (a1_x - b1_x)) * 
        ((a1_x - a2_x) * (b2_y - a1_y) + (a1_y - a2_y) * (a1_x - b2_x)) > 0):
        return False
    if (((b1_x - b2_x) * (a1_y - b1_y) + (b1_y - b2_y) * (b1_x - a1_x)) * 
        ((b1_x - b2_x) * (a2_y - b1_y) + (b1_y - b2_y) * (b1_x - a2_x)) > 0):
        return False
    return True

# city_a1_itrator が最も小さい city_b2_itrator が最も大きい
def uncross_pathes(tour,city_a1_itrator, city_a2_itrator, city_b1_itrator, city_b2_itrator):
    new_tour = tour[:city_a1_itrator]
    new_tour += tour[city_a2_itrator:city_b1_itrator].reverse()
    new_tour += tour[city_b2_itrator:]
    return new_tour

def greedy(dist,city_list):
    current_city = city_list.pop(0)
    unvisited_cities = city_list#set(range(1, number_of_cities))
    tour = [current_city]
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

def solve(cities):
    number_of_cities = len(cities)
    x_grid = 8
    y_grid = 6
    grid = [ [[] for j in range(y_grid)] for i in range(x_grid)]
    for i in range(number_of_cities):
        city_x_grid = math.floor(cities[i][0]/(1600.0/x_grid))
        city_y_grid = math.floor(cities[i][1]/(900.0/y_grid))
        grid[city_x_grid][city_y_grid].append(i)

    print(grid)
    dist = [[0] * number_of_cities for i in range(number_of_cities)]
    for i in range(number_of_cities):
        for j in range(i, number_of_cities):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    tour_grid = [ [[] for j in range(y_grid)] for i in range(x_grid)]
    copied_grid = copy.deepcopy(grid)
    for x in range(x_grid):
        for y in range(y_grid):
            
            if len(grid[x][y]) > 0:
                tour_mini = greedy(dist,copied_grid[x][y])
                tour_grid[x][y] = tour_mini
                print("x{0} y{1} grid{2} tour_grid{3}\n".format(x,y,grid[x][y],tour_grid[x][y]))
   
    tour = []
    grid_order_x = list(range(0,8,1))
    for i in range(7,-1,-1):
        grid_order_x += [i]*5
    grid_order_y = [0]*8 
    for i in range(4):
        grid_order_y += list(range(1,6,1))+list(range(5,0,-1))
    for i in range(len(grid_order_x)):
        x = grid_order_x[i]
        y = grid_order_y[i]
        tour += tour_grid[x][y]
    print(tour)
    
    '''
    if (is_cross(city_a1, city_a2, city_b1, city_b2)):
        uncross_pathes(tour,city_a1, city_a2, city_b1, city_b2)
    '''

    return tour
  
if __name__ == '__main__':
    # assert len(sys.argv) > 1
    CHALLENGES = 7
    cities = read_input(f'input_{2}.csv')
    tour = solve(cities)
    
    for i in range(CHALLENGES):
        #print(i)
        cities = read_input(f'input_{i}.csv')
        tour = solve(cities)
        #print_tour(tour)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')
            
        