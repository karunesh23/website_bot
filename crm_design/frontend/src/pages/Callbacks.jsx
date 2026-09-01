import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import '../index.css';

function Callbacks() {
  const [callbacks, setCallbacks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [expandedSessionId, setExpandedSessionId] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/crm/callbacks')
      .then(res => res.json())
      .then(data => {
        setCallbacks(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching callbacks:', err);
        setLoading(false);
      });
  }, []);

  const filteredCallbacks = callbacks.filter(cb => {
    if (statusFilter && cb.status !== statusFilter) return false;
    if (searchTerm) {
      const q = searchTerm.toLowerCase();
      const matches = 
        cb.customer_name?.toLowerCase().includes(q) ||
        cb.email?.toLowerCase().includes(q) ||
        cb.phone?.includes(searchTerm);
      if (!matches) return false;
    }
    return true;
  });

  const getStatusBadge = (status) => {
    switch (status) {
      case 'Requested': return <span className="status-badge status-new">Requested</span>;
      case 'Sent to Evoke': return <span className="status-badge status-progress">Sent to Evoke</span>;
      case 'Connected': return <span className="status-badge status-resolved">Connected</span>;
      case 'Missed': return <span className="status-badge status-open">Missed</span>;
      default: return <span className="status-badge status-new">{status || 'Requested'}</span>;
    }
  };

  const headerStyle = { backgroundColor: '#184e7f', color: 'white', borderBottom: 'none', padding: '16px 20px', textTransform: 'uppercase', fontSize: '0.85rem' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ color: '#184e7f', fontSize: '1.25rem', margin: 0 }}>Callbacks</h2>
      </div>

      <div style={{ display: 'flex', gap: '15px' }}>
        <input
          type="text"
          placeholder="Search by ID, Name, Email, or Phone..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            flex: 1,
            padding: '12px 16px',
            borderRadius: '6px',
            border: '1px solid var(--border-color)',
            outline: 'none',
            fontSize: '0.9rem',
            color: 'var(--text-main)'
          }}
        />
        <select 
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          style={{
            padding: '12px 16px',
            borderRadius: '6px',
            border: '1px solid var(--border-color)',
            outline: 'none',
            fontSize: '0.9rem',
            backgroundColor: 'white'
          }}
        >
          <option value="">All Statuses</option>
          <option value="Requested">Requested</option>
          <option value="Sent to Evoke">Sent to Evoke</option>
          <option value="Connected">Connected</option>
          <option value="Missed">Missed</option>
        </select>
      </div>
      <div className="table-container" style={{ padding: '16px', backgroundColor: 'white' }}>
        {loading ? (
          <div style={{ padding: '2rem', textAlign: 'center' }}>Loading callbacks...</div>
        ) : (
          <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: 0 }}>
            <thead>
              <tr>
                <th style={{ ...headerStyle, borderTopLeftRadius: '8px' }}>Callback ID</th>
                <th style={{ ...headerStyle }}>Customer</th>
                <th style={{ ...headerStyle }}>Phone</th>
                <th style={{ ...headerStyle }}>Email</th>
                <th style={{ ...headerStyle }}>Topic</th>
                <th style={{ ...headerStyle }}>Requested Time</th>
                <th style={{ ...headerStyle }}>Status</th>
                <th style={{ ...headerStyle }}>Session ID</th>
                <th style={{ ...headerStyle, borderTopRightRadius: '8px' }}>Related Lead/Ticket</th>
              </tr>
            </thead>
            <tbody>
              {filteredCallbacks.map((cb, idx) => (
                <tr key={idx}>
                  <td>CB-{cb.callback_id}</td>
                  <td><div className="font-medium">{cb.customer_name || 'N/A'}</div></td>
                  <td>{cb.phone}</td>
                  <td>{cb.email}</td>
                  <td>{cb.topic}</td>
                  <td>{cb.requested_time ? new Date(cb.requested_time).toLocaleString() : '-'}</td>
                  <td>{getStatusBadge(cb.status)}</td>
                  <td>
                    <div 
                      onClick={() => setExpandedSessionId(expandedSessionId === cb.callback_id ? null : cb.callback_id)}
                      style={{ 
                        maxWidth: expandedSessionId === cb.callback_id ? '300px' : '100px', 
                        overflow: expandedSessionId === cb.callback_id ? 'visible' : 'hidden', 
                        textOverflow: expandedSessionId === cb.callback_id ? 'clip' : 'ellipsis', 
                        whiteSpace: expandedSessionId === cb.callback_id ? 'normal' : 'nowrap',
                        wordBreak: 'break-all',
                        cursor: 'pointer'
                      }} 
                      title={cb.session_id}
                    >
                      {cb.session_id || '-'}
                    </div>
                  </td>
                  <td>
                    {cb.related_lead && <span style={{ marginRight: '8px' }}>Lead: {cb.related_lead}</span>}
                    {cb.related_ticket && <span>Ticket: {cb.related_ticket}</span>}
                    {!cb.related_lead && !cb.related_ticket && '-'}
                  </td>
                </tr>
              ))}
              {filteredCallbacks.length === 0 && (
                <tr>
                  <td colSpan="8" style={{ textAlign: 'center', padding: '2rem' }}>
                    No callbacks found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Callbacks;
