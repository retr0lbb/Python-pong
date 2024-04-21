import pygame, sys
import random
import time

pygame.init()
clock = pygame.time.Clock()

class Ball:
    size = 25
    x1 = 0
    y1 = 0
    vx = 0
    vy = 0
    
    max_speed = 30
    kinematic = 0

    def __init__(self, size, x, y):
        self.size = size
        self.x1 = x
        self.y1 = y
    

    def draw(self):
        self.kinematic = pygame.Rect((screen_width / 2 -self.size/2), (screen_height/2 - self.size/2), self.size, self.size)

    def restart_at_center(self):
        self.kinematic.x = round(screen_width/2 - self.size/2)
        self.kinematic.y = round(screen_height/2 - self.size/2)
        self.vx = 0
        self.vy = 0

        while abs(self.vx) <= 2 and abs(self.vy) <= 1:
            self.vx = random.uniform(-6, 6)
            self.vy = random.uniform(-6, 6)

    
    def bounce_collison(self):
        if self.kinematic.top <= 0 or self.kinematic.bottom >= screen_height:
            #increment y speed
            if abs(self.vy) < self.max_speed:
                self.vy *= -1.5
            else:
                self.vy *= -1
        if self.kinematic.left <= 0 or self.kinematic.right >= screen_width:
            
            if self.vx < 0:
                enemy.points += 1
            else:
                player1.points += 1

            self.restart_at_center()
        
        if self.kinematic.colliderect(player1.drawReturn) or ball.kinematic.colliderect(enemy.drawReturn):
            if abs(self.vx) < self.max_speed:
                self.vx *= -1.5
            else:
                self.vx *= -1
        
        if abs(self.vx) > self.max_speed:
            self.vx = self.max_speed if self.vx > 0 else -self.max_speed
        if abs(self.vy) > self.max_speed:
            self.vy = self.max_speed if self.vy > 0 else -self.max_speed

class Player:
    height = 20
    width = 10
    color = "red"
    velocity = 0
    speed = 10
    points = 0

    drawReturn = 0

    x1 = 0
    y1 = 0

    def __init__(self, height, width, color, x1, y1):
        self.color = color
        self.height = height
        self.width = width
        self.x1 = x1
        self.y1 = y1

    def draw(self):
        self.drawReturn = pygame.Rect(self.x1, self.y1, self.width, self.height)
    
    def check_ground_collision(self):
        if self.drawReturn.top <= 0:
            self.drawReturn.top = 0
        if self.drawReturn.bottom >= screen_height:
            self.drawReturn.bottom = screen_height

 
gameover = False
points_to_win = 5

message = lambda m, c, pos= None: screen.blit(
    pygame.font.SysFont("Segoe UI", 25)
    .render(m, True, c),
    pos if pos else [screen_width/6, screen_height/3]
)

screen_width = 1200
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height ))
pygame.display.set_caption("Pong Game")


player1 = Player(120, 20, "white", 30, (screen_height/2 - 60))
enemy = Player(120, 20, "red", (screen_width -30 -20), (screen_height/2 - 60))
enemy.speed = 8
ball = Ball(20, (screen_width/2 - 10), (screen_height/2 -10))

player1.draw()
enemy.draw()
ball.draw()
ball.restart_at_center()

bg_color  = pygame.Color("gray12")
light_gray = (200, 200, 200)
red= (255, 0, 0)

font_pontuation = pygame.font.Font(None, 78)

while True:
    # game over logic
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                    
                if event.key == pygame.K_RETURN:
                    gameover = False
                    player1.points = 0
                    enemy.points = 0

                    player1.drawReturn.y = (screen_height/2 - player1.height/2)
                    enemy.drawReturn.y = (screen_height/2 - enemy.height/2)

        screen.fill((255, 255, 255))
        message("GAME OVER", (255, 0, 0), [38, 38])
        if player1.points > 10:
            message(f"Player 1 ganhou de {points_to_win} a {enemy.points}", (255, 0, 0), [70, 38])
        else:
            message(f"Bot 1 ganhou de {points_to_win} a {player1.points}", (255, 0, 0), [38, 70])
        
        message("Pressione 'Enter' para reiniciar o jogo ou pressione q para sair", (255, 0, 178))


        pygame.display.flip() 
        clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # controlls

            if event.key == pygame.K_r:
                ball.restart_at_center()

            if event.key == pygame.K_UP:
                player1.velocity = -player1.speed
            if event.key == pygame.K_DOWN:
                player1.velocity = player1.speed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player1.velocity = 0
            if event.key == pygame.K_DOWN:
                player1.velocity = 0
                

    #fisics

    ball.kinematic.x += ball.vx
    ball.kinematic.y += ball.vy

    ball.bounce_collison()

    player1.drawReturn.y += player1.velocity
    player1.check_ground_collision()

    if enemy.drawReturn.y > ball.kinematic.y:
        enemy.velocity = -enemy.speed
    if enemy.drawReturn.y < ball.kinematic.y:
        enemy.velocity = enemy.speed

    enemy.drawReturn.y += enemy.velocity
    enemy.check_ground_collision()

    if player1.points >= points_to_win or enemy.points >= points_to_win:
        gameover = True



    #visual
    screen.fill(bg_color)
    pygame.draw.aaline(screen, light_gray, (screen_width/2, 0), (screen_width/2, screen_height))
    pygame.draw.rect(screen, light_gray, player1.drawReturn)
    pygame.draw.rect(screen, red, enemy.drawReturn)
    pygame.draw.rect(screen, light_gray, ball.kinematic)

    playe1_points = font_pontuation.render(f"{player1.points}", True, (255, 255, 255))
    enemy_points = font_pontuation.render(f"{enemy.points}", True, (255, 255, 255))


    player1_text_width = playe1_points.get_width()
    enemy_text_width = enemy_points.get_width()


    player1_text_position = (screen_width // 4 - player1_text_width// 2, 64)
    enemy_text_position = (3* screen_width // 4 - enemy_text_width // 2, 64)


    screen.blit(playe1_points, player1_text_position)
    screen.blit(enemy_points, enemy_text_position)


    pygame.display.flip()
    clock.tick(60)



