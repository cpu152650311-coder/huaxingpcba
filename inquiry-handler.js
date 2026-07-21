async function handleInquiry(event) {
  event.preventDefault();
  const form = event.target;
  
  const formData = new FormData();
  formData.append('name', form.querySelector('[name="name"]')?.value || '');
  formData.append('email', form.querySelector('[name="email"]')?.value || '');
  formData.append('message', form.querySelector('[name="message"]')?.value || '');
  formData.append('source', 'huaxingpcba.com');

  // Attach files (real upload — no more fake filenames!)
  const fileInput = form.querySelector('[name="attachment"]');
  if (fileInput && fileInput.files) {
    for (const file of fileInput.files) {
      formData.append('files', file);
    }
  }

  try {
    const res = await fetch('https://inquiry-proxy.cpu152650311.workers.dev/inquiry-upload', {
      method: 'POST',
      body: formData,
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
