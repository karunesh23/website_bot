import { useState, useEffect } from 'react';
import '../index.css';

function CallLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/crm/call-logs')
      .then(res => res.json())
      .then(data => {
        setLogs(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching call logs:', err);
        setLoading(false);
      });
  }, []);

  const headerStyle = { backgroundColor: '#184e7f', color: 'white', borderBottom: 'none', padding: '16px 20px', textTransform: 'uppercase', fontSize: '0.85rem' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ color: '#184e7f', fontSize: '1.25rem', margin: 0 }}>Call Logs / Escalations</h2>
      </div>

      <div className="table-container" style={{ padding: '16px', backgroundColor: 'white' }}>
        {loading ? (
            <div style={{ padding: '2rem', textAlign: 'center' }}>Loading call logs...</div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: 0 }}>
                <thead>
                  <tr>
                    <th style={{ ...headerStyle, borderTopLeftRadius: '8px' }}>Call ID</th>
                    <th style={{ ...headerStyle }}>Callback ID</th>
                    <th style={{ ...headerStyle }}>Member ID</th>
                    <th style={{ ...headerStyle }}>Received At</th>
                    <th style={{ ...headerStyle }}>Picked</th>
                    <th style={{ ...headerStyle }}>Picked At</th>
                    <th style={{ ...headerStyle }}>Escalated To</th>
                    <th style={{ ...headerStyle }}>Outcome</th>
                    <th style={{ ...headerStyle }}>Duration (s)</th>
                    <th style={{ ...headerStyle }}>Recording URL</th>
                    <th style={{ ...headerStyle, borderTopRightRadius: '8px' }}>Call Summary</th>
                  </tr>
                </thead>
                <tbody>
                  {logs.map((log, idx) => (
                    <tr key={idx}>
                      <td><div style={{ maxWidth: '80px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }} title={log.call_id}>{log.call_id}</div></td>
                      <td>{log.callback_id || '-'}</td>
                      <td>{log.member_id ? `TM-${log.member_id}` : '-'}</td>
                      <td style={{ whiteSpace: 'nowrap' }}>{log.received_at ? new Date(log.received_at).toLocaleString() : '-'}</td>
                      <td>
                        <span className={`status-badge ${log.picked ? 'status-resolved' : 'status-open'}`}>
                          {log.picked ? 'Yes' : 'No'}
                        </span>
                      </td>
                      <td style={{ whiteSpace: 'nowrap' }}>{log.picked_at ? new Date(log.picked_at).toLocaleString() : '-'}</td>
                      <td>{log.escalated_to ? `TM-${log.escalated_to}` : '-'}</td>
                      <td>
                        {log.outcome && (
                          <span className={`status-badge ${log.outcome === 'Connected' ? 'status-resolved' : (log.outcome === 'Missed' ? 'status-open' : 'status-progress')}`}>
                            {log.outcome}
                          </span>
                        )}
                        {!log.outcome && '-'}
                      </td>
                      <td>{log.duration_seconds || '-'}</td>
                      <td>
                        {log.recording_url ? (
                          <a href={log.recording_url} target="_blank" rel="noopener noreferrer" style={{ color: '#184e7f', textDecoration: 'underline' }}>Play / Download</a>
                        ) : '-'}
                      </td>
                      <td>
                        <div style={{ maxWidth: '300px', whiteSpace: 'normal' }} title={log.call_summary}>
                          {log.call_summary || '-'}
                        </div>
                      </td>
                    </tr>
                  ))}
                  {logs.length === 0 && (
                    <tr>
                      <td colSpan="11" style={{ textAlign: 'center', padding: '2rem' }}>
                        No call logs found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
    </div>
  );
}

export default CallLogs;
