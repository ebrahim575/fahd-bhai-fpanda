import { Suspense } from "react"
import dynamic from "next/dynamic"
import ChatInterface from "@/components/ChatInterface"
import FileUpload from "@/components/FileUpload"
import ThemeToggle from "@/components/ThemeToggle"

const DynamicGraphSection = dynamic(() => import("@/components/GraphSection"), {
  ssr: false,
  loading: () => <div className="h-64 bg-secondary animate-pulse rounded-md"></div>,
})

export default function Home() {
  return (
    <div className="flex flex-col h-screen bg-background text-foreground">
      <header className="flex justify-between items-center p-3 border-b border-border">
        <h1 className="text-xl font-medium text-primary">FP&A AI</h1>
        <div className="flex items-center space-x-3">
          <FileUpload />
          <ThemeToggle />
        </div>
      </header>
      <main className="flex-grow flex flex-col p-3 space-y-3 overflow-hidden max-w-5xl mx-auto w-full">
        <div className="flex-grow overflow-y-auto">
          <DynamicGraphSection />
        </div>
        <div className="flex-shrink-0 sticky bottom-0 bg-background pb-3">
          <ChatInterface />
        </div>
      </main>
    </div>
  )
}

