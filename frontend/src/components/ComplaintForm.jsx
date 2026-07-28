import React from 'react';

function Field({ label, value, mono = false, flagged = false }) {
  return (
    <div className={`field ${flagged ? 'field--flagged' : ''}`}>
      <span className="field__label">{label}</span>
      <span className={`field__value ${mono ? 'field__value--mono' : ''} ${!value ? 'field__value--empty' : ''}`}>
        {value || (flagged ? 'Missing' : '—')}
      </span>
    </div>
  );
}

export default function ComplaintForm({ complaint }) {
  const missing = new Set(complaint.missing_fields || []);

  return (
    <div className="log-form">
      <div className="log-form__head">
        <h2 className="log-form__title">Log Customer Complaint</h2>
        <span className="log-form__ref">{complaint.complaint_ref}</span>
      </div>

      {complaint.completeness_status === 'Incomplete' && (
        <div className="log-form__banner">
          Incomplete submission — missing {(complaint.missing_fields || []).join(', ')}.
          Risk assessment was skipped until these are provided.
        </div>
      )}

      {complaint.is_duplicate && (
        <div className="log-form__banner log-form__banner--info">
          Possible duplicate of complaint #{complaint.duplicate_of_id} ({complaint.duplicate_confidence}% confidence)
        </div>
      )}

      <div className="log-form__grid">
        <Field label="Product name" value={complaint.product_name} flagged={missing.has('product_name')} />
        <Field label="Batch / lot number" value={complaint.batch_number} mono flagged={missing.has('batch_number')} />
        <Field label="Product category" value={complaint.product_category} />
        <Field label="Manufacturing date" value={complaint.manufacturing_date} mono />
        <Field label="Expiry date" value={complaint.expiry_date} mono />
        <Field label="Quantity affected" value={complaint.quantity_affected} />
        <Field label="Complaint type" value={complaint.complaint_type} />
        <Field label="Customer name" value={complaint.customer_name} />
        <Field label="Customer organization" value={complaint.customer_organization} />
      </div>

      <div className="log-form__description">
        <span className="field__label">Description</span>
        <p className="log-form__description-text">
          {complaint.complaint_description || 'Not provided'}
        </p>
      </div>
    </div>
  );
}
