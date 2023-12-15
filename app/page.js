'use client'
import Button from '@mui/material/Button';
import { useRouter } from 'next/navigation'
import { useEffect,useState } from 'react';
import { POST } from './requests';
import { collectBrowserEnv } from '@/utils/collectBrowserEnv'

export default function Home() {
  const router = useRouter();
  const [browserEnv, setBrowserEnv] = useState(null)

  useEffect(() => {
    setBrowserEnv(collectBrowserEnv())
  },[])
  
  return (
    <div className='min-h-screen w-full flex justify-center items-center'>
      <Button 
      onClick={() => {
        POST('/api/judgeBrowserEnv',{
          browserEnv: browserEnv
        }).then(res => {
          if(res.code === 403) {
            router.push('/verify')
          } else if(res.code === 200) {
            router.push('/pass')
          }
        })
      }}
      variant="outlined">登录</Button>
    </div>
  )
}