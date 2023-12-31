import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 700))
    screen.blit(floor_surface, (floor_x_pos + 500, 700))

def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bot_pipe = pipe_surface.get_rect(midtop = (750, random_pipe_position))
    top_pipe = pipe_surface.get_rect(midbottom = (750, random_pipe_position - 250))
    return bot_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe =pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 850:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * -3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == "main_game":
        score_surface = game_font.render(str(int(score)), True,(255,255,255))
        score_rect = score_surface.get_rect(center = (250, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(250, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f"high_score: {int(high_score)}", True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(250, 670))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()

# creating screen
screen_width = 500
screen_height = 850
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# creating tile of game
game_font = pygame.font.Font("04B_19.TTF", 40)
pygame.display.set_caption("JUMPY BIRD")

# game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0

# loading font
game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center = (250, 360))

# loading background/floor and scaling it
bg_surface = pygame.image.load("assets/background-day.png").convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

# scaling assets
bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-downflap.png"))
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-midflap.png"))
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/redbird-upflap.png"))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 400))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


# loading pipes, positioning, and scaling
pipe_surface = pygame.image.load("assets/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400,500,600]

#sound


while True:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8

            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 400)
                bird_movement = 0
                score = 0


        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, -200))

    if game_active:
        #movement
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)

         #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.006
        score_display("main_game")
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -500:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)