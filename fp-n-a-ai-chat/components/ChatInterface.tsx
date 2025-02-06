"use client"

import { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"

type Message = {
  id: number
  text: string
  sender: "user" | "ai"
  graphs?: any[]
  data?: any[]
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = { id: Date.now(), text: input, sender: "user" }
    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsTyping(true)

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input }),
      })

      const data = await response.json()
      const aiMessage: Message = { 
        id: Date.now(), 
        text: data.response, 
        sender: "ai",
        graphs: data.graphs,
        data: data.data
      }
      setMessages((prev) => [...prev, aiMessage])
      
      // Update graphs if present in response
      if (data.graphs?.length > 0) {
        window.dispatchEvent(new CustomEvent('updateGraphs', { 
          detail: { 
            graphs: data.graphs, 
            data: data.data,
            append: true // New flag to indicate this is from chat
          }
        }))
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsTyping(false)
    }
  }

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [messagesEndRef]) //Corrected dependency

  return (
    <div className="flex flex-col h-full">
      <div className="flex-grow overflow-y-auto scrollbar-thin scrollbar-thumb-secondary scrollbar-track-transparent">
        <div className="flex flex-col space-y-3 p-3">
          <AnimatePresence>
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`flex ${message.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-xs md:max-w-md lg:max-w-lg xl:max-w-xl px-3 py-2 rounded-md text-xs ${
                    message.sender === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-secondary text-secondary-foreground"
                  }`}
                >
                  {message.text}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
          {isTyping && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="flex justify-start">
              <div className="bg-secondary text-secondary-foreground px-3 py-2 rounded-md text-xs">
                <span className="animate-pulse">●●●</span>
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      <div className="border-t border-border bg-background p-3">
        <form onSubmit={handleSubmit} className="flex items-center space-x-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            className="flex-grow px-3 py-2 bg-input text-foreground rounded-md text-xs focus:outline-none focus:ring-2 focus:ring-primary"
          />
          <button
            type="submit"
            className="px-3 py-2 bg-primary text-primary-foreground rounded-md text-xs hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}

