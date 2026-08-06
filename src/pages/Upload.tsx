import React, { useState } from 'react'

function mockTagFromFilename(name: string) {
  const keywords = name.toLowerCase().split(/[^a-z0-9]+/).filter(Boolean)
  const seeds = ['摄影','烘焙','编程','舞蹈','旅行','美食','教育','健身']
  const picks = Array.from(new Set([...keywords, ...seeds])).slice(0,4)
  return picks
}

export default function Upload({ onNewTags }: any) {
  const [fileName, setFileName] = useState('')
  const [tags, setTags] = useState<string[]>([])

  const handleFile = (e:any) => {
    const f = e.target.files?.[0]
    if (!f) return
    setFileName(f.name)
    setTags(mockTagFromFilename(f.name))
  }

  return (
    <div className="card">
      <h2>上传视频（本地模拟）</h2>
      <p>选择一个本地视频文件，系统将根据文件名做模拟标签生成（示例 POC）。</p>
      <input type="file" accept="video/*" onChange={handleFile} />
      {fileName && <div style={{marginTop:12}}>
        <div>文件: <strong>{fileName}</strong></div>
        <div style={{marginTop:8}}>自动生成标签：</div>
        <div style={{marginTop:6}}>
          {tags.map((t,i)=><span key={i} className="tag">{t}</span>)}
        </div>
        <div className="controls">
          <button className="button" onClick={() => onNewTags(tags)}>保存到我的标签</button>
        </div>
      </div>}
    </div>
  )
}
