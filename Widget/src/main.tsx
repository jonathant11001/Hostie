import { createRoot } from 'react-dom/client'
import './index.css'
import ChatWidget from './components/ChatWidget'

const container = document.createElement("div");
document.body.appendChild(container);

createRoot(container).render(<ChatWidget />);