class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k%=n
        l,r =0,n-1
        while l<r:
            nums[l],nums[r] = nums[r],nums[l]
            l+=1
            r-=1
        l,r = 0,k-1
        while l<r:
            nums[l],nums[r] = nums[r],nums[l]
            l+=1
            r-=1
        l,r = k,n-1
        while l<r:
            nums[l],nums[r] = nums[r],nums[l]
            l+=1
            r-=1