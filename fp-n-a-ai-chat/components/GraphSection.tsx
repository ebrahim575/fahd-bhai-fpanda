"use client"

import { useState, useEffect } from "react"
import { motion } from "framer-motion"

export default function GraphSection() {
  const [graphs, setGraphs] = useState<number[]>([])

  useEffect(() => {
    // Simulate fetching graph data
    const fetchGraphs = async () => {
      // In a real application, this would be an API call
      const numGraphs = Math.floor(Math.random() * 3) + 1 // Random number of graphs (1-3)
      setGraphs(Array.from({ length: numGraphs }, (_, i) => i))
    }

    fetchGraphs()
  }, [])

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
      {graphs.map((graph) => (
        <motion.div
          key={graph}
          className="bg-card p-3 rounded-md shadow-lg"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: graph * 0.1 }}
        >
          <div className="h-32 bg-secondary rounded-md flex items-center justify-center">
            <svg className="w-8 h-8 text-muted-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"
              />
            </svg>
          </div>
          <p className="mt-2 text-center text-xs font-normal text-muted-foreground">Financial Graph {graph + 1}</p>
        </motion.div>
      ))}
    </div>
  )
}

