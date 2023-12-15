import Modal from '@mui/material/Modal'
import { useState, useEffect, useLayoutEffect, useReducer } from 'react'
import { useRouter } from 'next/navigation';
import { POST } from '@/app/requests';

const CLICK_POINT_RADIUS = 20; // 圆点直径
const CLICK_POINT_THRESHOLD = 50; // 点击点的误差阈值
const IMG_NUM = 8; // 图片数量
const VERIFY_LIMIT = 30; // 最多验证次数

const clickPointsReducer = (state, action) => {
  switch (action.type) {
    case 'ADD_CLICK_POINT':
      return [
        ...state,
        {
          x: action.payload.x,
          y: action.payload.y,
          id: action.payload.x
        }
      ];
    case 'REMOVE_CLICK_POINT':
      return state.filter(point => point.id !== action.payload.id);
    case 'REMOVE_ALL_CLICK_POINTS':
      return [];
    default:
      throw new Error(`unhandled action type: ${action.type}`)
  }
}

const ClickPoint = ({ x, y, id, onClick }) => {
  return (
    <div
      key={id}
      style={{
        position: 'absolute',
        top: y - CLICK_POINT_RADIUS / 2,
        left: x - CLICK_POINT_RADIUS / 2,
        width: CLICK_POINT_RADIUS,
        height: CLICK_POINT_RADIUS,
        borderRadius: CLICK_POINT_RADIUS / 2,
        backgroundColor: 'red',
        cursor: 'pointer',
      }}
      onClick={onClick}
    >
    </div>
  )
}

const handleClick = (event, dispatch) => {
  const { clientX, clientY } = event;
  const parentRect = event.target.getBoundingClientRect();
  const res = {
    x: clientX - parentRect.left,
    y: clientY - parentRect.top,
  };
  // 添加点击点
  dispatch({ type: 'ADD_CLICK_POINT', payload: res });
}

const VerifyModal = ({ ifOpen, setModalOpen, setPass }) => {
  const [clickPoints, dispatch] = useReducer(clickPointsReducer, []);
  const [imgcaptchaAnswer, setImgcaptchaAnswer] = useState(null);
  const [randomIndex, setRandomIndex] = useState(null);
  //const IMG_URL = `/lib/images/${randomIndex}.png`;
  //const WAV_URL = `/lib/wavs/${randomIndex}.wav`;
  const IMG_URL = `/output/overlay_output/${randomIndex}.png`;
  const WAV_URL = `/output/voice_output/${randomIndex}.wav`;

  const router = useRouter();

  /**
   * TODO
   * 服务端动态生成图片 & 语音太慢了!
   * 1. 考虑优化服务端生成程序
   * 2. 前端进入页面就请求服务端,服务端同步开始生成
   */
  useLayoutEffect(() => {
    (async() => {
      const tmp = new Date().getTime();
      let verifyCount = localStorage.getItem('verifyCount') || localStorage.setItem('verifyCount', 0);
      console.log('verifyCount', verifyCount)
      if(verifyCount >= VERIFY_LIMIT) {
        router.push('/forbidden');
      }
  
      await POST('/api/generateVoiceAndImage',{
        filename: tmp
      })

      setRandomIndex(tmp);

      fetch(`/output/char_output/${tmp}.json`).then(res => res.json()).then(res => {
        setImgcaptchaAnswer(res);
        console.log('imgcaptchaAnswer', res)
      });
    })()
  }, [ifOpen])

  useEffect(() => {
    if (clickPoints.length === 4) {
      handleVerify()
    }
  }, [clickPoints])

  const onClose = () => {
    dispatch({ type: 'REMOVE_ALL_CLICK_POINTS' })
    setModalOpen(false)
  }

  const handleVerify = async () => {
    const pos = imgcaptchaAnswer.answer;
    console.log('clickPoints', clickPoints)
    console.log('pos', pos)

    // 判断四个点是否与预设的点相近
    for (let i = 0; i < pos.length; i++) {
      if (Math.abs(pos[i].x - clickPoints[i].x) > CLICK_POINT_THRESHOLD || Math.abs(pos[i].y - clickPoints[i].y) > CLICK_POINT_THRESHOLD) {
        console.log('incorrect key', i)
        console.log('x diff', Math.abs(pos[i].x - clickPoints[i].x))
        console.log('y diff', Math.abs(pos[i].y - clickPoints[i].y))
        localStorage.setItem('verifyCount', parseInt(localStorage.getItem('verifyCount')) + 1);
        alert('验证失败');
        setPass(false);
        onClose();
        dispatch({ type: 'REMOVE_ALL_CLICK_POINTS' })
        return null;
      }
    }
    alert('验证成功')
    onClose();
    setPass(true);
    dispatch({ type: 'REMOVE_ALL_CLICK_POINTS' })
  }

  return (
    <Modal
      onClose={onClose}
      open={ifOpen}>
      <div className="modal flex flex-col space-y-3">
        <div className='text-xl font-bold'>验证你的身份</div>
        <div className='text-sm'> 按顺序点击你听到的词语 </div>
        <div
          onClick={(e) => {
            handleClick(e, dispatch)
          }}
          style={{ backgroundImage: `url(${IMG_URL})` }} className='w-80 h-80 bg-contain relative'>
          {
            clickPoints.map(point => {
              return (
                <ClickPoint
                  key={point.id}
                  x={point.x}
                  y={point.y}
                  id={point.id}
                  onClick={(e) => {
                    dispatch({
                      type: 'REMOVE_CLICK_POINT',
                      payload: {
                        id: point.id
                      }
                    })
                    e.stopPropagation();
                  }}
                />
              )
            })
          }
        </div>
        <audio src={WAV_URL} controls></audio>
      </div>
    </Modal>
  )
}

export default VerifyModal