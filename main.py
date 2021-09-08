from blessed import Terminal
import random
import copy
from collections import deque 

term = Terminal()
up = term.KEY_UP
right = term.KEY_RIGHT
left = term.KEY_LEFT
down = term.KEY_DOWN
dirc = right

# -------config start---------

border = '*'
body = '🛑'
space = ' '
food = '🍕'

#initial snake position
snake = deque([[6,5], [6,4], [6,3]])
#initial food position
food_pos = [4,11]
height = 30
width = 40
score = 0
speed = 3
max_speed = 6

# ------config end-------

def empty_spaces(world, space):
    result = []
    for i in range(len(world)):
        for j in range(len(world)):
            if world[i][j] == space:
                result.append([i, j])
    return result

with term.cbreak(), term.hidden_cursor():
    print(term.home + term.clear) #clearing the screen

    world = [[space] * width for _ in range(height)]
    for i in range(height):
        world[i][0] = border
        world[i][-1] = border
    for j in range(width):
        world[0][j] = border
        world[-1][j] = border
    for s in snake:
        world[s[0]][s[1]] = body
    world[food_pos[0]][food_pos[1]] = food
    for row in world:
        print(' '.join(row))
    print('use arrow keys to move')
    print('Expand the terminal window for a better view')

    val = ''
    moving = False

    while val.lower != 'q':
        val = term.inkey(timeout = 1/speed)
        if val.code in [up, right, down]:
            moving = True
        if not moving:
            continue
        if val.code == up and dirc != down:
            dirc = up
        elif val.code == right and dirc != left:
            dirc = right
        elif val.code == down and dirc != up:
            dirc = down
        elif val.code == left and dirc != right:
            dirc = left

        head = copy.copy(snake[0])
        if dirc == up:
            head[0] -= 1
        elif dirc == right:
            head[1] += 1 
        elif dirc == down:
            head[0] += 1 
        elif dirc == left:
            head[1] -= 1

        heading = world[head[0]][head[1]]
        ate_food = False
        if heading == food:
            ate_food = True
            emptys = empty_spaces(world, space)
            food_pos = random.choice(emptys)
            world[food_pos[0]][food_pos[1]] = food
            speed = min(max_speed, speed * 1.05)
        elif heading == border:
            break
        elif heading == body and head != snake[-1]:
            break

        if not ate_food:
            tail = snake.pop()
            world[tail[0]][tail[1]] = space
        world[head[0]][head[1]] = body
        snake.appendleft(head)

        print(term.move_yz(0,0))
        for row in world:
            print(' '.join(row))

        score = len(snake) - 3
        print(f'score: {score} - speed: {speed:.1f}')
        print(term.clear_eos, end='')

print('game over!!!!!!')