'''
오락실 pang 게임 만들기

[게임 조건]
1. 캐릭터는 화면 아래에 위치, 좌우로만 이동 가능
2. 스페이스를 누르면 무기를 쏘아 올림
3. 큰 공 1개가 나타나서 바운스
4. 무기에 닿으면 공은 작은 크기 2개로 분할, 가장 작은 크기의 공은 사라짐
5. 모든 공을 없애면 게임 종료(성공)
6. 캐릭터는 공에 닿으면 게임 종료(실패)
7. 시간 제한 99초 초과시 게임 종료(실패)
8. FPS는 30으로 고정(필요시 speed 값을 조정)

[게임 이미지]
1. 배경 : 640 * 480(가로, 세로) - background.png
2. 무대 : 640 * 50 - stage.png
3. 캐릭터 : 33 * 60 - character.png
4. 무기 : 20 * 430 weapon.png
5. 풍선 : 160 * 160, 80 * 80, 40 * 40, 20 * 20 - ball1.png ~ ball4/png
'''
import os

import pygame

# 기본 초기화(반드시 해야하는 것들)
# pygame 을 import 하면 반드시 초기화를 해줘야한다.
pygame.init()

# 화면 크기 설정
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("SPLIT BALLOON GAME")

# 폰트 설정
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()

# 게임 종료 메시지
game_result = "GAME OVER"

# 이동할 좌표
character_to_x = 0
# 이동 속도
character_speed = 0.6

# FPS
clock = pygame.time.Clock()

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
life = 3
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]
stage_y_pos = screen_height - stage_height

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = screen_width / 2 - character_width / 2
character_y_pos = screen_height - character_height - stage_height

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weapon_speed = 10

# 풍선 만들기(4개 크기에 대해 따로 처리)
balloon_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

# 풍선 크기에 따른 최초 스피드
balloon_speed_y = [-18, -15, -12, -9]

# 풍선들
balloons = []

# 최초 발생 큰 풍선 추가
balloons.append({
    "pos_x": 50,  # 풍선의 x 좌표
    "pos_y": 50,  # 풍선의 y좌표
    "img_idx": 0,
    "to_x": 3,  # x축 이동 방향
    "to_y": -6,  # y축 이동 방향
    "init_speed_y": balloon_speed_y[0]  # y 최초 속도
})

# 사라질 무기와 공 정보 저장 변수
weapon_to_remove = -1
ballons_to_remove = -1

running = True
while running:
    dt = clock.tick(30)  # 게임화면의 초당 프레임 수

    # 2. 이벤트 처리(키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트가 발생하였는가?
            running = False  # 게임이 진행되지 않음

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                # 무기 위치 정의
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_pos += character_to_x * dt
    # 3. 게임 캐릭터 위치 정의
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = screen_width - character_width

    # 무기 이동 조절
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 풍선 위치 정의
    for balloon_idx, balloon_val in enumerate(balloons):
        balloon_pos_x = balloon_val["pos_x"]
        balloon_pos_y = balloon_val["pos_y"]
        balloon_img_idx = balloon_val["img_idx"]

        balloon_size = balloon_images[balloon_img_idx].get_rect().size
        balloon_width = balloon_size[0]
        balloon_height = balloon_size[1]

        # 좌,우 벽에 닿았을 때 공 위치 변경(튕겨나가는 효과)
        if balloon_pos_x < 0 or balloon_pos_x > screen_width - balloon_width:
            balloon_val["to_x"] = balloon_val["to_x"] * -1

        # 스테이지에 튕겨서 올라가는 효과
        if balloon_pos_y >= screen_height - stage_height - balloon_height:
            balloon_val["to_y"] = balloon_val["init_speed_y"]
        # 그 외의 경우에는 속도를 줄여나감(포물선 효과)
        else:
            balloon_val["to_y"] += 0.5

        balloon_val["pos_x"] += balloon_val["to_x"]
        balloon_val["pos_y"] += balloon_val["to_y"]

    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for balloon_idx, balloon_val in enumerate(balloons):
        balloon_pos_x = balloon_val["pos_x"]
        balloon_pos_y = balloon_val["pos_y"]
        balloon_img_idx = balloon_val["img_idx"]

        # 공 rect 정보 업데이트
        balloon_rect = balloon_images[balloon_img_idx].get_rect()
        balloon_rect.left = balloon_pos_x
        balloon_rect.top = balloon_pos_y

        # 공과 캐릭터 충돌 처리
        if character_rect.colliderect(balloon_rect):
            if life == 0:
                running = False
                break
            life -= 1
            character_x_pos = 10
            character_y_pos = screen_height - character_height - stage_height

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_x_pos = weapon_val[0]
            weapon_y_pos = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_x_pos
            weapon_rect.top = weapon_y_pos

            # 충돌 체크
            if weapon_rect.colliderect(balloon_rect):
                weapon_to_remove = weapon_idx  # 해당 무기를 없애기 위한 값 설정
                ballons_to_remove = balloon_idx  # 해당 풍선을 없애기 위한 값 설정

                if balloon_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    balloon_width = balloon_rect.size[0]
                    balloon_height = balloon_rect.size[1]

                    # 나눠진 공 정보
                    small_balloon_rect = balloon_images[balloon_img_idx + 1].get_rect()
                    small_balloon_width = small_balloon_rect.size[0]
                    small_balloon_height = small_balloon_rect.size[1]
                    # 왼쪽으로 튕겨나가는 작은 공
                    balloons.append({
                        "pos_x": balloon_pos_x + (balloon_width / 2) - (small_balloon_width / 2),  # 풍선의 x 좌표
                        "pos_y": balloon_pos_y + (balloon_height / 2) - (small_balloon_height / 2),  # 풍선의 y좌표
                        "img_idx": balloon_img_idx + 1,
                        "to_x": -3,  # x축 이동 방향
                        "to_y": -6,  # y축 이동 방향
                        "init_speed_y": balloon_speed_y[balloon_img_idx + 1]  # y 최초 속도
                    })
                    # 오른쪽으로 튕겨나가는 작은 공
                    balloons.append({
                        "pos_x": balloon_pos_x + (balloon_width / 2) - (small_balloon_width / 2),  # 풍선의 x 좌표
                        "pos_y": balloon_pos_y + (balloon_height / 2) - (small_balloon_height / 2),  # 풍선의 y좌표
                        "img_idx": balloon_img_idx + 1,
                        "to_x": +3,  # x축 이동 방향
                        "to_y": -6,  # y축 이동 방향
                        "init_speed_y": balloon_speed_y[balloon_img_idx + 1]
                    })
                break
        else :
            continue
        break

    if ballons_to_remove > -1:
        del balloons[ballons_to_remove]
        ballons_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤경우 게임 종료
    if len(balloons) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기 - screen.blit
    screen.blit(background, (0, 0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balloons):
        balloon_pos_x = val["pos_x"]
        balloon_pos_y = val["pos_y"]
        balloon_img_idx = val["img_idx"]
        screen.blit(balloon_images[balloon_img_idx], (balloon_pos_x, balloon_pos_y))

    screen.blit(stage, (0, stage_y_pos))
    screen.blit(character, (character_x_pos, character_y_pos))

    now_life = game_font.render(str(int(life)), True, (0, 0, 0))
    screen.blit(now_life, (screen_width - 30, 10))

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render(f"Time : {int(total_time - elapsed_time)}", True, (0, 0, 0))
    screen.blit(timer, (10, 10))

    # 시간 초과
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update()
# 게임 오버 메시지 저장
msg = game_font.render(game_result, True, (0, 0, 0))
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))

screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()
