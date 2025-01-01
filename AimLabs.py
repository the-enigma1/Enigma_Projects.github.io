import pygame
import math
import random
import time

pygame.init()

width, height = 800, 600

# Initializing a pygame window
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Aim Labs")

target_increment = 500                 #Generates new targets after every 500ms
target_event = pygame.USEREVENT        #Custom pygame event for target generation.

target_padding = 30                    #Space from the border of the window
bg_color = (0, 25, 40)                 #background color of the window

lives = 3                               
top_bar_height = 50                      #stats bar height
label_font = pygame.font.SysFont("comicsans", 24)    #used font and its size

class Target:                   #default values of the targets
    max_size = 30
    growth_rate = 0.2           #target size increases by the rate of 20ms
    color = 'red'
    second_color = 'white'

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0           #initial size of the target from 0 
        self.grow = True        #tells that target is increasing

    def update(self):
        if self.size + self.growth_rate >= self.max_size:     
            self.grow = False       #when the size of target reaches 30 it will stop growing

        if self.grow:
            self.size += self.growth_rate     #increase the size of the target on every call until it reaches 30
        else:
            self.size -= self.growth_rate     #decrease the size of the target on every call until it reaches 0 again

    def draw(self, win):                      #now we start drawing the targets
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.second_color, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.color, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.second_color, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):              #this function allows us to hit the targets
        dis = math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)  #using distance formula to calculate distance b/w two points
        return dis <= self.size        #check if the hit is within the boundry of target or not

def draw(win, targets):    
    win.fill(bg_color)             #clears any objects on window before drawing new frames

    for target in targets:           #this loop will iterate over each target present in the list below
        target.draw(win)

def format_time(secs):     #This function converts the given time in minutes,seconds format
    milli = math.floor(int(secs * 1000 % 1000) / 100) 
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time, targets_pressed, misses):     #This function draws the stats bar
    pygame.draw.rect(win, "grey", (0, 0, width, top_bar_height))
    time_label = label_font.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    hits_label1 = label_font.render(f"Hits: {targets_pressed}", 1, "black")
    lives_label1 = label_font.render(f"Lives: {lives - misses}", 1, "black")

    win.blit(time_label, (50, 5))
    win.blit(hits_label1, (350, 5))
    win.blit(lives_label1, (650, 5))

def end_screen(win, elapsed_time, targets_pressed, clicks):    #This function displays the user stats after game ends
    win.fill(bg_color)
    time_label = label_font.render(f"Time: {format_time(elapsed_time)}", 1, "white")
    hits_label1 = label_font.render(f"Hits: {targets_pressed}", 1, "white")
    accuracy = round(targets_pressed / clicks * 100, 1)
    accuracy_label1 = label_font.render(f"Accuracy: {accuracy}%", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(hits_label1, (get_middle(hits_label1), 200))
    win.blit(accuracy_label1, (get_middle(accuracy_label1), 300))

    restart_button = pygame.Rect(width // 2 - 100, 400, 200, 50)
    pygame.draw.rect(win, "red", restart_button)
    restart_label = label_font.render("Restart", 1, "white")
    win.blit(restart_label, (get_middle(restart_label), 410))

    pygame.display.update()

    run = True
    while run:            #through this loop we will control closing & restarting of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    main()

            if event.type == pygame.KEYDOWN:
                quit()

def get_middle(surface):
    return width / 2 - surface.get_width() / 2

def main():   
    run = True
    targets = [] #list to store all active target objects.
    clock = pygame.time.Clock()  #controls the speed of loop

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(target_event, target_increment)

    while run:
        clock.tick(60)  #now this loop will run at 60 fps
        click = 0
        mouse_pos = pygame.mouse.get_pos()         #captures mouse current position
        elapsed_time = time.time() - start_time   #calculates the time since the game started

        for event in pygame.event.get():        #this loop will handle happening events
            if event.type == pygame.QUIT:  
                run = False  
                break

            if event.type == target_event: #spawn new targets at random positions
                x = random.randint(target_padding, width - target_padding)
                y = random.randint(target_padding + top_bar_height, height - target_padding)  #avoids averlapping with stats bar
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1 #count clicks to measure accuracy

        for target in targets:
            target.update()

            #disposing the created targets
            if target.size <= 0:
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1

        if misses >= lives:
            end_screen(win, elapsed_time, targets_pressed, clicks)  # ends the game

        draw(win, targets)
        draw_top_bar(win, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()  # Quits window after the loop ends

# Ensures that the function runs
if __name__ == "__main__":
    main()
