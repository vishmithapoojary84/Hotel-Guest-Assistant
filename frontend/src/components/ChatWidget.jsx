import { useState, useRef, useEffect } from 'react'
import ChatHeader from './ChatHeader'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'
import { sendChatMessage } from '../services/api'

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am the Oceanview Resort virtual assistant. How can I help you today?' }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    if (isOpen) {
      scrollToBottom()
    }
  }, [messages, isOpen])

  const handleSend = async (text) => {
    const userMessage = { role: 'user', content: text }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      const history = messages.filter(m => m.role !== 'system')
      const data = await sendChatMessage(text, history)
      setMessages(prev => [...prev, { role: 'assistant', content: data.reply }])
    } catch (err) {
      console.error(err)
      setMessages(prev => [...prev, { role: 'assistant', content: "⚠️ Sorry, an error occurred while connecting to the backend. Please ensure the backend is running." }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="chat-widget-container">
      {isOpen && (
        <div className="chat-container floating">
          <div className="chat-header-flex">
             <ChatHeader />
             <button className="close-btn" onClick={() => setIsOpen(false)} aria-label="Close Chat">
               ✖️
             </button>
          </div>
          
          <div className="messages-area">
            {messages.map((msg, idx) => (
              <ChatMessage key={idx} message={msg} />
            ))}
            {isLoading && (
              <div className="message-wrapper assistant">
                <div className="message-bubble loading">
                  <span className="dot"></span>
                  <span className="dot"></span>
                  <span className="dot"></span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <ChatInput onSend={handleSend} isLoading={isLoading} />
        </div>
      )}

      <button 
        className={`chat-toggle-btn ${isOpen ? 'hidden' : ''}`}
        onClick={() => setIsOpen(true)}
      >
        💬 Ask Us Anything
      </button>
    </div>
  )
}
