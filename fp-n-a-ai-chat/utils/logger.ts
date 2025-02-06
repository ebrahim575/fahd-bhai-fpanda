export const logger = {
  log: (message: string) => {
    const timestamp = new Date().toISOString()
    const logMessage = `${timestamp} [INFO] ${message}`
    console.log(logMessage)
    try {
      const logs = JSON.parse(localStorage.getItem('app_logs') || '[]')
      logs.push(logMessage)
      localStorage.setItem('app_logs', JSON.stringify(logs))
    } catch (e) {
      console.error('Failed to save log:', e)
    }
  },
  error: (message: string) => {
    const timestamp = new Date().toISOString()
    const logMessage = `${timestamp} [ERROR] ${message}`
    console.error(logMessage)
    try {
      const logs = JSON.parse(localStorage.getItem('app_logs') || '[]')
      logs.push(logMessage)
      localStorage.setItem('app_logs', JSON.stringify(logs))
    } catch (e) {
      console.error('Failed to save log:', e)
    }
  },
  close: () => {}
} 