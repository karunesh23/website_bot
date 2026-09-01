import { useState, useEffect } from 'react';
import axios from 'axios';
import '../index.css';

function ClientsContacts() {
  const [clients, setClients] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedClient, setSelectedClient] = useState(null);
  const [client360Data, setClient360Data] = useState(null);
  const [loading360, setLoading360] = useState(false);
  const [expandedChats, setExpandedChats] = useState({});

  useEffect(() => {
    axios.get('http://localhost:8000/api/crm/clients')
      .then(res => setClients(res.data))
      .catch(err => console.error(err));
  }, []);

  const openClient360 = (client) => {
    setSelectedClient(client);
    setLoading360(true);
    axios.get(`http://localhost:8000/api/crm/client/${client.id}/360`)
      .then(res => {
        setClient360Data(res.data);
        setLoading360(false);
      })
      .catch(err => {
        console.error(err);
        setLoading360(false);
      });
  };

  const closeClient360 = () => {
    setSelectedClient(null);
    setClient360Data(null);
  };

  const filteredClients = clients.filter(c => {
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const matches =
        c.reference_id?.toLowerCase().includes(q) ||
        c.name?.toLowerCase().includes(q) ||
        c.email?.toLowerCase().includes(q) ||
        c.phone?.toLowerCase().includes(q);
      if (!matches) return false;
    }
    return true;
  });

  const sortedClients = [...filteredClients].sort((a, b) => {
    const numA = a.id || 0;
    const numB = b.id || 0;
    return numA - numB;
  });

  const headerStyle = { backgroundColor: '#184e7f', color: 'white', borderBottom: 'none', padding: '16px 20px' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ color: '#184e7f', fontSize: '1.25rem', margin: 0 }}>Clients & Contacts</h2>
      </div>

      <div>
        <input
          type="text"
          placeholder="Search by ID, Name, Email, or Phone..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            width: '100%',
            padding: '12px 16px',
            borderRadius: '6px',
            border: '1px solid var(--border-color)',
            outline: 'none',
            fontSize: '0.9rem',
            color: 'var(--text-main)'
          }}
        />
      </div>

      <div className="table-container" style={{ padding: '16px', backgroundColor: 'white' }}>
        <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: 0 }}>
          <thead>
            <tr>
              <th style={{ ...headerStyle, borderTopLeftRadius: '8px' }}>Reference ID</th>
              <th style={{ ...headerStyle }}>Name</th>
              <th style={{ ...headerStyle }}>Company Name</th>
              <th style={{ ...headerStyle }}>Email</th>
              <th style={{ ...headerStyle }}>Phone Number</th>
              <th style={{ ...headerStyle }}>Client Type</th>
              <th style={{ ...headerStyle }}>Status</th>
              <th style={{ ...headerStyle }}>Created At</th>
              <th style={{ ...headerStyle }}>Last Contacted</th>
              <th style={{ ...headerStyle, borderTopRightRadius: '8px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {sortedClients.map((c, i) => (
              <tr key={i}>
                <td style={{ color: '#184e7f', fontWeight: '600' }}>{c.reference_id}</td>
                <td>{c.name}</td>
                <td>{c.company_name || '-'}</td>
                <td>{c.email}</td>
                <td style={{ whiteSpace: 'nowrap' }}>{c.phone}</td>
                <td>{c.client_type}</td>
                <td>
                  <span className={`badge ${c.status?.toLowerCase().replace(' ', '-') || 'new'}`}>
                    {c.status || 'New'}
                  </span>
                </td>
                <td>{new Date(c.created_at).toLocaleDateString()}</td>
                <td>{c.last_contacted_at ? new Date(c.last_contacted_at).toLocaleDateString() : '-'}</td>
                <td>
                  <button onClick={() => openClient360(c)} style={{ padding: '6px 12px', cursor: 'pointer', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '4px' }}>
                    View 360°
                  </button>
                </td>
              </tr>
            ))}
            {sortedClients.length === 0 && (
              <tr><td colSpan="9" style={{ textAlign: 'center' }}>No records found.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {selectedClient && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', width: '80%', maxWidth: '800px', maxHeight: '90vh', overflowY: 'auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ margin: 0, color: '#184e7f' }}>Client 360° View: {selectedClient.name}</h2>
              <button onClick={closeClient360} style={{ background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer' }}>×</button>
            </div>

            {loading360 ? (
              <div>Loading client details...</div>
            ) : client360Data ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                <div style={{ display: 'flex', gap: '20px' }}>
                  <div style={{ flex: 1, backgroundColor: '#f8fafc', padding: '15px', borderRadius: '6px' }}>
                    <h3 style={{ margin: '0 0 10px 0', fontSize: '1.1rem' }}>Profile</h3>
                    <p><strong>Ref ID:</strong> {client360Data.client.reference_id}</p>
                    <p><strong>Email:</strong> {client360Data.client.email}</p>
                    <p><strong>Phone:</strong> {client360Data.client.phone}</p>
                    <p><strong>Type:</strong> {client360Data.client.client_type}</p>
                  </div>
                  <div style={{ flex: 1, backgroundColor: '#f8fafc', padding: '15px', borderRadius: '6px' }}>
                    <h3 style={{ margin: '0 0 10px 0', fontSize: '1.1rem' }}>Stats</h3>
                    <p><strong>Total Leads:</strong> {client360Data.leads.length}</p>
                    <p><strong>Total Tickets:</strong> {client360Data.tickets.length}</p>
                    <p><strong>Total Callbacks:</strong> {client360Data.callbacks.length}</p>
                  </div>
                </div>

                <div>
                  <h3 style={{ borderBottom: '1px solid #e2e8f0', paddingBottom: '8px' }}>Interaction Timeline</h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '15px', marginTop: '10px' }}>
                    {(() => {
                      const timeline = [
                        ...client360Data.tickets.map(t => ({ ...t, type: 'Ticket', date: new Date(t.created_at) })),
                        ...client360Data.callbacks.map(c => ({ ...c, type: 'Callback', date: new Date(c.created_at) })),
                        ...client360Data.chat_history.map(ch => ({ ...ch, type: 'Chat', date: new Date(ch.timestamp || new Date()) })),
                        ...(client360Data.call_logs || []).map(cl => ({ ...cl, type: 'Call', date: new Date(cl.time || new Date()) }))
                      ].sort((a, b) => b.date - a.date);

                      return timeline.length > 0 ? timeline.map((item, i) => (
                        <div key={i} style={{ borderLeft: '3px solid #184e7f', paddingLeft: '15px', backgroundColor: '#f8fafc', padding: '15px', borderRadius: '6px' }}>
                          <div style={{ fontSize: '0.85rem', color: '#64748b', marginBottom: '5px' }}>
                            <strong>{item.type}</strong> • {item.date.toLocaleString()}
                          </div>
                          
                          {item.type === 'Ticket' && (
                            <div>
                              <strong>Ticket ID: {item.ticket_id}</strong> - {item.category}
                              <span className={`badge ${item.status?.toLowerCase().replace(' ', '-')}`} style={{ marginLeft: '10px' }}>{item.status}</span>
                            </div>
                          )}
                          
                          {item.type === 'Callback' && (
                            <div>
                              <strong>Callback for: {item.topic}</strong>
                              <span className="badge" style={{ marginLeft: '10px' }}>{item.status}</span>
                            </div>
                          )}
                          
                          {item.type === 'Chat' && (
                            <div>
                              <div style={{ fontWeight: 'bold' }}>Chat Interaction</div>
                              <div style={{ marginTop: '5px' }}>
                                <span style={{ color: '#184e7f', fontWeight: '500' }}>User:</span> {item.question}
                              </div>
                              <div style={{ cursor: 'pointer', color: '#184e7f', fontSize: '0.9rem', marginTop: '5px' }} onClick={() => setExpandedChats({...expandedChats, [i]: !expandedChats[i]})}>
                                {expandedChats[i] ? 'Hide Bot Reply' : 'Show Bot Reply'}
                              </div>
                              {expandedChats[i] && (
                                <div style={{ marginTop: '5px', color: '#334155' }}>
                                  <span style={{ fontWeight: '500' }}>Bot:</span> {item.answer}
                                </div>
                              )}
                            </div>
                          )}
                          
                          {item.type === 'Call' && (
                            <div>
                              <div style={{ fontWeight: 'bold' }}>Call Log: {item.status}</div>
                              <div><strong>Outcome:</strong> {item.outcome}</div>
                              <div><strong>Duration:</strong> {item.duration || 0}s</div>
                              {item.summary && <div style={{ fontStyle: 'italic', marginTop: '5px' }}>"{item.summary}"</div>}
                              {item.recording_url && (
                                <button style={{ marginTop: '10px', padding: '4px 8px', fontSize: '0.8rem', backgroundColor: '#e2e8f0', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
                                  ▶ Play Recording
                                </button>
                              )}
                            </div>
                          )}
                        </div>
                      )) : <p>No interactions recorded.</p>;
                    })()}
                  </div>
                </div>
              </div>
            ) : (
              <div>Failed to load data.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default ClientsContacts;
