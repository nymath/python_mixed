# -*- coding: utf-8 -*-
'''
函数代码请只在 "
##########start 下面可以改动

##########end 上面可以改动 "

中间部分作答，作答行数自由调整


给你一个整数数组 nums 和一个整数 k ，请你返回其中出现频率前 k 高的元素。你可以按 任意顺序 返回答案。

 

示例 1:

输入: nums = [1,1,1,2,2,3], k = 2
输出: [1,2]
示例 2:

输入: nums = [1], k = 1
输出: [1]
 

提示：

1 <= nums.length <= 105
k 的取值范围是 [1, 数组中不相同的元素的个数]
题目数据保证答案唯一，换句话说，数组中前 k 个高频元素的集合是唯一的

  　
'''



def TEST_DO_NOT_CHANGE(lst_nums,k):
    lst_rlt=[]
    print(lst_nums,k)
    ##########start 下面可以改动
    num_lst = list(map(lambda x:lst_nums.count(x),lst_nums))
    
    colc = {}
    for key,value in zip(lst_nums,num_lst):
        colc[key] = value
    l1 = list(colc.keys())
    l1.sort(key=lambda x:colc[x],reverse=True)
    lst_rlt = l1[0:k]
    ##########end 上面可以改动 "  
    return lst_rlt

    
if __name__ == "__main__":
    print (TEST_DO_NOT_CHANGE([1,1,1,2,2,3],2))
    #######下面可以添加测试语句
    
