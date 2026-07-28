import React from 'react';
import { useSelector } from 'react-redux';

const SEVERITY_DOT = { Critical: 'critical', Major: 'major', Minor: 'minor' };

export default function ComplaintHistory() {
  const { history, historyStatus } = useSelector((state) => state.complaints);

  if (historyStatus === 'loading' && history.length === 0) {
    return <div className="history-empty">Loading complaint history…</div>;
  }

  if (history.length === 0) {
    return (
      <div className="history-empty">
        No complaints logged yet. Submit one above to see it appear here.
      </div>
    );
  }

  return (
    <div className="history-card">
      <h2 className="history-card__title">All records</h2>
      <div className="history-table">
        <div className="history-table__row history-table__row--head">
          <span>Reference</span>
          <span>Product</span>
          <span>Type</span>
          <span>Severity</span>
          <span>Status</span>
        </div>
        {history.map((c) => (
          <div className="history-table__row" key={c.id}>
            <span className="history-table__ref">{c.complaint_ref}</span>
            <span>{c.product_name || '—'}</span>
            <span>{c.complaint_type || '—'}</span>
            <span>
              {c.severity_level ? (
                <span className={`severity-dot severity-dot--${SEVERITY_DOT[c.severity_level] || 'pending'}`}>
                  {c.severity_level}
                </span>
              ) : '—'}
            </span>
            <span>{c.status}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
