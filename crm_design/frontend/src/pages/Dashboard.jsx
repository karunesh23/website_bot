import { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard() {
  const [data, setData] = useState({
    stats: { new_leads: 0, open_tickets: 0, pending_callbacks: 0, escalations: 0 },
    recent_tickets: [],
    escalations_list: []
  });

  useEffect(() => {
    // In a real app, you would configure an Axios instance with base URL.
    axios.get('http://localhost:8000/api/crm/dashboard')
      .then(res => setData(res.data))
      .catch(err => console.error("Failed to fetch dashboard data:", err));
  }, []);

  return (
    <div>
      <div className="dashboard-cards">

        <div className="stat-card">
          <div className="stat-title">New Leads</div>
          <div className="stat-value" style={{ color: '#184e7f' }}>{data.stats.new_leads}</div>
        </div>
        <div className="stat-card warning">
          <div className="stat-title">Open Tickets</div>
          <div className="stat-value warning-text">{data.stats.open_tickets}</div>
        </div>
        <div className="stat-card" style={{ borderLeftColor: '#f97316' }}>
          <div className="stat-title">Pending Callbacks</div>
          <div className="stat-value" style={{ color: '#f97316' }}>{data.stats.pending_callbacks}</div>
        </div>
        <div className="stat-card danger">
          <div className="stat-title">Escalations</div>
          <div className="stat-value danger-text">{data.stats.escalations}</div>
        </div>
      </div>

      <div className="dashboard-grid">
        <div className="panel">
          <div className="panel-header">
            Recent Tickets
          </div>
          <div className="panel-body" style={{ padding: 0 }}>
            <table style={{ width: '100%' }}>
              <thead>
                <tr>
                  <th style={{ backgroundColor: '#184e7f', color: 'white' }}>Ticket ID</th>
                  <th style={{ backgroundColor: '#184e7f', color: 'white' }}>Query</th>
                  <th style={{ backgroundColor: '#184e7f', color: 'white' }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {data.recent_tickets.map((t, i) => (
                  <tr key={i}>
                    <td style={{ color: '#184e7f', fontWeight: '600' }}>{t.id}</td>
                    <td>{t.query}</td>
                    <td>
                      <span className={`badge ${t.status.toLowerCase().replace(' ', '-')}`}>
                        {t.status}
                      </span>
                    </td>
                  </tr>
                ))}
                {data.recent_tickets.length === 0 && (
                  <tr>
                    <td colSpan="3" style={{ textAlign: 'center', padding: '20px' }}>No recent tickets</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        <div className="panel">
          <div className="panel-header">
            Active Escalations
          </div>
          <div className="panel-body" style={{ padding: 0 }}>
            <table style={{ width: '100%' }}>
              <thead>
                <tr>
                  <th style={{ backgroundColor: '#184e7f', color: 'white' }}>Escalation ID</th>
                  <th style={{ backgroundColor: '#184e7f', color: 'white' }}>Reason</th>
                  <th style={{ backgroundColor: '#184e7f', color: 'white' }}>Raised On</th>
                </tr>
              </thead>
              <tbody>
                {(data.escalations_list || []).map((e, i) => (
                  <tr key={i}>
                    <td style={{ color: '#184e7f', fontWeight: '600' }}>{e.id}</td>
                    <td>{e.reason}</td>
                    <td>{e.raised_on ? new Date(e.raised_on).toLocaleString() : '-'}</td>
                  </tr>
                ))}
                {(!data.escalations_list || data.escalations_list.length === 0) && (
                  <tr>
                    <td colSpan="3" style={{ textAlign: 'center', padding: '20px' }}>No active escalations</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
