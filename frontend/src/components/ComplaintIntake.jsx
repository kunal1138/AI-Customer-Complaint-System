import React, { useState, useRef } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { processTextComplaint, processFileComplaint, clearCurrentResult } from '../store/complaintsSlice';

export default function ComplaintIntake() {
  const dispatch = useDispatch();
  const { status, error } = useSelector((state) => state.complaints);
  const [text, setText] = useState('');
  const [mode, setMode] = useState('text'); // 'text' | 'file'
  const fileInputRef = useRef(null);

  const isLoading = status === 'loading';

  function handleSubmitText(e) {
    e.preventDefault();
    if (!text.trim()) return;
    dispatch(clearCurrentResult());
    dispatch(processTextComplaint(text));
  }

  function handleFileChange(e) {
    const file = e.target.files?.[0];
    if (!file) return;
    dispatch(clearCurrentResult());
    dispatch(processFileComplaint(file));
  }

  return (
    <div className="intake-card">
      <div className="intake-card__head">
        <h2 className="intake-card__title">New complaint intake</h2>
        <div className="intake-card__modes" role="tablist" aria-label="Complaint input method">
          <button
            role="tab"
            aria-selected={mode === 'text'}
            className={`mode-tab ${mode === 'text' ? 'mode-tab--active' : ''}`}
            onClick={() => setMode('text')}
            type="button"
          >
            Paste text
          </button>
          <button
            role="tab"
            aria-selected={mode === 'file'}
            className={`mode-tab ${mode === 'file' ? 'mode-tab--active' : ''}`}
            onClick={() => setMode('file')}
            type="button"
          >
            Upload file
          </button>
        </div>
      </div>

      {mode === 'text' ? (
        <form onSubmit={handleSubmitText}>
          <textarea
            className="intake-textarea"
            placeholder="Paste the complaint email, letter, or manual entry here…"
            value={text}
            onChange={(e) => setText(e.target.value)}
            rows={7}
            disabled={isLoading}
          />
          <div className="intake-card__footer">
            <span className="intake-hint">Text is processed by the LangGraph agent — extraction, risk, and CAPA analysis run automatically.</span>
            <button className="btn-primary" type="submit" disabled={isLoading || !text.trim()}>
              {isLoading ? 'Processing…' : 'Process complaint'}
            </button>
          </div>
        </form>
      ) : (
        <div className="intake-upload">
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.txt"
            onChange={handleFileChange}
            disabled={isLoading}
            id="complaint-file-input"
            className="intake-upload__input"
          />
          <label htmlFor="complaint-file-input" className="intake-upload__label">
            {isLoading ? 'Processing…' : 'Choose a PDF or email (.txt) file'}
          </label>
          <span className="intake-hint">Accepted: complaint PDFs, or exported email text files.</span>
        </div>
      )}

      {error && (
        <div className="intake-error" role="alert">
          Couldn't process this complaint: {error}
        </div>
      )}
    </div>
  );
}
