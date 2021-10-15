import random

import gym
import gym_snake
import numpy as np
import json
import itertools

width = 14
height = 14
block = 1

        
epsilon = 0.1
lmd = 0.7
gamma = 0.5


policy = []

qs = [''.join(s) for s in list(itertools.product(*[['0','1']] * 4))]

widths = ['0','1','-1']
heights = ['2','3','-1']

q = {}
for i in widths:
    for j in heights:
        for k in qs:
            q[str((i,j,k))] = [0,0,0,0]
    


env = gym.make('snake-v0')
observation = env.reset() 

obs, reward, done, info = env.step(env.action_space.sample())

attempts = []
scores = []

for i in range(1,110):
    
    if(i % 100 == 0):
        epsilon = 0
    game_controller = env.controller

    grid_object = game_controller.grid
    grid_pixels = grid_object.grid

    snakes_array = game_controller.snakes
    snake_object1 = snakes_array[0]

    done = False
    count = 1
    while not done:
        if(i >=100):
            env.render()
        snake = list(snake_object1.body)
        head = tuple(snake_object1.head)
        for j in range(len(snake)):
            snake[j] = tuple(list(snake[j]))


        snake.append(head)
        
        foodx, foody = 0, 0
        for y in range(0,height * 10,10):
            for x in range(0,width * 10,10):
                if (np.array_equal(obs[y][x],np.array([0,0,255]))):
                    foodx, foody = x / 10, y / 10
                    break


        food = (foodx, foody)

        
        head = snake[-1]
        dX = food[0] - head[0]
        dY = food[1] - head[1]

        if dX > 0:
            pX = '1' 
        elif dX < 0:
            pX = '0' 
        else:
            pX = '-1'
                
        if dY > 0:
            pY = '3'
        elif dY < 0:
            pY = '2'
        else:
            pY = '-1'

        vcs = [
            [head[0]-block, head[1]],   
            [head[0]+block, head[1]],         
            [head[0],head[1]-block],
            [head[0], head[1]+block],
        ]

        
        vicinity = []
        for vc in vcs:
            if vc[0] < 0 or vc[1] < 0 or vc[0] >= width or vc[1] >= height or vc in snake[:-1]: 
                vicinity.append('1')
            else:
                vicinity.append('0')
        vic = ''.join(vicinity)
    
        state = [(dX, dY), (pX, pY), vic, food]


        
        scores = q[str((state[1][0],state[1][1],state[2]))]
    
        options = [np.random.randint(0, 4), scores.index(max(scores))]
        probs = [epsilon, 1 - epsilon]
        action =  random.choices(options, probs)[0]
    
        policy.append([state, action])
        
        obs, rew, done, _ = env.step(action)
        if rew == 1:
            count += 1
        dead = False

        if done:
            dead = True
        
        
        pol = policy[::-1]
        reward = 0
        for j in range(len(pol[:-1])):
            if dead: 
                state = str((pol[0][0][1][0],pol[0][0][1][1],pol[0][0][2]))
                reward = -1
            
                q[state][pol[0][1]] = (1-lmd) * q[state][pol[0][1]] + lmd * reward 
                dead = False
            else:
                if (pol[j+1][0][3] != pol[j][0][3]) or abs(pol[j+1][0][0][0]) > abs(pol[j][0][0][0]) or abs(pol[j+1][0][0][1]) > abs(pol[j][0][0][1]): 
                    reward = 1
                else:
                    reward = -1 
            
                state = str((pol[j+1][0][1][0],pol[j+1][0][1][1],pol[j+1][0][2]))
                new_state = str((pol[j][0][1][0],pol[j][0][1][1],pol[j][0][2]))
                q[state][pol[j+1][1]] = (1-lmd) * (q[state][pol[j+1][1]]) + lmd * (reward + gamma*max(q[new_state])) 
    

        
        

    print(i, count)
    attempts.append(i)
    scores.append(count)
    env.reset()
    

