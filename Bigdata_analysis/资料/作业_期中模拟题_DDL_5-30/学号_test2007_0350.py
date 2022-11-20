# -*- coding: utf-8 -*-
'''
函数代码请只在 "
##########start 下面可以改动

##########end 上面可以改动 "

中间部分作答，作答行数自由调整


给你一个整数数组 nums 。数组中唯一元素是那些只出现 恰好一次 的元素。

请你返回 nums 中唯一元素的 和 。

 

示例 1：

输入：nums = [1,2,3,2]
输出：4
解释：唯一元素为 [1,3] ，和为 4 。
示例 2：

输入：nums = [1,1,1,1,1]
输出：0
解释：没有唯一元素，和为 0 。
示例 3 ：

输入：nums = [1,2,3,4,5]
输出：15
解释：唯一元素为 [1,2,3,4,5] ，和为 15 。

 　
'''



def TEST_DO_NOT_CHANGE(lst_input):
    rlt=None
    print(lst_input)
    ##########start 下面可以改动
    num_lst = list(map(lambda x:(lst_input.count(x)==1)*x,lst_input))
    rlt = 0
    for i in range(0,len(num_lst)):
        rlt += num_lst[i]
        
    ##########end 上面可以改动 "  
    return rlt

    
if __name__ == "__main__":
    print (TEST_DO_NOT_CHANGE([1,1,1,1,1]))
    #######下面可以添加测试语句
    print (TEST_DO_NOT_CHANGE([1,2,3,4,5]))
