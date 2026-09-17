import { useState, useRef, useEffect } from 'react'
import ChatHeader from './components/ChatHeader'
import ChatMessage from './components/ChatMessage'
import ChatInput from './components/ChatInput'
import { sendChatMessage } from './services/api'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am the Oceanview Resort virtual assistant. How can I help you today?' }
  ])
  const [isLoading, setIsLoading] = useState(false)
  const [isChatOpen, setIsChatOpen] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isChatOpen])

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
    <div className="hotel-website">
      {/* Navigation Bar */}
      <nav className="navbar">
        <div className="nav-brand">Oceanview Resort</div>
        <button className="book-now-btn" onClick={() => setIsChatOpen(true)}>Book Now</button>
      </nav>

      {/* Hero Section */}
      <main className="hero-section">
        <div className="hero-content">
          <h1>Experience Ultimate Luxury</h1>
          <p>Discover paradise at Oceanview Resort. Breathtaking views, world-class amenities, and unforgettable memories await.</p>
          <button className="cta-btn" onClick={() => setIsChatOpen(true)}>Explore with AI Assistant</button>
        </div>
      </main>

      {/* Floating Chat Button */}
      {!isChatOpen && (
        <button className="chat-toggle-btn" onClick={() => setIsChatOpen(true)}>
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
        </button>
      )}

      {/* Chat Widget */}
      <div className={`chat-widget ${isChatOpen ? 'open' : ''}`}>
        <div className="chat-widget-header">
          <ChatHeader />
          <button className="close-btn" onClick={() => setIsChatOpen(false)}>
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
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
    </div>
  )
}

export default App
