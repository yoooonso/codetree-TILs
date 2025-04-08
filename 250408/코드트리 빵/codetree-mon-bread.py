# 빵사기 위해 편의점 이동 - NxN 격자에서
# m명의 사람이 각자 m분에 이동하기 시작 
# 1분 동안 3가지 행동 
    # 1. 격자에 있는 사람들은 편의점 방향을 향해 1칸 전진 (최단 거리로, 우선순위 상좌우하)
    # 2. 편의점 도착시 멈추고, 이때부터 다른 사람들 지날 수 없음
    # 3. t<=m의 t분이면, t 사람은 가고 싶은 편의점과 가장 가까이 있는 베이스 캠프로 (행이 작은, 열이 작은)
        # 베이스캠프는 다른 사람들이 지나갈 수 없음 

import sys
from collections import deque
input = sys.stdin.readline
n, m = map(int, input().split())
grid = [list(map(int, input().split())) for _ in range(n)]
destinations = [list(map(int, input().split())) for _ in range(m)]
cur_positions = [(-1,-1)] * m

for i, (dest_y, dest_x) in enumerate(destinations):
    destinations[i][0] = dest_y - 1
    destinations[i][1] = dest_x - 1

dy = [-1, 0, 0, 1]
dx = [0, -1, 1, 0]
t = 1
success = 0
while True:
    # 1. 1칸 전진 
    for i, (y, x) in enumerate(cur_positions):
        if y == -1 and x == -1:
            continue

        visited = [[False]*n for _ in range(n)]
        d_list = []
        queue = deque([(y, x, d_list)])
        visited[y][x] = True
        dest_y, dest_x = destinations[i]

        while queue:
            r, c, d_l = queue.popleft()

            if r == dest_y and c == dest_x:
                d_list = d_l
                break

            for d in range(4):
                nr, nc = r + dy[d], c + dx[d]
                if 0<= nr <n and 0<= nc<n and grid[nr][nc] == 0 and visited[nr][nc]==False:
                    queue.append((nr, nc, d_l + [d]))
                    visited[nr][nc] = True

        cur_positions[i] = y + dy[d_list[0]], x + dx[d_list[0]]
    
    # 2. 이동한 곳 편의점인지 확인 + 업데이트
    for i, (y, x) in enumerate(cur_positions):
        if y == -1 and x == -1:
            continue
        dest_y, dest_x = destinations[i]
        if y == dest_y and x == dest_x:
            grid[y][x] = -1
            cur_positions[i] = (-1, -1)
            success += 1
    if success >= m:
        break
    
    # 3. t인 사람 베이스캠프 찾고, position 업데이트
    if t <= m:
        visited = [[False]*n for _ in range(n)]
        y, x = destinations[t-1]
        queue = deque([(y, x, 0)])
        visited[y][x] = True
        hubo = []
        min_depth = float('inf')

        while queue:
            r, c, depth = queue.popleft()

            if grid[r][c] == 1 and min_depth >= depth:
                hubo.append((r, c))
                min_depth = depth
            elif min_depth < depth:
                break
            
            for d in range(4):
                nr, nc = r + dy[d], c + dx[d]
                if 0<= nr <n and 0<= nc<n and grid[nr][nc] != -1 and visited[nr][nc]==False:
                    queue.append((nr, nc, depth + 1))
                    visited[nr][nc] = True
  
        hubo.sort()
        base_y, base_x = hubo[0]
        cur_positions[t-1] = (base_y, base_x)
        grid[base_y][base_x] = -1

    t += 1 

print(t)