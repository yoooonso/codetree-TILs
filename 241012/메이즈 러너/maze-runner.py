# 미로 탈출 - M 참가자, N 격자
# 미로 칸 - 1. 빈칸(이동 가능), .2. 벽(이동 불가, 내구도 존재, 회전할 때 내구도 감소, 0이되면 빈칸), 3. 출구 - 즉시 탈출
# 참가자는 한칸씩 이동
    # 상하좌우 
    # 동시 이동 (모든 참가자)
    # 움직인 칸은 현재보다 출구까지 최단거리가 가까워야 함 
    # 움직이는 칸 - 2개 이상이면 상하 우선
    # 움직일 수 없는 상황이면 x
    # 한칸에 2명이상의 참가자 있을 수 있음 ****

# 모든 참가자 이동 후 미로 회전
    # 출구, 한명 이상의 참가자를 포함한 가장 작은 정사각형을 잡고, 90도로 회전 - 이때 내구도 1씩 깎임
    # 가장 작은 크기의 정사각형이 2개 이상이면, r 작은 것, c 작은 것

# K 초동안, K초 전에 모든 참가자가 탈출하면 게임 끝
# 게임 끝났을때, 모든 참가자들의 이동 거리 합과 출구 좌표 출력

import copy
from collections import deque

N, M, K = map(int, input().split())
miro = [list(map(int, input().split())) for _ in range(N)] # 0, 빈칸, 1이상 벽
parties = [list(map(int, input().split())) for _ in range(M)]
exit = list(map(int, input().split()))
finish = [False] * M

move_sum = 0 # 이동거리 합 - 움직일 때 마다 업데이트
dx = [0, 0, -1, 1] # 상하 우선
dy = [-1, 1, 0, 0]

def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1-y2)

def is_in(x, y):
    return 1<= x <=N and 1<=y <=N
for _ in range(K):
    # 참가자 이동 
    for i, party in enumerate(parties):
        if finish[i] == False:
            x = party[1]
            y = party[0]
            cur_min = distance(x, y, exit[1], exit[0])
            move = False
            for d in range(4):
                nx = x + dx[d]
                ny = y + dy[d]

                if is_in(nx, ny) and miro[ny-1][nx-1] == 0 and cur_min > distance(nx, ny, exit[1], exit[0]):
                    # 빈칸 이면 - 업데이트, 전체 이동 거리 증가
                    cur_min = distance(nx, ny, exit[1], exit[0])
                    parties[i] = [ny, nx]
                    move = True
                    if cur_min == 0:
                        finish[i] = True
            if move:
                move_sum += 1
    
    if finish == [True] * M:
        break

    #print(parties)
    
    # 회전 -> 미로, 참가자, 출구 모두 업데이트 
    # 일단 참가자 선택 
    min_dis_with_e = float('inf')
    min_x, min_y = None, None
    select_party = None
    for i, party in enumerate(parties):
        if finish[i] == False:
            w = abs(party[1] - exit[1]) + 1
            h = abs(party[0] - exit[0]) + 1
            if h < w:
                cur_min = w
            else:
                cur_min = h
            
            if cur_min < min_dis_with_e \
                or (cur_min == min_dis_with_e and party[1] < min_x)\
                or (cur_min == min_dis_with_e and party[1] == min_x and party[0] < min_y):
                select_party = i
                min_dis_with_e = cur_min
                min_x, min_y = party[1], party[0]
    
     # 참가자와 함께 회전 
    # 회전 부분 copy
    length = min_dis_with_e

    if parties[select_party][1] < exit[1]:
        square_start_x = max(1, exit[1] - length + 1)
    else:
        square_start_x = max(1, parties[select_party][1] - length + 1)
    if parties[select_party][0] < exit[0]:
        square_start_y = max(1, exit[0] - length + 1)
    else:
        square_start_y = max(1, parties[select_party][0] - length + 1)

    squre = copy.deepcopy([m[square_start_x-1:square_start_x-1+length] for m in miro[square_start_y-1:square_start_y-1+length]])
    new_parties = copy.deepcopy(parties)
    #copy_x_party, copy_y_party = parties[select_party][1] - square_start_x, parties[select_party][0] - square_start_y 
    copy_x_exit, copy_y_exit = exit[1] - square_start_x, exit[0] - square_start_y
    #print(copy_x_party, copy_y_party, copy_x_exit, copy_y_exit)
    # print(exit)
    # print(squre)
    # copy한 부분 90도 회전 
    #squre_rotate = [[] * length for i in ragne(length)]
    for i in range(length):
        for j in range(length):
            # 회전한 부분 내구도 깎기 & 원래 미로에 붙이기 
            if squre[i][j] > 0:
                miro[square_start_y -1 + j][square_start_x -1 + length -1 -i] = squre[i][j] - 1
            else:
                miro[square_start_y -1 + j][square_start_x -1 + length -1 -i] = squre[i][j]
            
            # exit & 참가자 업데이트
            for p in range(len(parties)):
                if parties[p][1] - square_start_x == j and parties[p][0] - square_start_y == i:
                    new_parties[p] = [square_start_y + j, square_start_x + length -1 -i]

            if i == copy_y_exit and j == copy_x_exit:
                exit = (square_start_y + j, square_start_x + length -1 -i)

    parties = new_parties
    # print(parties)
    

# 참가자 이동 거리 합 
print(move_sum)
# 출구 좌표 
print(exit[0], exit[1], end=" ")