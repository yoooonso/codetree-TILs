# 탐사 순서, 언제나 5x5 격자 유적지
# 1. 3x3 격자 선택 - 회전 무조건 진행 (중심 좌표 기준), 90도, 180도, 270도
    # 3개의 회전 방식 중 유물 획득 가치 최대화 방법 선택
    # 가치 동일한 경우, 회전 각도가 가장 작은 방법
    # 회전 각도도 같다면 중심 좌표 의 열이 가장 작은, 행이 가장 작은

# 2. 유물 획득 - 유물의 가치: 모인 조각의 개수
    # 발견된 유물 제거
    # 유적의 벽면에는 유물이 제거될 때, 생겨나는 조각에 대한 정보가 담김
    # 새로운 조각: 열 번호가 작은 순, 행 번호가 큰 순으로 조각 생김
    # 새로운 조각 채운 후
        # 유물 연쇄 획득 가능 - 계속 반복

# 3. 새로운 턴으로, 각 턴 마다 유물의 가치 총합 출력 필요

import sys
import copy
from collections import deque

K, M = map(int, sys.stdin.readline().split())
board = [list(map(int, sys.stdin.readline().split())) for _ in range(5)]
pieces = list(map(int, sys.stdin.readline().split()))

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

pieces_i = 0

def find_value(board):
    visited = [[False] * 5 for _ in range(5)]
    value = 0
    puzzles = []
    
    for i in range(5):
        for j in range(5):
            puzzle = []
            cur = board[i][j]
            if not visited[i][j]:
                queue = deque([(i, j)])
                visited[i][j] = True
                puzzle.append((i, j))
                cnt = 1
                while queue:
                    y, x = queue.popleft()
                    for k in range(4):
                        ny = y + dy[k]
                        nx = x + dx[k]
                        if 0 <= ny < 5 and 0<= nx <5 \
                        and board[ny][nx] == cur and visited[ny][nx] == False:
                            queue.append((ny, nx))
                            visited[ny][nx] = True
                            puzzle.append((ny, nx))
                            cnt += 1
                if cnt >= 3:
                    value += cnt
                    puzzles += puzzle

    return value, puzzles

for i in range(1, K+1): # K번의 턴 반복
    # 중심 좌표 선택 & 경우의 수 비교
    compare_list = []
    best_value = 0
    total_value = 0
    for c in range(1,4): # 열 행 순 이므로
        for r in range(1,4): # 1, 2, 3 가능
            new_board = copy.deepcopy(board)
            board_3x3 = [row[c-1:c+2] for row in board[r-1:r+2]]
            new_small_board = copy.deepcopy(board_3x3)

            # 회전 90 & 유물 가치 구함 & 저장 순서 - 유물 획득 가치, 회전 각도, 열, 행 순
            for sr in range(3):
                for sc in range(3):
                    new_board[sc + (r-1)][2-sr + (c-1)] = new_small_board[sr][sc]
            value, puzzles = find_value(new_board)
            if value > best_value:
                best_value = value
                best_puzzles = puzzles 
                best_board = copy.deepcopy(new_board)

            # 회전 180 & 유물 가치 구함 & 저장 순서 - 유물 획득 가치, 회전 각도, 열, 행 순
            for sr in range(3):
                for sc in range(3):
                    new_board[2-sc + (r-1)][2-sr + (c-1)] = new_small_board[sr][sc]
            value, puzzles = find_value(new_board)
            if value > best_value:
                best_value = value
                best_puzzles = puzzles 
                best_board = copy.deepcopy(new_board)

            # 회전 270 & 유물 가치 구함 & 저장 순서 - 유물 획득 가치, 회전 각도, 열, 행 순
            for sr in range(3):
                for sc in range(3):
                    new_board[2-sc + (r-1)][sr + (c-1)] = new_small_board[sr][sc]
            value, puzzles = find_value(new_board)
            if value > best_value:
                best_value = value
                best_puzzles = puzzles 
                best_board = copy.deepcopy(new_board)

    if best_value == 0: # 아예 끝내기 
        break
    
    # 유물 제거 교체 작업 시작 - puzzles 기준 
    total_value += best_value
    while 1:
        puzzles = sorted(best_puzzles, key = lambda x: [x[1], -x[0]])

        for puzz in puzzles:
            best_board[puzz[0]][puzz[1]] = pieces[pieces_i]
            pieces_i += 1

        value, best_puzzles = find_value(best_board)
        total_value += value
        if value == 0:
            break
    # 출력 
    print(total_value)
    board = copy.deepcopy(best_board)