#!/usr/bin/env python3

import sys
import math
import copy

from common import print_tour, read_input, format_tour
INF = 100100
def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def get_distance(cities):
    number_of_cities = len(cities)
    distance_matrix = [[0] * number_of_cities for i in range(number_of_cities)]
    for i in range(number_of_cities):
        for j in range(i, number_of_cities):
            distance_matrix[i][j] = distance_matrix[j][i] = distance(cities[i], cities[j])
    return distance_matrix

def is_cross(city_a1, city_a2, city_b1, city_b2):
    if distance(city_a1,city_a2) + distance(city_b1,city_b2) > distance(city_a1,city_b1) + distance(city_b2,city_a2):
        return True
    else:
        return False

# city_a1_itrator が最も小さい city_b2_itrator が最も大きい
def uncross_pathes(tour,city_iterator1, city_iterator2 ):
        tmp = tour[city_iterator1 + 1 : city_iterator2 + 1 ]
        tour[city_iterator1 + 1 : city_iterator2 + 1 ] = tmp[::-1]
        return tour

def improve_tour(cities,tour,dist):
    number_of_cities = len(cities)
    while True:
        improved = False
        for i in range(0,number_of_cities-2):
            for j in range(i+2,number_of_cities):
                if i == 0 and j == number_of_cities - 1:
                    continue
                if is_cross(cities[tour[i]],cities[tour[i+1]],cities[tour[j]],cities[tour[(j+1)%number_of_cities]]):
                    tour = uncross_pathes(tour,i,j)
                    improved = True
        if not improved:
            break
    return tour


def greedy(distance_matrix,city_list):
    current_city = city_list.pop(0)
    unvisited_cities = city_list#set(range(1, number_of_cities))
    tour = [current_city]
    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: distance_matrix[current_city][city])
        
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour
def solve_neo(cities):
    distance_matrix = get_distance(cities)
    city_list = list(range(0, len(cities)))
    tour = greedy(distance_matrix,city_list)
    tour = improve_tour(cities,tour,distance_matrix)
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

    distance_matrix = [[0] * number_of_cities for i in range(number_of_cities)]
    for i in range(number_of_cities):
        for j in range(i, number_of_cities):
            distance_matrix[i][j] = distance_matrix[j][i] = distance(cities[i], cities[j])

    tour_grid = [ [[] for j in range(y_grid)] for i in range(x_grid)]
    copied_grid = copy.deepcopy(grid)
    for x in range(x_grid):
        for y in range(y_grid):
            
            if len(grid[x][y]) > 0:
                tour_mini = greedy(distance_matrix,copied_grid[x][y])
                tour_grid[x][y] = tour_mini
   
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
    return tour
  
if __name__ == '__main__':
    # assert len(sys.argv) > 1
    CHALLENGES = 7
    
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        tour = solve_neo(cities)
        #print_tour(tour)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')
            
        