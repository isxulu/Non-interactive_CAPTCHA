const browserEnv = {}

/**
 * 获取浏览器类型
 */
const getPlatform = () => {
  if (navigator.platform) {
    browserEnv.platform = navigator.platform;
  } else {
    browserEnv.platform = null;
  }
}

/**
 * 获取浏览器是否支持webdriver
 */
const getWebdriver = () => {
  if (navigator.webdriver) {
    browserEnv.webdriver = navigator.webdriver;
  } else {
    browserEnv.webdriver = null;
  }
}

/**
 * 获取插件信息
 */
const getPluginInfo = () => {
  let plugins = [];
  for (let i = 0; i < navigator.plugins.length; i++) {
    plugins.push(navigator.plugins[i].name);
  }
  browserEnv.plugins = plugins;
}

/**
 * 获取webgl渲染下的浏览器类型
 */
const getUserBrowserType = () => {
  // 创建一个 Canvas 元素
  var canvas = document.createElement('canvas');

  // 获取 WebGL 上下文
  var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

  // 获取 WebGL 调试信息扩展
  var debugInfo = gl.getExtension('WEBGL_debug_renderer_info');

  // 获取浏览器的渲染器信息
  var renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);

  // 根据渲染器信息来判断浏览器类型
  if (renderer.indexOf('Intel') >= 0 || renderer.indexOf('NVIDIA') >= 0 || renderer.indexOf('AMD') >= 0) {
    browserEnv.webglBrowserType = 'Chrome';
  } else if (renderer.indexOf('NVIDIA') >= 0 || renderer.indexOf('ATI') >= 0) {
    browserEnv.webglBrowserType = 'Firefox';
  } else if (renderer.indexOf('Apple') >= 0) {
    browserEnv.webglBrowserType = 'Safari';
  } else if (renderer.indexOf('Direct3D') >= 0 || renderer.indexOf('Microsoft') >= 0) {
    browserEnv.webglBrowserType = 'IE';
  } else {
    browserEnv.webglBrowserType = 'Unknown';
  }
}

/**
 * 获取 navigator.userAgent
 */
const getNavigatorUserAgent = () => {
    browserEnv.navigatorUserAgent = navigator.userAgent;
}

/**
* 收集浏览器环境信息
*/
export const collectBrowserEnv = () => {
    getUserBrowserType();
    getNavigatorUserAgent();
    getPluginInfo();
    getWebdriver();
    getPlatform();

    return browserEnv;
}