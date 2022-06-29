# Auto_JsFinder


## 0x01：Introduce

对Threezh1师傅的https://github.com/Threezh1/JSFinder，进行了一定的修改


去除了深度爬取和寻找domain的功能，只保留了爬取js接口的功能，并添加了自动请求并打印body。因为在实际使用过程中，往往是爬取到接口在放到txt中利用bp的Intruder去跑，觉得太过于繁琐，于是就修改了一下代码

## 0x02：Use

首先输入需要爬取的js接口

![image](https://user-images.githubusercontent.com/48739932/176452416-960098e4-d82a-4df4-9a0a-2d2a481ae336.png)

mac用户可以添加快捷命令：alias JsFind="python3 /Users/Str1am/JSFinder-master/jsFinder_new.py"

会爬取接口并请求和打印body

![image](https://user-images.githubusercontent.com/48739932/176452825-6b7f1c07-8c1e-4e02-a30e-b7122aa8771d.png)

这里出现了一种常见情况，host+path并不是网站的请求接口，所以没有返回任何body

所以添加了一个自定义接口功能，输入网站的api接口

![image](https://user-images.githubusercontent.com/48739932/176453017-fb2c73c4-c6da-486c-a09c-44a1b106b7dc.png)

根据返回包接口就可以方便的测试越权了

## Notice

代码中过滤了返回head为text/html的数据，防止出现返回body过于冗长影响判断，所以可能或遗漏部分接口


