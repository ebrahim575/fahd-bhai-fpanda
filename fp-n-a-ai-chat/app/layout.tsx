import "./globals.css"
import type React from "react"

export const metadata = {
  title: "FP&A AI",
  description: "AI-powered financial planning and analysis assistant",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-background text-foreground">{children}</body>
    </html>
  )
}

