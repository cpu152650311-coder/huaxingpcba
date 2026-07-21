async function handleInquiry(event) {
  event.preventDefault();
  const form = event.target;
  // Collect form fields
  const fileInput = form.querySelector('[name="attachment"]');
  const hasFiles = fileInput && fileInput.files && fileInput.files.length > 0;
  let msg = form.querySelector('[name="message"]')?.value || '';
  if (hasFiles) {
    const names = Array.from(fileInput.files).map(f => f.name).join(', ');
    msg = `[Attachments: ${names} — please email files to sales@huaxingpcba.com]\n\n${msg}`;
  }
  const data = {
    name: form.querySelector('[name="name"]')?.value || '',
    email: form.querySelector('[name="email"]')?.value || '',
    message: msg,
    source: 'huaxingpcba.com',
  };
  try {
    const res = await fetch('https://inquiry-proxy.cpu152650311.workers.dev/inquiry', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const result = await res.json();
    if (result.success) {
      window.location.href = '/thank-you.html';
    } else {
      alert(result.message || 'Submission failed. Please try again.');
    }
  } catch {
    alert('Network error. Please try again later.');
  }
  return false;
}
