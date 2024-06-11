import sys, pygame

pygame.init()

size = width, height = 1920, 1080
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("new.gif")
ball_rectangle = ball.get_rect()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ball_rectangle = ball_rectangle.move(speed)
    if ball_rectangle.left < 0 or ball_rectangle.right > width:
        speed[0] = -speed[0]
    if ball_rectangle.top < 0 or ball_rectangle.bottom > height:
        speed[1] = -speed[1]

    screen.fill(black)
    screen.blit(ball, ball_rectangle)
    pygame.display.flip()
