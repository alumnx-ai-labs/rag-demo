import { useState, useRef } from 'react'
import './FileUpload.css'

export default function FileUpload({ onUpload }) {
  const [dragging, setDragging] = useState(false)
  const [status, setStatus]     = useState(null)  // { type: 'ok'|'err', msg }
  const [loading, setLoading]   = useState(false)
  const inputRef = useRef()

  async function upload(file) {
    if (!file) return
    setLoading(true)
    setStatus(null)
    const form = new FormData()
    form.append('file', file)
    try {
      const res  = await fetch('/api/upload', { method: 'POST', body: form })
      const text = await res.text()
      let data
      try { data = JSON.parse(text) } catch { data = { detail: text } }
      if (!res.ok) throw new Error(data.detail || 'Upload failed')
      setStatus({ type: 'ok', msg: `Indexed ${data.chunks} chunks from "${file.name}"` })
      onUpload(file.name)
    } catch (e) {
      setStatus({ type: 'err', msg: e.message })
    } finally {
      setLoading(false)
    }
  }

  function onDrop(e) {
    e.preventDefault()
    setDragging(false)
    upload(e.dataTransfer.files[0])
  }

  return (
    <div className="upload-section">
      <h2>Upload Document</h2>

      <div
        className={`drop-zone${dragging ? ' dragging' : ''}`}
        onClick={() => inputRef.current.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
      >
        <span className="icon">📄</span>
        <p>{loading ? 'Uploading…' : 'Drop file here or click to browse'}</p>
        <p className="hint">PDF or TXT</p>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt"
          hidden
          onChange={(e) => upload(e.target.files[0])}
        />
      </div>

      {status && (
        <p className={`status ${status.type}`}>{status.msg}</p>
      )}
    </div>
  )
}
