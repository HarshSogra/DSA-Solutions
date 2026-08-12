class Solution(object):
    def digitFrequencyScore(self, n):
        """
        :type n: int
        :rtype: int
        """
        score =0
        while n>0:
            score += n%10
            n = n//10
        return score