import pygame

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((1000, 667))
pygame.display.set_caption('game')
icon = pygame.image.load('image/OIP (1).jpg').convert()
pygame.display.set_icon(icon)
bg = pygame.image.load('image/phon.png').convert_alpha()
fail = pygame.image.load('image/fail.png')

walk_right = [
    pygame.image.load('image/right/1.png').convert_alpha(),
    pygame.image.load('image/right/2.png').convert_alpha(),
    pygame.image.load('image/right/3.png').convert_alpha(),
    pygame.image.load('image/right/4.png').convert_alpha(),
    pygame.image.load('image/right/5.png').convert_alpha(),
    pygame.image.load('image/right/6.png').convert_alpha(),
    pygame.image.load('image/right/7.png').convert_alpha(),
    pygame.image.load('image/right/8.png').convert_alpha()
]

walk_left = [
    pygame.image.load('image/left/l1.png').convert_alpha(),
    pygame.image.load('image/left/l2.png').convert_alpha(),
    pygame.image.load('image/left/l3.png').convert_alpha(),
    pygame.image.load('image/left/l4.png').convert_alpha(),
    pygame.image.load('image/left/l5.png').convert_alpha(),
    pygame.image.load('image/left/l6.png').convert_alpha(),
    pygame.image.load('image/left/l7.png').convert_alpha(),
    pygame.image.load('image/left/l8.png').convert_alpha(),
]

cloud = pygame.image.load('image/cloud.png').convert_alpha()
cloud_list = []

ghost = pygame.image.load('image/ghost (1).png').convert_alpha()
ghost_list = []

player_anim_count = 0
bg_x = 0
player_speed = 15
player_x = 150
player_y = 487

is_jump = False
jump_count = 9

cloud_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cloud_timer, 3500)

k = 0
count = pygame.font.Font('font/Roboto-Black.ttf', 20)
label_count = count.render(f'Очки:{k}', False, (0, 0, 0))
label_count_rect = label_count.get_rect(topleft=(0, 0))

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 7000)

label = pygame.font.Font('font/Roboto-Black.ttf', 40)
restart_label = label.render('Перезапуск', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(400, 200))

gameplay = True

bullet = pygame.image.load('image/bullet.png').convert_alpha()
bullets = []
bullets_left = 5
running = True
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1000, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))
        if cloud_list:
            for i in cloud_list:
                screen.blit(cloud, i)
                i.x -= 5
        if ghost_list:
            for (j, el) in enumerate(ghost_list):
                screen.blit(ghost, el)
                el.x -= 10

                if player_rect.colliderect(el):
                    gameplay = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > 10:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 900:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

        if player_anim_count == 7:
            player_anim_count = 0
        else:
            player_anim_count += 1
        bg_x -= 2
        if bg_x == -1000:
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):
                screen.blit(bullet, (el.x, el.y))
                el.x += 10

                if ghost_list:
                    for (index, ghost_el) in enumerate(ghost_list):
                        if el.colliderect(ghost_el):
                            ghost_list.pop(index)
                            bullets.pop(i)

    else:
        screen.blit(fail, (250, 300))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()

        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 150
            ghost_list.clear()
            cloud_list.clear()
            bullets.clear()
            bullets_left = 5




    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == cloud_timer:
            cloud_list.append(cloud.get_rect(topleft=(1000, 50)))
        if event.type == ghost_timer:
            ghost_list.append(ghost.get_rect(topleft=(1000, 525)))
        if gameplay and keys[pygame.K_b] and event.type == pygame.KEYUP and event.key == pygame.K_b and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 40)))
            bullets_left -= 1

    clock.tick(10)