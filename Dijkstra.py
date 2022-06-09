import concurrent.futures
from queue import PriorityQueue

class Dijkstra():
    def __init__(self, startX, startY, finishX, finishY, treasuresList, sideLen, map):
        self.startX = startX 
        self.startY = startY
        self.finishX = finishX
        self.finishY = finishY
        self.treasuresList = treasuresList
        self.sideLen = sideLen
        self.map = map

    def shortestPath(self):
        allPaths = self.permutation(self.treasuresList)
        distance = float('inf')
        futures = []
        shortestPath = []
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for path in allPaths:
                path.insert(0, (self.startX, self.startY))
                path.append((self.finishX, self.finishY))
                futures.append(executor.submit(self.getDistance, path))
            
            for future in concurrent.futures.as_completed(futures):
                steps = future.result()
                dist = len(steps)-1
                if(dist<distance):
                    distance = dist
                    shortestPath = steps

            return shortestPath
            # for x, y in shortestPath:
            #     if((x, y) not in (self.treasuresList+[(self.startX, self.startY), (self.finishX, self.finishY)])):
            #         self.draw(x, y, 'purple')

    def getNormalNeighbours(self, x, y):
        neighbours = [[x, y-1], #left
                    [x, y+1], #right
                    [x-1, y], #top
                    [x+1, y]] #bottom
        found = []
        for i in neighbours:                                                                  
            if i[0] >= 0 and i[0] < self.sideLen and i[1] >= 0 and i[1] < self.sideLen:
                if self.map[i[0]][i[1]] == 'Y':
                    found.append((i[0], i[1]))
        return found

    def getDistance(self, path):
        steps = []
        for node in zip(path[:-1], path[1:]):
            steps += self.getPath(self.dijkstra(node[0][0], node[0][1]), node[1][0], node[1][1])
        return steps

    def permutation(self, lst):
        if len(lst) == 0:
            return []
        if len(lst) == 1:
            return [lst]
        l = []
        for i in range(len(lst)):
            m = lst[i]
            remLst = lst[:i] + lst[i+1:]
            for p in self.permutation(remLst):
                l.append([m] + p)
        return l

    def dijkstra(self, beginX, beginY):
        dist = [[float('inf') for _ in range(self.sideLen)] for _ in range(self.sideLen)]
        prev = [[(-1, -1) for _ in range(self.sideLen)] for _ in range(self.sideLen)]
        dist[beginX][beginY] = 0
        q = PriorityQueue()

        for row in range(self.sideLen):
            for col in range(self.sideLen):
                q.put([dist[row][col], (row, col)])

        while not q.empty():
            u = q.get()
            for neighbour in self.getNormalNeighbours(u[1][0], u[1][1]):
                N = 1
                newLen = dist[u[1][0]][u[1][1]] + N
                if(newLen < dist[neighbour[0]][neighbour[1]]):
                    dist[neighbour[0]][neighbour[1]]  = newLen
                    prev[neighbour[0]][neighbour[1]] = (u[1][0], u[1][1])
                    nowy = [newLen, (neighbour[0], neighbour[1])]
                    q.put(nowy)
        return prev

    def getPath(self, prev, goalX, goalY):
        path = []
        s = []
        u = (goalX, goalY)
        if(prev[u[0]][u[1]] != (-1, -1) or u == (self.startX, self.startY)):
            while u != (-1, -1):
                s.insert(0, u)
                if((u[0], u[1]) not in [(goalX, goalY), (self.startX, self.startY)]):
                    path.append((u[0], u[1]))
                u = prev[u[0]][u[1]]

        return path         