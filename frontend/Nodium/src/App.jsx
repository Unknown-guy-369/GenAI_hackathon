import { useState } from 'react'
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
