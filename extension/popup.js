document.getElementById('downloadBtn').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  statusDiv.textContent = 'Sending request...';

  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = tab?.url || '';

  const isYouTube =
    url.includes('youtube.com/watch') ||
    url.includes('youtu.be/') ||
    url.includes('youtube.com/shorts/');

  if (!isYouTube) {
    statusDiv.textContent = 'Please open a YouTube video!';
    return;
  }

  try {
    const response = await fetch('http://localhost:5000/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    const data = await response.json();
    statusDiv.textContent = data.message;
  } catch (error) {
    statusDiv.textContent = 'Server offline! Run server.py first.';
  }
});
