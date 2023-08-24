'''
Patrick Rademacher
Anthony Rhodes
Artificial Intelligence
Portland State University
February 21, 2020

8 Queen Puzzle Solver Using Genetic Algorithms

'''


import math
import random
import numpy as np
import matplotlib.pyplot as plt

size_of_population = 1200



clash_dict = {
    0: 0,
    1: 0,
    2: 1,
    3: 3,
    4: 6,
    5: 10,
    6: 15,
    7: 21,
    8: 28
}

class board_specimen(object):
    def __init__(self, layout, rand_ints):
        self.layout = layout
        self.rand_ints = rand_ints
        self.total_row_clashes = 0
        self.diagz_clashes = 0
        self.diagz_clashes_2 = 0
        self.reverse_diagz_clashes = 0
        self.reverse_diagz_clashes_2 = 0
        self.clash_sum = 0
        self.health = 0
        self.probability = 0
        self.was_a_mutation = False
        self.came_from_a_mutation = False

    
    def fill_board_randomly(self):
        for k in range(8):
            self.layout[self.rand_ints[k]][k] = "♛"
        return self.layout    

    def count_row_clashes(self):
        for w in range(8):
            queen_count = 0
            for x in range(8):
                if self.layout[w][x] == "♛":
                    queen_count += 1  
            self.total_row_clashes += clash_dict[queen_count]
        return self.total_row_clashes
    
    def count_diagz_clashes(self):
        for g in range(8):
            queen_count = 0
            point_x = g
            point_y = 0
            coordinate = self.layout[point_x][point_y]
            if coordinate == "♛":
                    queen_count += 1
            while True:
                point_x -= 1
                point_y += 1
                if point_y == g + 1:
                    break
                coordinate = self.layout[point_x][point_y]
                if coordinate == "♛":
                    queen_count += 1

            self.diagz_clashes += clash_dict[queen_count]
        for g in range(1, 8):
            queen_count = 0
            point_x = g
            point_y = 7
            coordinate = self.layout[point_x][point_y]
            if coordinate == "♛":
                queen_count += 1
            while True:
                point_x += 1
                if point_x == 8:
                    break
                point_y -= 1
                coordinate = self.layout[point_x][point_y]
                if coordinate == "♛":
                    queen_count += 1
            self.diagz_clashes_2 += clash_dict[queen_count]
        for g in range(8):
            queen_count = 0
            point_x = g
            point_y = 7
            coordinate = self.layout[point_x][point_y]
            if coordinate == "♛":
                    queen_count += 1
            while True:
                point_x -= 1
                if point_x == -1:
                    break
                point_y -= 1
                coordinate = self.layout[point_x][point_y]
                if coordinate == "♛":
                    queen_count += 1  
            self.reverse_diagz_clashes += clash_dict[queen_count]
        for g in range(1, 8):
            queen_count = 0
            point_x = g
            point_y = 0
            coordinate = self.layout[point_x][point_y]
            if coordinate == "♛":
                    queen_count += 1
            while True:
                point_x += 1
                if point_x == 8:
                    break
                point_y += 1
                coordinate = self.layout[point_x][point_y]
                if coordinate == "♛":
                    queen_count += 1  
            self.reverse_diagz_clashes_2 += clash_dict[queen_count]
        self.clash_sum = self.diagz_clashes + self. diagz_clashes_2 + self.reverse_diagz_clashes + self.reverse_diagz_clashes_2
        return self.clash_sum
    
    def get_yo_health_report(self):
        self.clash_sum += self.total_row_clashes
        self.health = 28 - self.clash_sum
        if self.health == 28:
            print('HOLY FUCK!')
        return self.health           
    
    def update_probability(self, value):
        self.probability = value
        return self.probability  

    def update_layout(self, new_layout):
        for i in range(8):
            for j in range(8):
                self.layout[i][j] = new_layout[i][j]
        self.total_row_clashes = 0
        self.diagz_clashes = 0
        self.diagz_clashes_2 = 0
        self.reverse_diagz_clashes = 0
        self.reverse_diagz_clashes_2 = 0
        self.clash_sum = 0
        self.health = 0
        self.probability = 0
        self.was_a_mutation = False
        self.came_from_a_mutation = False
    
    def get_health(self):
        return self.health

    def update_mutation_bools(self, m):
        if m == 0 or m == 1:
            self.was_a_mutation = True
            return self.was_a_mutation
        else:
            self.came_from_a_mutation = True
            return self.came_from_a_mutation
        


    def print_layout(self):
        for a in range(8):
            for b in range(8):
                print(str(self.layout[a][b]) + ' ', end = '')
            print('\n')
        print(self.health)
        print(self.probability)
    
    

    
