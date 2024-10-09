# 색깔 트리, 각 노드는 특정 색깔, 최대 깊이 속성 존재
# 명령을 통해 동적으로 노드 추가, 색깔 변경 처리
# 빨강 1, 주황 2, 노랑 3, 초록 4, 파랑 5

# (1) 노드 추가
## 고유 번호 m, 부모 노드 번호 p, 색깔 c, 최대 깊이 dep
## p = -1이면 새로운 트리의 루트 노드가 됨
## dep는 해당 노드를 루트로 하는 서브트리의 최대 깊이 
## 따라서, 기존 노드의 dep에 따라 모순 발생시 노드 추가 취소
# (2) 색깔 변경
## 특정 노드 m를 루트로 하는 서브트리의 모든 노드 색깔을 지정 색으로 변경
# (3) 색깔 조회 - 특정 노드 m
# (4) 점수 조회 - 모든 노드의 가치 제곱 더하기
## 가치는 서브 노드의 색깔 다양성

import sys
from collections import deque

Q = int(input())
orders = [list(map(int, sys.stdin.readline().split())) for _ in range(Q)]

# 딕셔너리로 이어진 노드 표현
# [자신의 ID] = 부모 노드 ID, 컬러, 최대 깊이, 자식 노드 ID 순으로 추가
tree = {}
for order in orders:
    order_type = order[0]
    if order_type == 100: # 노드 추가
        m_id, p_id, color, max_depth = order[1:]
        if p_id == -1: 
            tree[m_id] = [p_id, color, max_depth]
        else:
            cur_depth = 1
            next_p_id = p_id
            poss = True
            while 1:
                if cur_depth < tree[next_p_id][2]:
                    cur_depth += 1
                    next_p_id = tree[next_p_id][0]
                else:
                    poss = False
                    break
                
                if next_p_id == -1:
                    break
                
            if poss:
                tree[m_id] = [p_id, color, max_depth]
                tree[p_id].append(m_id)
        #print(tree)
    elif order_type == 200: # 색깔 변경
        m_id, color = order[1:]
        change_list = [m_id]
        queue = deque([m_id])
        while queue:
            v = queue.popleft()

            for i in range(3, len(tree[v])):
                queue.append(tree[v][i])
                change_list.append(tree[v][i])
        for change in change_list:
            tree[change][1] = color

    elif order_type == 300: # 색깔 조회
        m_id = order[1]
        print(tree[m_id][1])

    elif order_type == 400: # 점수조회
        color_count= {}
        whole = 0
        for node in reversed(tree.keys()):
            if node not in color_count:
                color_count[node] = set()
            color_count[node].add(tree[node][1])
            
            parent = tree[node][0]
            if parent != -1:
                if parent not in color_count:
                    color_count[parent] = set()
                color_count[parent].update(color_count[node])

        for node in tree:
            whole += len(color_count[node])**2
        print(whole)