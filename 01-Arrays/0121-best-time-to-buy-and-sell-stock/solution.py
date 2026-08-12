class Solution(object):
    def maxProfit(self, prices):
        min_price=[0]
        max_price = 0
        for price in prices:
            if price <min_price:
                min_price = price
            profit = price-min_price
            if profit>max_price:
                max_price = profit
        return max_price

        