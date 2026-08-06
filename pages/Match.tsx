import React from 'react'

function scoreTags(a:string[], b:string[]) {
  const setA = new Set(a.map(x=>x.toLowerCase()))
  const setB = new Set(b.map(x=>x.toLowerCase()))
  const inter = [...setA].filter(x=>setB.has(x)).length
  const union = new Set([...setA, ...setB]).size || 1
  return inter / union
}

export default function Match({ users, currentUserId }: any) {
  const me = users.find((u:any)=>u.id===currentUserId)
  const others = users.filter((u:any)=>u.id!==currentUserId)
  const ranked = others.map((o:any)=>({ ...o, score: scoreTags(me.tags, o.tags) })).sort((a:any,b:any)=>b.score-a.score)
  return (
    <div className="card">
      <h2>基于标签的匹配</h2>
      <p>按照 Jaccard 相似度排序，展示最接近的用户。</p>
      <div style={{marginTop:12}}>
        {ranked.map((r:any)=>(
          <div key={r.id} className="card" style={{marginBottom:10}}>
            <div className="user-row">
              <div className="thumb">{r.name[0]}</div>
              <div style={{flex:1}}>
                <div><strong>{r.name}</strong> <span style={{color:'#666',marginLeft:8}}>score: {r.score.toFixed(2)}</span></div>
                <div style={{marginTop:6}}>{r.bio}</div>
                <div style={{marginTop:6}}>
                  {r.tags.map((t:string,i:number)=><span key={i} className="tag">{t}</span>)}
                </div>
              </div>
              <div>
                <button className="button" onClick={()=>alert('已发起匹配请求（模拟）')}>配对</button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
