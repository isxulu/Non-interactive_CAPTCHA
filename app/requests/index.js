export const POST = (url,payload) => {
    return new Promise((resolve,reject) => {
        fetch(url,{
            method:'POST',
            headers:{
                'Content-Type':'application/json'
            },
            body:JSON.stringify(payload)
        }).then(res => res.json()).then(res => {
            resolve(res)
        }).catch(err => {
            reject(err)
        })
    })
}