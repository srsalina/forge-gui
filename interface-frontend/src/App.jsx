import { useState } from 'react'
import { Button } from './components/ui/button'
import PenTestGUI from './components/PenTestGUI'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <main>
      <PenTestGUI />
    </main>
    </>
  )
}

export default App