def update_prob(size_of_population, first_generation):
    sum_population_health = 0
    avg_health = 0
    for c in range(size_of_population):
        sum_population_health += first_generation[c].health
    for c in range(size_of_population):
        prob = first_generation[c].health/sum_population_health
        first_generation[c].update_probability(prob)
    avg_health = sum_population_health/size_of_population
    print("avg health = " + str(avg_health))
    return first_generation, avg_health 
      
def let_us_breed(size_of_population, first_generation):
    bins = []
    mutant = -1
    starting_point = 0
    mutation = random.randint(0, 20)
    for b in range(size_of_population):
        bins.append([starting_point, starting_point + first_generation[b].probability])
        starting_point = starting_point + first_generation[b].probability
    child_one = [[0 for i in range(8)] for j in range (8)]
    child_two = [[0 for i in range(8)] for j in range (8)]
    lottery = 1000
    lottery_2 = 1000
    no_repeat = -1
    while(lottery >= 1):
        lottery = random.randint(0, 100000)
        lottery = lottery * .00001
    
    p1 = board_specimen(blank_board, [])
    p2 = board_specimen(blank_board, [])
    for b in range(len(bins)):
        if lottery >= bins[b][0] and lottery < bins[b][1]:
            p1 = first_generation[b]
            no_repeat = b
            break
    while(lottery_2 >= 1):
            lottery_2 = random.randint(0, 100000)
            lottery_2 = lottery_2 * .00001
            while lottery_2 >= bins[no_repeat][0] and lottery_2 < bins[no_repeat][1]:
                lottery_2 = random.randint(0, 100000)
                lottery_2 = lottery_2 * .00001
    for b in range(len(bins)):
        if lottery_2 >= bins[b][0] and lottery_2 < bins[b][1]:
            p2 = first_generation[b]
            break
    if p1.was_a_mutation == True or p2.was_a_mutation == True or p1.came_from_a_mutation == True or p2.came_from_a_mutation == True:
        mutant = 2
    for w in range(8):
        for x in range(8):
            if w < 4:
                child_one[x][w] = p1.layout[x][w]
                child_two[x][w] = p2.layout[x][w]
            else:
                child_two[x][w] = p1.layout[x][w]
                child_one[x][w] = p2.layout[x][w]
    if mutation == 5:
        col1 = random.randint(0, 7)
        col2 = random.randint(0,7)
        temp = []
        temp2 = []
        mutant = 0
        for i in range(8):
            temp.append(child_one[i][col1])
            temp2.append(child_one[i][col2])

        for i in range(8):
            child_one[i][col2] = temp[i]
            child_one[i][col1] = temp2[i]
    if mutation == 2:
        col1 = random.randint(0, 7)
        col2 = random.randint(0,7)
        temp = []
        temp2 = []
        mutant = 1
        for i in range(8):
            temp.append(child_two[i][col1])
            temp2.append(child_two[i][col2])

        for i in range(8):
            child_two[i][col2] = temp[i]
            child_two[i][col1] = temp2[i]
    return first_generation, child_one, child_two, mutant
   
def replace_weakest_w_children(size_of_population, first_generation, child1, child2, mutant):
    indy = -1
    indy2 = -1
    for r in range(2):
        minimum_health = 29
        for q in range(size_of_population):
            if first_generation[q].get_health() < minimum_health and q != indy:
                minimum_health = first_generation[q].get_health()
                if r == 0:
                    indy = q
                else:
                    indy2 = q
        if r == 0:
            first_generation[indy].update_layout(child1)
            first_generation[indy].count_row_clashes()
            first_generation[indy].count_diagz_clashes()
            first_generation[indy].get_yo_health_report()
            if mutant == 0:
                first_generation[indy].update_mutation_bools(mutant)
            elif mutant == 2:
                first_generation[indy].update_mutation_bools(mutant)




        else:
            first_generation[indy2].update_layout(child2)
            first_generation[indy2].count_row_clashes()
            first_generation[indy2].count_diagz_clashes()
            first_generation[indy2].get_yo_health_report()
            if mutant == 1:
                first_generation[indy].update_mutation_bools(mutant) 
            elif mutant == 2:
                first_generation[indy].update_mutation_bools(mutant) 

    
    return first_generation, first_generation[indy], first_generation[indy2]


rand_int_array = []
random_ints = []
for y in range(size_of_population):
    random_ints = []
    for z in range(8):
        random_ints.append(random.randint(0,7))
    rand_int_array.append(random_ints)


