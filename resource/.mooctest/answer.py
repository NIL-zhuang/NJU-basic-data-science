class Solution:
    def stoneGame(self, piles) -> bool:
        size = len(piles)
        '''
        第i堆石头，先手考虑：
        从（左边石头+剩下的他作为后手能拿到的最多的）和（右边石头+剩下的他作为后手能拿到的最多的）
        后手考虑：
        如果先手拿左边，自己作为先手能拿到的最多的
        如果先手拿右边，自己作为先手能拿到的最多的
        '''
        dic = {}
        size = len(piles)
        def helper(start,end):
            if start==end:return piles[start],0
            if (start,end) in dic:
                return dic[(start,end)][0], dic[(start,end)][1]
            l1 = piles[start]+helper(start+1,end)[1]
            l2 = piles[end]+helper(start,end-1)[1]
            if l1>l2:
                pre = l1
                post = helper(start+1,end)[0]
            else:
                pre = l2
                post = helper(start,end-1)[0]
            dic[(start,end)] = (pre,post)
            return pre,post
        pre,post = helper(0,size-1)
        return pre>post
b = input().split(',')
c= []
for i in b:
    c.append(int(i))
s = Solution()
print(s.stoneGame(c))