# P 명의 산타 
# 루돌프 산타 박치기 - 선물 배달 방해
# 산타들은 루돌프를 잡아서 크리스마스를 구해야 함

# M 개의 턴 - 루돌프 한번 움직인 뒤, 산타 움직임(기절 산타, 탈락 산타 제외)
# 루돌프 움직임 - 가장 가까운 산타 향해 1칸 돌진 (상하좌우, 대각선 가능)
    # 같은 거리면, r좌표가 큰, c좌표가 큰
# 산타 움직임 - 1부터 P번가지, 두돌프에게 거리가 가까워지는 방향으로 1칸 이동
    # 다른 산타가 있는 칸으로는 움직일 수 없음
    # 움직일 수 있는 칸이 없다면, 이동 x
    # 움직일 수 있어도 가까워질 수 없다면, 이동 x
    # 상하좌우 이동 가능 - 가까워질 수 있는 방향이 여러개면 (상우하좌) 우선순위 따름
# 충돌 - 산타와 루돌프 같은 칸 
    # 루돌프가 움직인 경우, 산타 + C, 루돌프 이동해온 방향으로 C칸 만큼 밀림
    # 산타가 움직인 경우, 산차 + D, 자신이 이동해온 반대 방향으로 D만큰 밀림
    # 밀려난 칸이 밖이면 탈락
    # 다른 산타 있으면 상호작용
# 상호작용 - 다른 산타가 있다면, 그 다른 산타는 1칸 해당 방향으로 밀림, 
    # (연쇄적, 밀린 칸에 또 다른 산타있다면 또 다른 산타 밀림)
# 기절 - 산타는 루돌프와 충돌 후 기절, k턴이었다면, k+2에서 정상상태
# 게임 종료 - M번에 턴, 만약 중도 P명 모두 탈락이면 즉시 종료, 매턴 이후 탈락 x 산타들에게는 1점 추가 부여

import sys
import copy
import math
from collections import deque

N, M, P, C, D = map(int, sys.stdin.readline().split())
board = [[0] * (N+1) for _ in range(N+1)]
rudol_y, rudol_x =  map(int, sys.stdin.readline().split())
board[rudol_y][rudol_x] = -1
santas = [list(map(int, sys.stdin.readline().split())) for _ in range(P)]
santas_pos = [(0,0)] * P
santas_score =[0] * (P) # 산타 점수
santas_status = [True] * (P) # 산타의 상태 - 아웃인지 아닌지
stun = [-1] * P #기절 상태 t+1 기록해서 

for santa in santas:
    santas_pos[santa[0] - 1] = (santa[1], santa[2])
    board[santa[1]][santa[2]] = santa[0]

def distance(y1, x1, y2, x2):
    return (y1-y2)**2 +(x1-x2)**2

# (x, y)가 보드 내의 좌표인지 확인하는 함수입니다.
def is_inrange(x, y):
    return 1 <= x and x <= N and 1 <= y and y <= N


# 상우하좌
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]


