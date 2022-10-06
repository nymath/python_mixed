# -*- coding: utf-8 -*-
'''
函数代码请只在 "
##########start 下面可以改动

##########end 上面可以改动 "

中间部分作答，作答行数自由调整

题目：判断101-200(包含101和200)之间有多少个素数，并按照从小到大保存所有素数至lst_rlt ，最后返回lst_rlt。
提示：判断素数的方法：用一个数分别去除2到sqrt(这个数)，如果能被整除，则表明此数不是素数，反之是素数。 （此方法并不惟一）　
'''


def TEST_DO_NOT_CHANGE():
    lst_rlt=[]
    ##########start下面可以改动
    def is_prime(n):
        rlt = True
        for i in range(2,int(n**(0.5)+1)):
            if n %i ==0:
                rlt = False
        return rlt*1
    for i in range(101,201):
        if is_prime(i) != 0:
            lst_rlt.append(int(is_prime(i)*i))

    ##########end 上面可以改动 "  
    return lst_rlt

    
if __name__ == "__main__":
    print (TEST_DO_NOT_CHANGE())
    #######下面可以添加测试语句
    
