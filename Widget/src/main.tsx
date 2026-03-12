import { createRoot } from 'react-dom/client'
import './index.css'
import ChatWidget from './components/ChatWidget'

const script =
  (document.currentScript as HTMLScriptElement) ||
  document.querySelector<HTMLScriptElement>('script[data-api-key]');

const apiKey = script?.getAttribute('data-api-key') ?? '';

const container = document.createElement("div");
document.body.appendChild(container);

createRoot(container).render(<ChatWidget apiKey={apiKey} />);