import ReactMarkdown from 'react-markdown';

export default function ChatMessage({ message }) {
  return (
    <div className={`message-wrapper ${message.role}`}>
      <div className="message-bubble">
        <ReactMarkdown>{message.content}</ReactMarkdown>
      </div>
    </div>
  );
}
