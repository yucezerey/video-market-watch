import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Pipeline from './pages/Pipeline'
import Scoring from './pages/Scoring'
import Tools from './pages/Tools'
import About from './pages/About'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/pipeline" element={<Pipeline />} />
          <Route path="/scoring" element={<Scoring />} />
          <Route path="/tools" element={<Tools />} />
          <Route path="/about" element={<About />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
