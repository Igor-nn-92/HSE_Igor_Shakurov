def is_monotonic(nums):
    if len(nums) <= 2:
        return True
    is_increasing = True
    is_decreasing = True

    for i in range(1, len(nums)):
        if nums[i] < nums[i - 1]:
            is_increasing = False
        if nums[i] > nums[i - 1]:
            is_decreasing = False
    if is_increasing or is_decreasing:
        return True
    return False
l=list (map(int,input().split()))
print (is_monotonic(l))
