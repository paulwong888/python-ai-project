## 机制
每个agent干完活后, 生成含有hand-off的输出消息, 即下一个agent的id, 发布到群, 再由chat-manager决定调用哪个agent<br>
相当于流程是自定义, 非大模型决定