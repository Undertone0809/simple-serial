<h1 align="center">
    cushy-serial
</h1>
<p align="center">
  <strong>一个轻量级的Python Serial框架</strong>
</p>

<p align="center">
    <a target="_blank" href="">
        <img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg?label=license" />
    </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/broadcast-service?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Total"/>
   </a>
    <a target="_blank" href=''>
        <img src="https://static.pepy.tech/personalized-badge/broadcast-service?period=month&units=international_system&left_color=grey&right_color=blue&left_text=Downloads/Week"/>
   </a>
</p>

# 简介
cushy-serial是一个轻量级的Serial框架，初衷是希望使Serial编程变得更加简单、快捷，因此，相较于传统的pyserial，该框架可以更加快速地构建起一个serial程序。

# 主要特性

- 兼容pyserial的所有特性
- 自定义serial消息异步回调，无需花费精力在多线程上
- 方便实现和管理多个serial连接
- 可自定义消息协议，兼容性强

# 快速上手
```bash
pip install cushy-socket --upgrade 
```

- 下面是一个简单的serial程序，当python客户端接收到来自串口的信息时会自动回调
```python
from cushy_serial import CushySerial

serial = CushySerial("COM1", 9600)
serial.send("I am python client")


@serial.on_message()
def handle_serial_message(msg: bytes):
    str_msg = msg.decode("utf-8")
    print(f"[serial] rec msg: {str_msg}")

```

> 需要说明的是，CushySerial兼容了Serial中所有的功能，因此，你可以在CushySerial中使用Serial的所有功能。

  
- 运行结果如下

<img src="https://zeeland-bucket.oss-cn-beijing.aliyuncs.com/images/20230310173226.png"/>


# 待办

- [ ] 提供bytes包解析功能，减少在包解析上所花费的工作
- [ ] 提供数据流监控，提高数据稳定性
- [ ] 提供更加细力度的数据包调控，降低丢包率
- [ ] 提供串口定时任务调度
- [ ] 完善单元测试

# 贡献
如果你想为这个项目做贡献，你可以提交pr或issue。我很高兴看到更多的人参与并优化它。
