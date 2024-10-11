# 체스판 - LxL -  빈칸, 함정, 벽, 체스판 밖도 벽
# 기사 초기 위치 (r,c), (r,c)를 좌측 상단으로하여 직사각형 형태 
# 기사 초기 체력 k

# 기사 이동 
# 상하좌우 중 한칸 이동 가능 (왕에게 명령)
# 이동 위치에 다른 기사 있으면 연쇄적으로 한칸 밀림
# 연쇄 이동에 벽이 있다면 이동 불가
# 사라진 기사에게 명령 불가

# 대결 데미지
# 명령 -> 다른 기사 밀치면, 다른 기사는 피해 - hxw에 놓여 있는 함정의 수만큼
# 체력 이상의 데미지 받으면 사라짐
# 명령을 받은 기사는 피해 입지 않고, 기사들은 모두 밀린 이후 데미지 얻음
# 밀렸더라도 밀쳐진 위치에 함정 없으면 피해 입지 않음 

import copy
from collections import deque

L, N, Q = map(int, input().split())

# 0, 빈칸, 1, 함정, 2, 벽
chess = [list(map(int, input().split())) for _ in range(L)]
# (r,c,h,w,k)
gisa = [list(map(int, input().split())) for _ in range(N)]
# (i, d) - i 번째 기사가 d 방향으로 한칸 이동 
# d 0 위, 1 오른쪽, 2 아래쪽, 3 왼쪽 
order = [list(map(int, input().split())) for _ in range(Q)]
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]

# 일단 gisa 위치, 체력를 저장해야 함 
pos = [[] for _ in range(N+1)]
strength = [0] * (N+1)
for i, g in enumerate(gisa):
    for h in range(0, g[2]):
        for w in range(0, g[3]):
            pos[i+1].append((g[0]+h, g[1]+w))
    strength[i+1] = g[4]

# 범위 검사 + 벽 검사
def is_in_not_wall(y, x):
    return (1<=y<=L and 1<=x<=L and chess[y-1][x-1] != 2)

#rint(pos)
#print(strength)
for i, d in order:
    # 움직임 방향
    mov_x = dx[d]
    mov_y = dy[d]

    # 이동에 성공하는 지 
    can_move = True

    # 현재 기사 위치 -> 이동 위치
    tmp_pos = []
    other_checking = deque([])
    move_list = []
    visited = [False] * (N+1)
    visited[i] = True
    for y, x in pos[i]:
        ny = y + mov_y
        nx = x + mov_x
        if not is_in_not_wall(ny, nx):
            can_move = False
            break
        tmp_pos.append((ny, nx))
        for o in range(1, len(pos)): 
            if i != o and (ny, nx) in pos[o] and visited[o] == False: # 연쇄 검사 필요한 리스트 큐에 삽입 (첫번째 연쇄)
                other_checking.append(o)
                visited[o] = True
                move_list.append(o)
        
    #print(i, move_list)

    # 이동 위치와 다른 기사 겹치는 경우 -> 연쇄 이동 검사 (두번째 이상 연쇄)
    if can_move and len(other_checking) > 0:
        while other_checking:
            o = other_checking.popleft()
            
            for y, x in pos[o]:
                ny = y + mov_y
                nx = x + mov_x

                if not is_in_not_wall(ny, nx): # 연쇄에서 range나가거나 벽 붙이치면 역시 실패 -> 종료 
                    can_move = False
                    other_checking = deque([])
                    break

                for o_ in range(1, len(pos)): 
                    if visited[o_] == False and (ny, nx) in pos[o_]:
                        other_checking.append(o_)
                        visited[o_] = True
                        move_list.append(o_)
    #print(i, move_list, can_move)
    # 검사 다 끝냈으면 이동 + 데미지 계산
    if can_move:
        pos[i] = tmp_pos # 현재 기사 이동
        if len(move_list) > 0:
            for o in move_list:
                tmp_pos = []
                for y, x in pos[o]:
                    ny = y + mov_y
                    nx = x + mov_x
                    if chess[ny-1][nx-1] == 1: # 데미지 계산
                        strength[o] -= 1
                    tmp_pos.append((ny, nx))
                pos[o] = tmp_pos # 연쇄 기사 이동 
                if strength[o] <= 0:
                    pos[o] = []
    # print(i, d)
    # print(pos)
    # print(strength)
    
total_d = 0
# print(pos)
# print(strength)
for i, s in enumerate(strength[1:]):
    demage = gisa[i][4] - s
    if len(pos[i+1]) == 0:
        demage = 0
    total_d += demage

print(total_d)