import { NextResponse } from 'next/server';
import UAParser from 'ua-parser-js';

export async function POST(request,response) {

    const BROWSER_ENV_PASS = NextResponse.json({
        message:'browser environment captcha pass',
        code:200
    });
    
    const BROWSER_ENV_REMAIN_VERIFY = NextResponse.json({
        message:'browser environment captcha remain verify',
        code:403
    });
    
    const getUserAgent = (request) => {
        const parser = new UAParser();
        const userAgent = request.headers.get('user-agent');
        const result = parser.setUA(userAgent).getResult();
    
        return result;
    }

    
    const res = await request.json();
    const userAgent = getUserAgent(request);

    // return BROWSER_ENV_REMAIN_VERIFY;  // !: 只是为了测试后面的两道

    // 根据浏览器环境判断是否有风险
    
    // 1. 判断webgl下检测到的浏览器类型是否与user Agent一致
    if(res.browserEnv.webglBrowserType == userAgent.browser.name)  {
        console.log(res.browserEnv.webglBrowserType + ' !== '+ userAgent.browser.name)
        return BROWSER_ENV_REMAIN_VERIFY;
    }
    
    // 2. 判断请求浏览器是否有plugins
    if(res.browserEnv.plugins.length === 0) {
        console.log('plugins length is 0')
        return BROWSER_ENV_REMAIN_VERIFY;
    }

    // 3. 判断请求浏览器的platform与user agent的os是否一致
    if(res.browserEnv.platform.slice(0,2) !== userAgent.os.name.slice(0,2)) {
        console.log(res.browserEnv.platform + ' !== '+ userAgent.os.name)
        return BROWSER_ENV_REMAIN_VERIFY;
    }
    
    return BROWSER_ENV_PASS

}