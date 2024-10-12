# 격자 NxM, 포탑 - 공격력 줄거나 늘어남, 0이하면 공격 불가
# K번 반복, 4가지 액션, 부서지지 않은 포탑이 1이 되면 즉시 중지

# 1. 공격자 선정
    # 가장 약한 포탑이 선정 - 핸디캡 적용으로 N+M만큼 공격력 증가
        # 가장 약한 포탑 - 공격력이 가장 낮은, 
        # 2개 이상이면 가장 최근에 공격한, 행과 열의 합이 가장 큰, 열 값이 가장 큰 

# 2. 공격자의 공격
    # 공격력이 가장 높은 포탑
    # 공격한 지 가장 오래된, 행과 열의 합이 가장 작은, 열 값이 가장 작은

    # 3. 레이저 공격 먼저 시도
        # 레이저 - 상하좌우 4개의 방향으로 움직임, 
        # 부서진 포탑의 위치는 지날 수 없음
        # 가장 자리 막힌 방향으로 진행하고자 하면 반대편으로 나옴
        # 공격 대상 포탑까지 최단 경로로 공격하며, 지나온 경로에는 절반만큼 공격, 대상에는 공격력만큼 피해
        # 최단 경로의 우선순위는 - 우하좌상 
        # 경로 없는 경우 4

    # 4. 레이저 안될 경우 포탄 공격
        # 공격 대상에 포탄 던지고 - 공격력만큼 피해
        # 공격 대상 주변 8칸음 - 공격력 반만큼 피해 - 반대편까지도 

# 5. 포탑 부서짐 
    # 공격력이 0 이하가 된 경우
# 6. 포탑 정비
    # 공격이 끝나면 공격과 무관했던 포탑은 공격력이 1씩 올라감 - 부서짐, 공격자, 공격받은 제외

# 마지막 공격 시점 저장

from collections import deque

N, M, K = map(int, input().split())
handi = N + M
board = [list(map(int, input().split())) for _ in range(N)]
attack = [[0]*M for _ in range(N)]

# 우하좌상 우선순위
dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

def return_search(board, attack):
    search = []
    for i in range(N):
        for j in range(M):
            # sorting 위해서, 공격력, 최근 공격 행 + 열, 열, 행
            if not board[i][j] == 0:
                search.append((board[i][j], attack[i][j], i + j, j, i)) 
    return search 

def bfs(attacker_x, attacker_y, target_x, target_y):
    queue = deque()
    visited = [[[] for __ in range(M)] for _ in range(N)]

    queue.append((attacker_x, attacker_y))
    visited[attacker_y][attacker_x] = (attacker_x, attacker_y)

    while queue:
        x, y = queue.popleft()

        if x == target_x and y == target_y:
            board[y][x] = max(0, board[y][x]- board[attacker_y][attacker_x])

            while 1:
                x, y = visited[y][x]
                #print(y, x, py, px, ' ddd')

                if x == attacker_x and y == attacker_y:
                    return True

                board[y][x] = max(0, board[y][x]- board[attacker_y][attacker_x] // 2)
                fset.add((x, y))
                #print(board)

        for i in range(4):
            nx = (x + dx[i]) % M
            ny = (y + dy[i]) % N

            if board[ny][nx] > 0 and len(visited[ny][nx]) == 0:
                queue.append((nx, ny))
                visited[ny][nx] = (x,y)
    
    return False

for k in range(K):
    
    search = return_search(board, attack)

    if len(search) <= 1:
        break

    search = sorted(search, key=lambda x: (x[0], -x[1], -x[2], -x[3]))

    # 공격자 선정 
    attacker_x, attacker_y = search[0][3], search[0][4]
    attacker_lv = search[0][0] + handi
    board[attacker_y][attacker_x] = attacker_lv
    attack[attacker_y][attacker_x] = k + 1

    # 타켓 선정 

    target_x, target_y = search[len(search)-1][3], search[len(search)-1][4]
    target_lv = search[len(search)-1][0]

    #print(attacker_x, attacker_y, attacker_lv, target_x, target_y, target_lv)
    
    # 레이저 공격
    # 최단 거리 찾기 - BFS, 경로 저장 
    fset = set()
    fset.add((attacker_x, attacker_y))
    fset.add((target_x, target_y))
    if bfs(attacker_x, attacker_y, target_x, target_y) == False:
        # 포탄
        board[target_y][target_x] = max(0, board[target_y][target_x] - board[attacker_y][attacker_x])
        #print(board)
        for i in range(-1, 2, 1):
            for j in range(-1, 2, 1):
                if (i ==0 and j ==0):
                    continue 

                y = (target_y+i) % N
                x = (target_x+j) % M

                if (y == attacker_y and x == attacker_x):
                    continue
                
                board[y][x] = max(0, board[y][x] - board[attacker_y][attacker_x] //2)
                fset.add((x, y))


    # 정비 
    for i in range(N):
        for j in range(M):
            if (j, i) not in fset and board[i][j] > 0:
                board[i][j] += 1
    
    #print(board)


print(max(map(max, board)))