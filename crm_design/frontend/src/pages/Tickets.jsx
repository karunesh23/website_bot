import { useState, useEffect } from 'react';
import axios from 'axios';
import '../index.css';

function Tickets() {
  const [tickets, setTickets] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [selectedTicket, setSelectedTicket] = useState(null);

  useEffect(() => {
    fetchTickets();
  }, []);

  const fetchTickets = () => {
    axios.get('http://localhost:8000/api/crm/tickets')
      .then(res => setTickets(res.data))
      .catch(err => console.error(err));
  };

  const filteredTickets = tickets.filter(t => {
    if (statusFilter && t.status !== statusFilter) return false;
    if (priorityFilter && t.priority !== priorityFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const matches = 
        t.ticket_id?.toLowerCase().includes(q) ||
        t.category?.toLowerCase().includes(q) ||
        t.client_reference_id?.toLowerCase().includes(q);
      if (!matches) return false;
    }
    return true;
  });

  const headerStyle = { backgroundColor: '#184e7f', color: 'white', borderBottom: 'none', padding: '16px 20px' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ color: '#184e7f', fontSize: '1.25rem', margin: 0 }}>Tickets</h2>
      </div>

      <div style={{ display: 'flex', gap: '15px' }}>
        <input 
          type="text" 
          placeholder="Search by Ticket ID, Ref ID, or Category..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
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
          <option value="OPEN">Open (New)</option>
          <option value="Sample Received">Sample Received</option>
          <option value="Testing in Progress">Testing in Progress</option>
          <option value="Report Under Review">Report Under Review</option>
          <option value="Report Issued">Report Issued</option>
          <option value="Resolved">Resolved</option>
        </select>
        <select 
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
          style={{
            padding: '12px 16px',
            borderRadius: '6px',
            border: '1px solid var(--border-color)',
            outline: 'none',
            fontSize: '0.9rem',
            backgroundColor: 'white'
          }}
        >
          <option value="">All Priorities</option>
          <option value="Urgent">Urgent</option>
          <option value="Normal">Normal</option>
        </select>
      </div>

      <div className="table-container" style={{ padding: '16px', backgroundColor: 'white' }}>
        <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: 0 }}>
          <thead>
            <tr>
              <th style={{ ...headerStyle, borderTopLeftRadius: '8px' }}>Ticket ID</th>
              <th style={{ ...headerStyle }}>Client/Ref ID</th>
              <th style={{ ...headerStyle }}>Category</th>
              <th style={{ ...headerStyle }}>Description</th>
              <th style={{ ...headerStyle }}>Priority</th>
              <th style={{ ...headerStyle }}>Status</th>
              <th style={{ ...headerStyle }}>Last Updated</th>
              <th style={{ ...headerStyle, borderTopRightRadius: '8px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredTickets.map((t, i) => (
              <tr key={i}>
                <td style={{ color: '#184e7f', fontWeight: '600' }}>{t.ticket_id}</td>
                <td>{t.client_reference_id}</td>
                <td>{t.category}</td>
                <td style={{ maxWidth: '200px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {t.description || '-'}
                </td>
                <td>
                  <span className={`badge priority-${t.priority?.toLowerCase()}`}>
                    {t.priority}
                  </span>
                </td>
                <td>
                  <span className={`badge ${t.status?.toLowerCase().replace(/ /g, '-') || 'new'}`}>
                    {t.status || 'OPEN'}
                  </span>
                </td>
                <td>{new Date(t.last_updated).toLocaleString()}</td>
                <td>
                  <button onClick={() => setSelectedTicket(t)} style={{ padding: '6px 12px', cursor: 'pointer', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '4px' }}>
                    View Details
                  </button>
                </td>
              </tr>
            ))}
            {filteredTickets.length === 0 && (
              <tr><td colSpan="8" style={{ textAlign: 'center' }}>No tickets found.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {selectedTicket && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', width: '600px', maxWidth: '90%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ margin: 0, color: '#184e7f' }}>Ticket Details: {selectedTicket.ticket_id}</h2>
              <button onClick={() => setSelectedTicket(null)} style={{ background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer' }}>×</button>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div style={{ display: 'flex', gap: '20px' }}>
                <div style={{ flex: 1 }}>
                  <strong>Client/Ref ID:</strong> {selectedTicket.client_reference_id}
                </div>
                <div style={{ flex: 1 }}>
                  <strong>Category:</strong> {selectedTicket.category}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '20px' }}>
                <div style={{ flex: 1 }}>
                  <strong>Priority:</strong> {selectedTicket.priority}
                </div>
                <div style={{ flex: 1 }}>
                  <strong>Last Updated:</strong> {new Date(selectedTicket.last_updated).toLocaleString()}
                </div>
              </div>
              <div>
                <strong>Description:</strong>
                <p style={{ margin: '5px 0', backgroundColor: '#f8fafc', padding: '10px', borderRadius: '4px', minHeight: '60px' }}>
                  {selectedTicket.description || 'No description provided.'}
                </p>
              </div>
              
              <div style={{ marginTop: '10px', borderTop: '1px solid #e2e8f0', paddingTop: '15px' }}>
                <h3 style={{ margin: '0 0 10px 0', fontSize: '1rem' }}>Status Tracking</h3>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Update Status:</label>
                <select 
                  value={selectedTicket.status || 'OPEN'}
                  onChange={(e) => {
                    const newStatus = e.target.value;
                    setSelectedTicket({...selectedTicket, status: newStatus});
                    // Note: Trigger API call to update status
                  }}
                  style={{ width: '100%', padding: '10px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                >
                  <option value="OPEN">Open</option>
                  <option value="Sample Received">Sample Received</option>
                  <option value="Testing in Progress">Testing in Progress</option>
                  <option value="Report Under Review">Report Under Review</option>
                  <option value="Report Issued">Report Issued</option>
                  <option value="Resolved">Resolved</option>
                </select>
              </div>
            </div>
            
            <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button onClick={() => setSelectedTicket(null)} style={{ padding: '8px 16px', borderRadius: '4px', border: '1px solid #cbd5e1', backgroundColor: 'white', cursor: 'pointer' }}>Cancel</button>
              <button onClick={() => {
                axios.put(`http://localhost:8000/api/crm/tickets/${selectedTicket.ticket_id}`, {
                  status: selectedTicket.status
                })
                .then(() => {
                  fetchTickets();
                  setSelectedTicket(null);
                })
                .catch(err => console.error("Failed to update ticket", err));
              }} style={{ padding: '8px 16px', borderRadius: '4px', border: 'none', backgroundColor: '#184e7f', color: 'white', cursor: 'pointer' }}>Save Changes</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Tickets;
