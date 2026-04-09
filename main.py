import pygame
import time
import random

# 1. KHỞI TẠO
pygame.init()

# Cấu hình màu sắc
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (21, 21, 21)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Cấu hình màn hình
width, height = 600, 400
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rắn Săn Mồi Pro - Python')

clock = pygame.time.Clock()
snake_block = 15  # Tăng kích thước rắn một chút cho dễ nhìn
initial_speed = 10

# Cấu hình Font
font_style = pygame.font.SysFont("arial", 25)
score_font = pygame.font.SysFont("consolas", 20)

# 2. CÁC HÀM TIỆN ÍCH
def display_score(score, high_score):
    value = score_font.render(f"Điểm: {score}  |  Kỷ lục: {high_score}", True, yellow)
    dis.blit(value, [10, 10])

def draw_snake(snake_block, snake_list):
    for i, x in enumerate(snake_list):
        # Đầu rắn màu xanh dương, thân màu đen
        color = blue if i == len(snake_list) - 1 else black
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])

def show_message(msg, color):
    mesg = font_style.render(msg, True, color)
    # Căn giữa văn bản
    text_rect = mesg.get_rect(center=(width/2, height/2.5))
    dis.blit(mesg, text_rect)

# 3. VÒNG LẶP CHÍNH CỦA GAME
def gameLoop():
    game_over = False
    game_close = False
    
    high_score = 0
    current_speed = initial_speed

    # Vị trí ban đầu
    x1, y1 = width / 2, height / 2
    x1_change, y1_change = 0, 0

    snake_List = []
    Length_of_snake = 1

    # Tạo thức ăn ngẫu nhiên
    foodx = round(random.randrange(0, width - snake_block) / 15.0) * 15.0
    foody = round(random.randrange(0, height - snake_block) / 15.0) * 15.0

    while not game_over:

        # MÀN HÌNH KHI THUA
        while game_close:
            dis.fill(white)
            show_message("BẠN ĐÃ THUA!", red)
            
            score = Length_of_snake - 1
            score_msg = score_font.render(f"Tổng điểm: {score}", True, black)
            dis.blit(score_msg, [width/2.5, height/1.8])
            
            hint_msg = score_font.render("Ấn C để Chơi tiếp hoặc Q để Thoát", True, blue)
            dis.blit(hint_msg, [width/4.5, height/1.5])
            
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # ĐIỀU KHIỂN
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0

        # Kiểm tra va chạm tường
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True
        
        x1 += x1_change
        y1 += y1_change
        dis.fill(white) # Nền màu trắng
        
        # Vẽ thức ăn
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        
        # Xử lý thân rắn
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Kiểm tra tự đâm vào thân
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        draw_snake(snake_block, snake_List)
        display_score(Length_of_snake - 1, high_score) # Tạm thời chưa lưu file nên high_score để minh họa
        
        pygame.display.update()

        # Kiểm tra khi ăn mồi
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 15.0) * 15.0
            foody = round(random.randrange(0, height - snake_block) / 15.0) * 15.0
            Length_of_snake += 1
            # Tăng tốc độ mỗi khi ăn 5 mồi
            if Length_of_snake % 5 == 0:
                current_speed += 1

        clock.tick(current_speed)

    pygame.quit()
    quit()

# Chạy game
if __name__ == "__main__":
    gameLoop()