first_generation = [["" for q in range(8)] for s in range(8)] * size_of_population
sum_population_health = 0
for u in range(size_of_population):
    blank_board = [["[ ]" for i in range(8)]for k in range(8)]
    first_generation[u] = board_specimen(blank_board,rand_int_array[u])
    first_generation[u].fill_board_randomly()
    first_generation[u].count_row_clashes()
    first_generation[u].count_diagz_clashes()
    first_generation[u].get_yo_health_report()
    sum_population_health += first_generation[u].health

    print("\n\n")


total_counts = []
alll_avg = []
counterr = 0
while True:
    found_prodigy = False
    ind = 0
    avg = 0
    ewww_mutant = False
    first_generation, avg = update_prob(size_of_population, first_generation)
    alll_avg.append(avg)
    total_counts.append(counterr)
    first_generation, c1, c2, ewww_mutant = let_us_breed(size_of_population, first_generation)
    for q in range(size_of_population):
        if first_generation[q].get_health() == 28:
            found_prodigy = True
            break
    first_generation, new_kid, new_kid_2 = replace_weakest_w_children(size_of_population, first_generation, c1, c2, ewww_mutant)
    kiddo = -1
    if new_kid.get_health() == 28 or new_kid_2.get_health() == 28:
        found_prodigy = True
        ind = q
        if new_kid.get_health() == 28:
            kiddo = 0
        elif new_kid_2.get_health() == 28:
            kiddo = 1
    counter = 0
    if found_prodigy == True:
        print('# of iterations = ' + str(counterr))
        print('average health: ') 
        for healths in alll_avg: 
            if counter == 0 or counter % 100 == 0:
                print(str(healths))
            counter += 1
        if kiddo == 0:
            print('was a mutation = ' + str(new_kid.was_a_mutation))
            print('came from a mutation = ' + str(new_kid.came_from_a_mutation))
        elif kiddo == 1:
            print('was a mutation = ' + str(new_kid_2.was_a_mutation))
            print('came from a mutation = ' + str(new_kid_2.came_from_a_mutation))
        plt.plot(total_counts, alll_avg)
        plt.xlabel('generation #')
        plt.ylabel('average health score')
        plt.show()

        break
    counterr += 1
    





'''
while True:
    proceed = False
    for h in range(size_of_population):
        lottery = random.randint(0, 100)
        lottery = lottery * .01
        if lottery > bins[h][0] and lottery < bins[h][1] and h != first_winner:
            print("lucky winner 2!!!!!!!!")
            for w in range(8):
                for x in range(8):
                    lucky_winner_2[w][x] = first_generation[h].layout[w][x]
            first_generation[h].print_layout()
            parent_two = first_generation[h]
            proceed = True
            break
    if proceed == True:
        break

child_one = [[0 for i in range(8)] for j in range (8)]
child_two = [[0 for i in range(8)] for j in range (8)]
counter = 0
for f in range(8):
    for g in range(8):
        if f < 4:
            child_one[g][f] = lucky_winner[g][f]
            child_two[g][f] = lucky_winner_2[g][f]
        else:
            child_one[g][f] = lucky_winner_2[g][f]
            child_two[g][f] = lucky_winner[g][f]


indy = -1
indy2 = -1
for r in range(2):
    minimum_health = 29
    for q in range(size_of_population):
        if first_generation[q].get_health() < minimum_health and q != indy:
            minimum_health = first_generation[q].get_health()
            if r == 0:
                indy = q
            else:
                indy2 = q
    if r == 0:
        first_generation[indy].update_layout(child_one)
        first_generation[indy].count_row_clashes()
        first_generation[indy].count_diagz_clashes()
        print('healllllthhhhh')
        print(first_generation[indy].get_yo_health_report())
        first_generation[indy].get_yo_health_report()
        print(first_generation[indy].get_yo_health_report())


    else:
        first_generation[indy2].update_layout(child_two)
        first_generation[indy2].count_row_clashes()
        first_generation[indy2].count_diagz_clashes()
        first_generation[indy2].get_yo_health_report()

    
    
   

print("first child")

for x in range(8):
    for y in range(8):
        print(child_one[x][y], end = ' ')
    print('\n')

print("second child")
for x in range(8):
    for y in range(8):
        print(child_two[x][y], end = ' ')
    print('\n')

print('\n\n\n')



print('\n\n\n')

first_generation[indy].print_layout()
first_generation[indy2].print_layout()
print(indy)
print(indy2)

for gens in range(size_of_population):
    if first_generation[gens].layout == child_one:
        print(gens)
'''