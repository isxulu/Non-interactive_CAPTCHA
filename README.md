#### Non-interactive_CAPTCHA

> This graduation project covers three different types of CAPTCHAs, including browser fingerprint verification, mouse trajectory verification, and interactive audio-visual verification. The first browser fingerprint verification does not require any user interaction; it collects various attribute information from the user's device and browser to generate a unique fingerprint identifier for identity verification. The second verification uses a click-based unobtrusive verification technology based on mouse trajectories, collecting and analyzing user mouse movement information on the page, including speed, direction, and acceleration, requiring only a mouse click for verification. These two verifications provide sufficient convenience for both regular users and special populations. If the first two verifications fail or are ambiguous, the final image + voice audio-visual CAPTCHA verification is provided, with all three verifications working together to ensure security.

### 运行

1. git clone
2. npm install
3. npm run dev

![20230412140709](https://typora-1309407228.cos.ap-shanghai.myqcloud.com/20230412140709.png)

### 运行逻辑

1. 用户移动鼠标到checkbox,点击checkbox
2. 后端根据以下数据判断访问用户风险等级
   1. 浏览器指纹
   2. 鼠标轨迹
3. 如果判断为有风险,弹出图片&语音验证码的modal,如果没有风险,直接通过

### 更新日志

3.25
1. 鼠标轨迹&时间戳捕捉
2. 浏览器指纹生成
3. 后端逻辑代码
   1. 高频请求ban
   2. 执行本地python模型

4.12
1. 接上了后端python模型
2. 美化了验证码样式

4.21
1. 增加了点击图片验证码

4.22
1. 完善了判断逻辑

4.24
1. 增加了浏览器环境风险因素检测
   1. webgl 浏览器类型 & user agent浏览器类型 & platform浏览器类型
   2. webdriver
   3. plugins

4.25
1. 增加了对于接收到的风险因素的综合判断

### TODO

1. 自定义浏览器指纹
2. ~~接入后端python模型~~
3. ~~图片&语音验证码~~
   1. ~~细化完善~~
4. ~~**根据浏览器环境判断访问风险**~~
5. ~~后端模型似乎还有一点问题(基本上都是pass)~~
6. ~~完善判断逻辑~~
7. ~~根据获得的风险因素,判断访问者的风险~~
8. 识别准确率的测试
   1. 测试从LSTM -> XGBoost -> 数据增广后的XGBoost的识别准确率的变化(鼠标轨迹部分)
   2. 测试图片语音验证码的识别准确率

### 踩坑记录

1. js里对于对象的遍历不是顺序的
2. 事件冒泡问题
3. 记得给每个element加key
4. 使用useReducer代替useState
5. 对于一些response可以考虑常量硬编码
   1. 硬编码的时候注意作用域！！！
   2. nextResponse声明在最顶层后，多次请求api会造成readable stream lock的错误，推测是由于每次请求返回的都是相同的nextResponse导致的
