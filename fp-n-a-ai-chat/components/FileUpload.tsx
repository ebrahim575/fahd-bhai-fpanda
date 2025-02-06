"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Upload } from "lucide-react"

export default function FileUpload() {
  const [isUploading, setIsUploading] = useState(false)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setIsUploading(true)
      // Simulate file upload
      setTimeout(() => {
        setIsUploading(false)
        alert("File uploaded successfully!")
      }, 2000)
    }
  }

  return (
    <div className="relative">
      <input type="file" id="file-upload" className="hidden" onChange={handleFileUpload} accept=".csv,.xlsx,.xls" />
      <motion.label
        htmlFor="file-upload"
        className="cursor-pointer inline-flex items-center px-2 py-1 border border-border rounded-md text-xs font-normal text-foreground bg-background hover:bg-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Upload className="mr-1 h-3 w-3" />
        {isUploading ? "Uploading..." : "Upload File"}
      </motion.label>
    </div>
  )
}

