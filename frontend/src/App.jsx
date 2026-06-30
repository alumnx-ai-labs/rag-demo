import { useState } from 'react'
import FileUpload from './components/FileUpload'
import ChatWindow from './components/ChatWindow'
import './App.css'

export default function App() {
  const [files, setFiles] = useState([])

  return (
    <div className="app">
      <header className="header">
        <h1>RAG Demo</h1>
        <p>Upload documents and ask questions about them</p>
      </header>

      <div className="layout">
        <aside className="sidebar">
          <FileUpload onUpload={(name) => setFiles((prev) => [...prev, name])} />

          {files.length > 0 && (
            <div className="file-list">
              <h3>Indexed Documents</h3>
              <ul>
                {files.map((f, i) => (
                  <li key={i} title={f}>{f}</li>
                ))}
              </ul>
            </div>
          )}
        </aside>

        <main className="chat-area">
          <ChatWindow />
        </main>
      </div>
    </div>
  )
}
