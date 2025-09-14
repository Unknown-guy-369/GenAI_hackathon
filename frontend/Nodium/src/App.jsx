import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import InputForm from './components/Inputform'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <InputForm />
    </>
  )
}

export default App
