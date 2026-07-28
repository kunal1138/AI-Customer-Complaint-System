import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import ComplaintIntake from './components/ComplaintIntake.jsx';
import ComplaintForm from './components/ComplaintForm.jsx';
import RiskAssessmentPanel from './components/RiskAssessmentPanel.jsx';
import ComplaintHistory from './components/ComplaintHistory.jsx';
import { loadComplaintHistory } from './store/complaintsSlice';
import './App.css';
import './components/components.css';

export default function App() {
  const dispatch = useDispatch();
  const { currentResult, status } = useSelector((state) => state.complaints);

  useEffect(() => {
    dispatch(loadComplaintHistory());
  }, [dispatch, currentResult]);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header__brand">
          <span className="app-header__mark">AIVOA</span>
          <span className="app-header__divider" aria-hidden="true">/</span>
          <span className="app-header__title">Customer Complaint Management</span>
        </div>
        <span className="app-header__tag">Pharmaceutical QMS · AI Copilot</span>
      </header>

      <main className="app-main">
        <section className="app-main__intake">
          <span className="section-eyebrow">01 — Intake</span>
          <ComplaintIntake />
        </section>

        {status === 'succeeded' && currentResult && (
          <section className="app-main__results">
            <div>
              <span className="section-eyebrow">02 — Complaint record</span>
              <ComplaintForm complaint={currentResult} />
            </div>
            <div>
              <span className="section-eyebrow">03 — Risk assessment</span>
              <RiskAssessmentPanel complaint={currentResult} />
            </div>
          </section>
        )}

        <section className="app-main__history">
          <span className="section-eyebrow">04 — Complaint log</span>
          <ComplaintHistory />
        </section>
      </main>
    </div>
  );
}
