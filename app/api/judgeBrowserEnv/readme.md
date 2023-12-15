## 浏览器环境风险判断

### 服务端接收到的sample

```
judgeBrowserEnv {
  test: 'test data for judge browser environment',
  browserEnv: {
    webglBrowserType: 'Chrome',
    navigatorUserAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    plugins: [
      'PDF Viewer',
      'Chrome PDF Viewer',
      'Chromium PDF Viewer',
      'Microsoft Edge PDF Viewer',
      'WebKit built-in PDF'
    ],
    webdriver: null,
    platform: 'Win32'
  }
}
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
userAgent {
  ua: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',        
  browser: { name: 'Chrome', version: '112.0.0.0', major: '112' },
  engine: { name: 'Blink', version: '112.0.0.0' },
  os: { name: 'Windows', version: '10' },
  device: { vendor: undefined, model: undefined, type: undefined },
  cpu: { architecture: 'amd64' }
}
```

### userAgent

对比request.headers.get('user-agent')与parser.setUA(userAgent).getResult()的浏览器版本信息

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
```

```
userAgent {
  ua: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
  browser: { name: 'Chrome', version: '112.0.0.0', major: '112' },
  engine: { name: 'Blink', version: '112.0.0.0' },
  os: { name: 'Windows', version: '10' },
  device: { vendor: undefined, model: undefined, type: undefined },
  cpu: { architecture: 'amd64' }
}
```

### plugin

```
plugins: [
  'PDF Viewer',
  'Chrome PDF Viewer',
  'Chromium PDF Viewer',
  'Microsoft Edge PDF Viewer',
  'WebKit built-in PDF'
]
```

### platform

```
platform: 'Win32'
```

### webdriver