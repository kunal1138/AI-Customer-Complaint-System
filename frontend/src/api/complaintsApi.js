const API_BASE = 'http://localhost:8000/api';

export async function submitTextComplaint(text) {
  const res = await fetch(`${API_BASE}/complaints/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, source_type: 'manual' }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Something went wrong' }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export async function submitFileComplaint(file) {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/complaints/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Something went wrong' }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

export async function fetchComplaints() {
  const res = await fetch(`${API_BASE}/complaints`);
  if (!res.ok) throw new Error('Failed to load complaints');
  return res.json();
}
