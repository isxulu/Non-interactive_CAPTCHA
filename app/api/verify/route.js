import { NextResponse } from 'next/server';
const fs = require('fs');
const exec = require('child_process').exec;

const globalHash = {};

const execCmd =  (args) => {
 return new Promise((resolve,reject) => {
    exec('python app/model/sample.py '+args,(err,stdout,stderr) => {
      console.log("stdout:",stdout)
      if(err) {
        resolve(false);
      }
      if(stdout.split('\n')[0][0] == 'p')
        resolve(true);
      else
        resolve(false);
    });
  });
}


export async function GET(request,response) {
  return NextResponse.json({
    message:'receive get'
  });
}

export async function POST(request,response) {

  const REQUEST_TOO_FASE = NextResponse.json({
    message:'request too fast',
    code:4031
  });
  
  const TRACE_PASS = NextResponse.json({
    message:'trace captcha pass',
    code:200
  });
  
  const TRACE_REMAIN_VERIFY = NextResponse.json({
    message:'trace captcha remain verify',
    code:403
  });

  const res = await request.json();
  const currTimeStamp = new Date().getTime();

  // 写入app/api/verify/verify.log
  const log = `user ${res.fingerprint} request at ${currTimeStamp}\n`;
  if(!fs.existsSync('app/api/verify/verify.log')) {
    fs.writeFileSync('app/api/verify/verify.log',log);
  } else {
    fs.appendFileSync('app/api/verify/verify.log',log);
  }

  if(!globalHash[res.fingerprint]) {
    globalHash[res.fingerprint] = currTimeStamp;
  } else {
    if(currTimeStamp - globalHash[res.fingerprint] < 100) {
      // 当来自同一个用户的请求过于频繁时
      globalHash[res.fingerprint] = currTimeStamp; // reset request timestamp
      return REQUEST_TOO_FASE
    } else {
      globalHash[res.fingerprint] = currTimeStamp; // reset request timestamp
    }
  }

  if(await execCmd(res.trace)) {
    // 执行python文件,如果通过校验，返回pass
    // console.log(res.trace);
    return TRACE_PASS
  } else {
    // 执行python文件,如果未通过校验，返回fail
    return TRACE_REMAIN_VERIFY
  }
}
