import copy
# [(Daily PS) 파이썬으로 구현하는 BFS와 DFS](https://cyc1am3n.github.io/2019/04/26/bfs_dfs_with_python.html)
# from collections import deque


# graph_list = {
#     'A': set(['B']),
#     'B': set(['A', 'C', 'H']),
#     'C': set(['B', 'D']),
#     'D': set(['C', 'E', 'G']),
#     'E': set(['D', 'F']),
#     'F': set(['E']),
#     'G': set(['D']),
#     'H': set(['B', 'I', 'J', 'M']),
#     'I': set(['H']),
#     'J': set(['H', 'K']),
#     'K': set(['J', 'L']),
#     'L': set(['K']),
#     'M': set(['H'])
# }

# root_node = 'A'

# # graph_list = {1: set([3, 4]),
# #               2: set([3, 4, 5]),
# #               3: set([1, 5]),
# #               4: set([1]),
# #               5: set([2, 6]),
# #               6: set([3, 5])}
# # root_node = 1



# def BFS_with_adj_list(graph, root):
#     visited = []
#     queue = deque([root])

#     while queue:
#         n = queue.popleft()
#         if n not in visited:
#             visited.append(n)
#             queue += graph[n] - set(visited)
#     return visited
  
# print(BFS_with_adj_list(graph_list, root_node))



# def DFS_with_adj_list(graph, root):
#     visited = []
#     stack = [root]

#     while stack:
#         n = stack.pop()
#         if n not in visited:
#             visited.append(n)
#             stack += graph[n] - set(visited)
#     return visited

# print(DFS_with_adj_list(graph_list, root_node))


# [파이썬으로 bfs, dfs 구현해보기](https://itholic.github.io/python-bfs-dfs/)


# graph = {
#     'A': ['B'],
#     'B': ['A', 'C', 'H'],
#     'C': ['B', 'D'],
#     'D': ['C', 'E', 'G'],
#     'E': ['D', 'F'],
#     'F': ['E'],
#     'G': ['D'],
#     'H': ['B', 'I', 'J', 'M'],
#     'I': ['H'],
#     'J': ['H', 'K'],
#     'K': ['J', 'L'],
#     'L': ['K'],
#     'M': ['H']
# }

# def bfs(graph, start_node):
#     visit = list()
#     queue = list()

#     queue.append(start_node)

#     while queue:
#         node = queue.pop(0)
#         if node not in visit:
#             visit.append(node)
#             queue.extend(graph[node])

#     return visit


# def dfs(graph, start_node):
#     visit = list()
#     stack = list()
#     path = list()

#     stack.append(start_node)

#     while stack:
#         path = copy.deepcopy(stack)
#         node = stack.pop()
#         print('stack before if: {}'.format(stack))
#         if node not in visit:
#             visit.append(node)
#             # print('STACK after if: {}'.format(stack))
#             stack.extend(graph[node])
#             path.extend(graph[node])
#             print('STACK after extend: {}'.format(stack))
#             print('PATH after extend: {}'.format(path))

#     return visit


# # print(bfs(graph, 'A'))
# print(dfs(graph, 'A'))



##-----------------------------------
# [How to trace the path in a Breadth-First Search?](https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search)
# graph is in adjacent list representation
graph = {
        '1': ['2', '3', '4'],
        '2': ['5', '6'],
        '5': ['9', '10'],
        '4': ['7', '8'],
        '7': ['11', '12']
        }

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

print bfs(graph, '1', '11')