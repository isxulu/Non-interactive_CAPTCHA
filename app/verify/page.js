'use client'
import FingerprintJS, { load } from '@fingerprintjs/fingerprintjs'
import { useState, useEffect } from 'react'
import '../style.css'
import { POST } from '../requests'
import { collectBrowserEnv } from '@/utils/collectBrowserEnv'
import dynamic from 'next/dynamic'
import { useRouter } from 'next/navigation'

const DynamicVerifyModal = dynamic(
  () => import('@/components/VerifyModal'),
  { ssr: false }
)

const ConfirmBox = ({ handleVerify,loading,pass,setLoading }) => {

  return (
    <div className='border-2 rounded-lg flex justify-between w-64 p-5 font-mono items-center bg-gray-50'>
      {
        loading ? <div className='bg-loading w-8 h-8 bg-cover animate-spin'/> : 
        <div 
        onClick={() => {
          setLoading(true);
          handleVerify();
        }}
        className='border-2 w-8 h-8 rounded-lg cursor-pointer bg-white flex justify-center items-center'>
          {
            (() => {
              if(pass) {
                return <div className='bg-pass w-4 h-4 bg-cover'/>
              } else if(pass === false) {
                return <div className='bg-fail w-4 h-4 bg-cover'/>
              }
            })()
          }
        </div>
      }
      <div>
        点击以验证
      </div>
      <a 
      href='https://github.com/biu9/srtp-web'
      className='flex flex-col justify-center items-center bg-github w-8 h-8 bg-cover cursor-pointer'>
      </a>
    </div>
  )
}

export default function Verify() {
  const trace = []
  const [modalOpen, setModalOpen] = useState(false)
  const [fingerprint, setFingerprint] = useState(null)
  const [loading, setLoading] = useState(false)
  const [pass, setPass] = useState(null)
  const [browserEnv, setBrowserEnv] = useState(null)
  const router = useRouter()

  const getTrace = (e) => {
    trace.push([e.clientX, e.clientY, e.timeStamp])
  }

  useEffect(() => {
    const getFingerprint = async () => {
      const fp = await FingerprintJS.load()
      const result = await fp.get()
      setFingerprint(result.visitorId)
    }
    getFingerprint()
    setBrowserEnv(collectBrowserEnv())
  },[])

  /**
   * 判断浏览器环境 & 鼠标轨迹是否有风险
   */
  const handleVerify = async () => {
    Promise.all([
      POST('/api/judgeBrowserEnv', {
        browserEnv:browserEnv
      }),
      POST('/api/verify',{
        fingerprint,
        trace
      })
    ]).then(res => {
      console.log('res',res)
      
      for(let i=0;i<res.length;i++) {
        if(res[i].code === 4031) {
          console.log('forbidden')
          router.push('/forbidden')
          return
        }
        if(res[i].code === 403) {
          setModalOpen(true)
          return
        }
      }
      setPass(true)
    }).finally(() => {
        setLoading(false)
    }).catch(err => {
        console.log('err',err)
    })
  }

  return (
    <div onMouseMove={(e) => getTrace(e)} className="home-bg">
      {
        modalOpen &&       
        <DynamicVerifyModal 
          ifOpen={modalOpen}
          setModalOpen={setModalOpen}
          setPass={setPass}
        />
      }

      <ConfirmBox
        handleVerify={handleVerify}
        loading={loading}
        pass={pass}
        setLoading={setLoading}
      />
    </div>
  )
}
