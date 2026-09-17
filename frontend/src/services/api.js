export const sendChatMessage = async (message, history) => {
  const response = await fetch('http://localhost:8000/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, history })
  });
  if (!response.ok) {
    throw new Error('Failed to get a response from the server.');
  }
  return response.json();
}
