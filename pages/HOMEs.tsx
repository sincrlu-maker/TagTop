import React from 'react'

export default function Home({ users }: any) {
  return (
    <div className="card">
      <h2>示例用户</h2>
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(220px,1fr))',gap:12,marginTop:12}}>
        {users.map((u:any)=>
          <div key={u.id} className="card">
            <div className="user-row">
              <div className="thumb">{u.name[0]}</div>
              <div>
                <div><strong>{u.name}</strong></div>
                <div style={{marginTop:6}}>{u.bio}</div>
                <div style={{marginTop:6}}>
                  {u.tags.map((t:string,i:number)=><span key={i} className="tag">{t}</span>)}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
