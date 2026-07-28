import React from 'react';

const SEVERITY_META = {
  Critical: { className: 'critical', pct: 100 },
  Major: { className: 'major', pct: 66 },
  Minor: { className: 'minor', pct: 33 },
};

export default function RiskAssessmentPanel({ complaint }) {
  const hasAssessment = complaint.severity_level != null;
  const meta = SEVERITY_META[complaint.severity_level] || { className: 'pending', pct: 0 };
  const scorePct = complaint.risk_score != null ? (complaint.risk_score / 10) * 100 : 0;

  return (
    <div className="risk-panel">
      <div className="risk-panel__head">
        <h2 className="risk-panel__title">AI Copilot — Risk Assessment</h2>
        <span className="risk-panel__badge">LangGraph</span>
      </div>

      {!hasAssessment ? (
        <div className="risk-panel__pending">
          Risk assessment not run — complaint is incomplete. Provide the missing fields
          and resubmit to generate a risk score.
        </div>
      ) : (
        <>
          <div className={`risk-severity risk-severity--${meta.className}`}>
            <span className="risk-severity__label">{complaint.severity_level}</span>
            <span className="risk-severity__score">{complaint.risk_score}<span className="risk-severity__scale">/10</span></span>
          </div>

          <div className="risk-gauge" aria-hidden="true">
            <div className={`risk-gauge__fill risk-gauge__fill--${meta.className}`} style={{ width: `${scorePct}%` }} />
          </div>

          <div className="risk-block">
            <span className="risk-block__label">Reasoning</span>
            <p className="risk-block__text">{complaint.risk_reasoning}</p>
          </div>

          <div className="risk-block">
            <span className="risk-block__label">Suggested root cause</span>
            <p className="risk-block__text">{complaint.root_cause_suggestion}</p>
          </div>

          <div className="risk-block">
            <span className="risk-block__label">CAPA recommendation</span>
            <p className="risk-block__text">{complaint.capa_recommendation}</p>
          </div>

          <div className="risk-block risk-block--summary">
            <span className="risk-block__label">Summary</span>
            <p className="risk-block__text">{complaint.ai_summary}</p>
          </div>

          <p className="risk-panel__disclaimer">
            AI-generated hypotheses for investigator review — not a substitute for formal QA sign-off.
          </p>
        </>
      )}
    </div>
  );
}
