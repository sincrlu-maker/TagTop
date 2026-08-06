import React, { useState } from 'react'
import Home from './pages/Home'
import Upload from './pages/Upload'
import Profile from './pages/Profile'
import Match from './pages/Match'
import dataUsers from './data/users.json'

type Page = 'home' | 'upload' | 'profile' | 'match'

export default function App() {
  const [page, setPage] = useState<Page>('home')
  const [users, setUsers] = useState(dataUsers)
  const [currentUserId] = useState(users[0].id) // demo: first user is "me"

  const updateUser = (id: string, patch: Partial<any>) => {
    setUsers((u:any[]) => u.map(x => x.id === id ? { ...x, ...patch } : x))
  }

  return (
    <div className="app">
      <div className="header">
        <h1>细分 — 标签配对 Demo</h1>
        <div style={{marginLeft:'auto'}}>当前演示用户: <strong>{users.find(u=>u.id===currentUserId)?.name}</strong></div>
      </div>

      <div className="nav">
        <button className="button" onClick={() => setPage('home')}>首页</button>
        <button className="button" onClick={() => setPage('upload')}>上传视频（模拟）</button>
        <button className="button" onClick={() => setPage('profile')}>我的资料</button>
        <button className="button" onClick={() => setPage('match')}>标签配对</button>
      </div>

      <div style={{marginTop:18}}>
        {page === 'home' && <Home users={users} />}
        {page === 'upload' && <Upload onNewTags={(tags)=> updateUser(currentUserId, { tags })} />}
        {page === 'profile' && <Profile user={users.find(u=>u.id===currentUserId)!} onSave={(patch)=> updateUser(currentUserId, patch)} />}
        {page === 'match' && <Match users={users} currentUserId={currentUserId} />}
      </div>
    </div>
  )
}
