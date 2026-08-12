class Solution(object):
    def jump(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        current_end = 0
        fastened = 0
        jump = 0
        for i in range (len(nums)-1):
            fastened = max(fastened,i+nums[i])
            if i == current_end:
                jump+=1
                current_end = fastened
        return jump