此为《量化投资》教材第5.9节《案例：构建一个沪深300指数增强基金》所用代码所用数据与代码。
非常欢迎同学们指出代码以及教材中的问题！如有问题或建议，可以联系编者 zhaochaoyi@pku.edu.cn

此版本用于2022年秋季学期北京大学数学科学学院“量化交易”课程。
更新日期：2022年10月9日

Copyright: 孙健 吴岚 赵朝熠


此案例提供数据包括（数据来源：Wind）：
(1) 沪深300指数周数据
(2) 十年期国债收益率的日数据
(3) 沪深300指数成分股列表周频数据
(4) 沪深300指数成分股权重周频数据
(5) 沪深300指数成分股流通市值周频数据
(6) 沪深300指数成分股账面市值比周频数据
(7) 沪深300指数成分股收盘价周频数据
(8) 沪深300指数成分股交易状态周频数据

如可以使用WindPy接口，则使用WindPy版本代码即无需使用上述(3)-(8)数据。(3)-(8)数据下载的代码见“ch5 - case - Step1 - FactorCalculation - NoWind.py”第33行至101行被注释掉的部分。

该案例使用的代码包括（各代码具体功能见代码开篇注释）：
(1) ch5 - case - Step1 - FactorCalculation - NoWind.py
(1') ch5 - case - Step1 - FactorCalculation - Wind.py
(2) ch5 - case - Step2 - SingleFactorTest.py
(3) ch5 - case - Step3 - Strategy - NoWind.py
(3') ch5 - case - Step3 - Strategy - Wind.py
(4) ch5 - case - Step4 - BackTest.py
如果无法使用WindPy接口，则运行顺序为(1)(2)(3)(4)；
如果可以使用WindPy接口，则运行顺序为(1')(2)(3')(4)。

【注】运行使用WindPy与不使用WindPy两个版本所得结果略有微小不同，是因为两种方法对相同收益率股票的排序不一致，导致rankIC的计算结果不同。例如，假设ABCD这四只股票本周收益率均为0%，但流通市值有所不同，如果不使用WindPy的代码将其排序为A<B<C<D，但使用WindPy的代码将其排序为B<A<D<C，那么二者得到的rankIC就不相同。教材中展示的结果是使用WindPy的版本。
【TODO】我将在后续版本中将二者调整为一致。

编程语言为python 3。将python工作路径设置为该文件夹即可运行。