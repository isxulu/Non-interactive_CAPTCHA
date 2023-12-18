# Non-interactive_CAPTCHA

> This graduation project covers three different types of CAPTCHAs, including browser fingerprint verification, mouse trajectory verification, and interactive audio-visual verification. The first browser fingerprint verification does not require any user interaction; it collects various attribute information from the user's device and browser to generate a unique fingerprint identifier for identity verification. The second verification uses a click-based unobtrusive verification technology based on mouse trajectories, collecting and analyzing user mouse movement information on the page, including speed, direction, and acceleration, requiring only a mouse click for verification. These two verifications provide sufficient convenience for both regular users and special populations. If the first two verifications fail or are ambiguous, the final image + voice audio-visual CAPTCHA verification is provided, with all three verifications working together to ensure security.

### How to run

1. git clone
2. npm install
3. npm run dev

![20230412140709](https://typora-1309407228.cos.ap-shanghai.myqcloud.com/20230412140709.png)

### Execution logic

1. The user moves the mouse to the checkbox and clicks on it.
2. The backend determines the user's risk level of access based on the following data:
   1. Browser fingerprint
   2. Mouse trajectory
3. If a risk is detected, a modal with image and voice captcha is displayed. If no risk is detected, access is granted directly.

### Update Log

3.25
1. Capture mouse trajectory and timestamps.
2. Generate browser fingerprint.
3. Backend logic code:
   1. Ban high-frequency requests.
   2. Execute local Python model.

4.12
1. Integrated the backend Python model.
2. Enhanced the style of the captcha.

4.21
1. Added image captcha on click.

4.22
1. Improved the judgment logic.

4.24
1. Added browser environment risk factor detection:
   1. WebGL browser type.
   2. User agent browser type.
   3. Platform browser type.
   4. Webdriver.
   5. Plugins.

4.25
1. Enhanced comprehensive judgment of received risk factors.
   
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

### Pitfall records

1. Object iteration in JavaScript is not guaranteed to be in order.
2. Event bubbling issue.
3. Remember to assign a unique key to each element.
4. Consider using `useReducer` instead of `useState`.
5. For certain responses, consider hard-coding constants.
   1. Pay attention to the scope when hard-coding!
   2. Declaring `nextResponse` at the top level may cause a "readable stream lock" error when making multiple API requests, possibly due to receiving the same `nextResponse` repeatedly.
