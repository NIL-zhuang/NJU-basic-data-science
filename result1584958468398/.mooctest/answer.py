class Solution:
    def surfaceArea(self, grid) -> int:
        s = sum(sum([4*i+2 for i in m if i != 0]) for m in grid)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if j != len(grid[0])-1:
                    s -= min(grid[i][j], grid[i][j+1])*2
                if i != len(grid)-1:
                    s -= min(grid[i][j], grid[i+1][j])*2
        return s
num = int(input().strip())
n = []
for i in range(num):
    b = input().split(',')
    c = []
    for i in b:
        c.append(int(i))
    n.append(c)
s = Solution()
print(s.surfaceArea(n))