for t in range(M): # M번 반복
    
    # 루돌프 움직임 - 어떤 산타 방향으로 갈건지
    min_dis, min_santa = float('inf'), None
    current_min = (min_dis, (-10000, -10000))
    for i in range(P):
        if santas_status[i]:
            current_val = (distance(rudol_y, rudol_x, santas_pos[i][0], santas_pos[i][1]), -santas_pos[i][0], -santas_pos[i][1])
            if current_min > current_val:
                min_santa = i
                current_min = (distance(rudol_y, rudol_x, santas_pos[i][0], santas_pos[i][1]), -santas_pos[i][0], -santas_pos[i][1])
   
    # 산타 방향으로 이동        
    if not min_santa == None:
        rudol_x_, rudol_y_ = 0, 0
        if santas_pos[min_santa][0] > rudol_y:
            rudol_y_ = 1
        elif santas_pos[min_santa][0] < rudol_y:
            rudol_y_ = -1
        if santas_pos[min_santa][1] > rudol_x:
            rudol_x_ = 1
        elif santas_pos[min_santa][1] < rudol_x:
            rudol_x_ = -1
        board[rudol_y][rudol_x] = 0
        rudol_x += rudol_x_
        rudol_y += rudol_y_


    # 루돌프 이동 시 충돌 처리
    if rudol_y == santas_pos[min_santa][0] and rudol_x  == santas_pos[min_santa][1]:
        # 충돌 발생 - 루돌프가 산타와 충돌
        santas_score[min_santa] += C
        # 산타 밀림 처리 (C만큼 이동)
        firstX = santas_pos[min_santa][1] + C * rudol_x_
        firstY = santas_pos[min_santa][0] + C * rudol_y_
     
        lastX, lastY = firstX, firstY

        stun[min_santa] = t + 1
        # 만약 이동한 위치에 산타가 있을 경우, 연쇄적으로 이동이 일어납니다.
        while is_inrange(lastX, lastY) and board[lastY][lastX] > 0:
            lastX += rudol_x_
            lastY += rudol_y_
        # 연쇄적으로 충돌 일어난 가장 마지막 위치에서 시작해서
        # 순차적으로 보드판에 있는 산타를 한칸씩 이동 시킴
        while not (lastX == firstX and lastY == firstY):
            beforeX = lastX - rudol_x_
            beforeY = lastY - rudol_y_
            if not is_inrange(beforeX, beforeY):
                break
            idx = board[beforeY][beforeX]
            if not is_inrange(lastX, lastY):
                santas_status[idx-1] = False # 아웃
            else:
                board[lastY][lastX] = board[beforeY][beforeX]
                santas_pos[idx-1] = (lastY, lastX)
            lastY, lastX = beforeY, beforeX

        santas_pos[min_santa] = (firstY, firstX)
        if is_inrange(firstX, firstY):
            board[firstY][firstX] = min_santa+1
        else:
            santas_status[min_santa] = False
    board[rudol_y][rudol_x] = -1
    

    # 산타 움직임
    for i in range(P):
        if santas_status[i] == False or stun[i] >= t: # 기절이거나, 탈락이면 스킵
            continue

        s_y, s_x = santas_pos[i][0], santas_pos[i][1]
        min_dis = distance(s_y, s_x, rudol_y, rudol_x)
        dir_select = -1
        for d in range(4):
            ny, nx = s_y+dy[d], s_x+dx[d]

            if not is_inrange(nx, ny) or board[ny][nx] > 0:
                continue

            dis = distance(ny, nx, rudol_y, rudol_x)
            if dis < min_dis:
                min_dis = dis
                dir_select = d
        
        if dir_select != -1:
            ny, nx = s_y+dy[dir_select], s_x+dx[dir_select]
    
            if rudol_y == ny and rudol_x == nx:
                # 충돌 발생 - 루돌프가 산타와 충돌
                santas_score[i] += D
                stun[i] = t+1

                moveX = -dx[dir_select]
                moveY = -dy[dir_select]

                firstX = nx + moveX * D
                firstY = ny + moveY * D
                lastX, lastY = firstX, firstY

                if not D==1:
                    # 이동 위치에 산타 있을 경우 연쇄 이동
                    while is_inrange(lastX, lastY) and board[lastY][lastX] > 0:
                        lastX += moveX
                        lastY += moveY
                    
                    # 연쇄 충돌 마지막 위치에서 시작해
                    # 순차적으로 산타 이동 
                    while lastX != firstX or lastY != firstY:
                        beforeX = lastX - moveX
                        beforeY = lastY - moveY

                        if not is_inrange(beforeX, beforeY):
                            break
                        idx = board[beforeY][beforeX]
                        if not is_inrange(lastX, lastY):
                            santas_status[idx-1]= False
                        else:
                            board[lastY][lastX] = board[beforeY][beforeX]
                            santas_pos[idx-1] = (lastY, lastX)
                        
                        lastX, lastY = beforeX, beforeY
                    
                    board[santas_pos[i][0]][santas_pos[i][1]] = 0
                    santas_pos[i] = (firstY, firstX)
                    if is_inrange(firstX, firstY):
                        board[firstY][firstX] = i+1
                    else:
                        santas_status[i] = False
            else:
                board[santas_pos[i][0]][santas_pos[i][1]] = 0
                santas_pos[i] = (ny, nx)
                board[ny][nx] = i+1

    # 탈락 산타, 점수 업데이트 
    for i in range(P):
        if santas_status[i]:
            santas_score[i] += 1

for i in range(P):
    print(santas_score[i], end=" ")