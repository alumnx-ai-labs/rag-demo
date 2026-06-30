import { useState, useRef, useEffect } from 'react'
import './ChatWindow.css'

const WELCOME = 'Hello! Upload a document in the sidebar, then ask me anything about it.'

export default function ChatWindow() {
  const [messages, setMessages] = useState([{ role: 'assistant', text: WELCOME }])
  const [input,    setInput]    = useState('')
  const [loading,  setLoading]  = useState(false)
  const bottomRef = useRef()

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  async function send() {
    const q = input.trim()
    if (!q || loading) return
    setInput('')
    setMessages((prev) => [...prev, { role: 'user', text: q }])
    setLoading(true)

    try {
      const res  = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q }),
      })
      const text = await res.text()
      let data
      try { data = JSON.parse(text) } catch { data = { answer: text } }
      if (!res.ok) throw new Error(data.detail || 'Query failed')
      setMessages((prev) => [...prev, { role: 'assistant', text: data.answer }])
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', text: 'Error: could not reach the server.' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <div className="bubble">{m.text}</div>
          </div>
        ))}
        {loading && (
          <div className="msg assistant">
            <div className="bubble thinking">Thinking…</div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <div className="input-bar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && send()}
          placeholder="Ask a question about your documents…"
          disabled={loading}
        />
        <button onClick={send} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  )
}
