# scanWebFinger
简单的web指纹扫描识别，目前规则很少。
-
###json文件存放匹配规则  

```基本名称,扫描路径,[状态匹配|文本包含],权重值```
_Tips:规则文件print就是文本包含中含有想要数据的信息,例如版本号,等其他敏感信息._

###依赖库:  
```
pip3 install requests
pip3 install argparse
pip3 install tqdm
```