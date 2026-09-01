import { useState, useEffect } from 'react';
import axios from 'axios';
import '../index.css';

function Leads() {
  const [leads, setLeads] = useState([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [serviceFilter, setServiceFilter] = useState('');
  const [selectedLead, setSelectedLead] = useState(null);

  useEffect(() => {
    fetchLeads();
  }, []);

  const fetchLeads = () => {
    axios.get('http://localhost:8000/api/crm/leads')
      .then(res => setLeads(res.data))
      .catch(err => console.error(err));
  };

  const filteredLeads = leads.filter(l => {
    if (statusFilter && l.lead_status !== statusFilter) return false;
    if (serviceFilter && l.service_interest !== serviceFilter) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      const matches = 
        String(l.lead_id).includes(q) ||
        l.reference_id?.toLowerCase().includes(q) ||
        l.service_interest?.toLowerCase().includes(q) ||
        l.product?.toLowerCase().includes(q);
      if (!matches) return false;
    }
    return true;
  });

  const headerStyle = { backgroundColor: '#184e7f', color: 'white', borderBottom: 'none', padding: '16px 20px' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ color: '#184e7f', fontSize: '1.25rem', margin: 0 }}>Leads</h2>
      </div>

      <div style={{ display: 'flex', gap: '15px' }}>
        <input 
          type="text" 
          placeholder="Search by ID, Service, or Product..."
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
          value={serviceFilter}
          onChange={(e) => setServiceFilter(e.target.value)}
          style={{
            padding: '12px 16px',
            borderRadius: '6px',
            border: '1px solid var(--border-color)',
            outline: 'none',
            fontSize: '0.9rem',
            backgroundColor: 'white'
          }}
        >
          <option value="">All Services</option>
          <option value="Electrical Safety Testing">Electrical Safety Testing</option>
          <option value="Environmental / IP Testing">Environmental / IP Testing</option>
          <option value="Electro-Medical Equipment">Electro-Medical Equipment</option>
          <option value="Photometry (LM-79/LM-80)">Photometry (LM-79/LM-80)</option>
          <option value="EMC/EMI Testing">EMC/EMI Testing</option>
          <option value="Software Testing">Software Testing</option>
          <option value="Information Security">Information Security</option>
          <option value="Calibration Services">Calibration Services</option>
          <option value="Packaging Testing">Packaging Testing</option>
        </select>
      </div>

      <div className="table-container" style={{ padding: '16px', backgroundColor: 'white' }}>
        <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: 0 }}>
          <thead>
            <tr>
              <th style={{ ...headerStyle, borderTopLeftRadius: '8px' }}>Lead ID</th>
              <th style={{ ...headerStyle }}>Reference ID</th>
              <th style={{ ...headerStyle }}>Service Interest</th>
              <th style={{ ...headerStyle }}>Product</th>
              <th style={{ ...headerStyle }}>Interest Details</th>
              <th style={{ ...headerStyle }}>Session ID</th>
              <th style={{ ...headerStyle }}>Lead Status</th>
              <th style={{ ...headerStyle, borderTopRightRadius: '8px' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredLeads.map((l, i) => (
              <tr key={i}>
                <td style={{ color: '#184e7f', fontWeight: '600' }}>L{l.lead_id}</td>
                <td>{l.reference_id}</td>
                <td>{l.service_interest}</td>
                <td>{l.product || '-'}</td>
                <td style={{ maxWidth: '200px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {l.interest_details || '-'}
                </td>
                <td style={{ maxWidth: '100px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  {l.session_id || '-'}
                </td>
                <td>
                  <span className={`badge ${l.lead_status?.toLowerCase().replace(' ', '-') || 'new'}`}>
                    {l.lead_status || 'New'}
                  </span>
                </td>
                <td>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button onClick={() => setSelectedLead(l)} style={{ padding: '6px 12px', cursor: 'pointer', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '4px' }}>
                      View
                    </button>
                    {(l.lead_status === 'Qualified' || l.lead_status === 'Contacted') && (
                      <button 
                        onClick={() => {
                          fetch(`http://localhost:8000/api/crm/leads/${l.lead_id}/convert`, { method: 'POST' })
                            .then(res => res.json())
                            .then(() => fetchLeads())
                            .catch(err => console.error(err));
                        }} 
                        style={{ padding: '6px 12px', cursor: 'pointer', backgroundColor: '#184e7f', color: 'white', border: 'none', borderRadius: '4px' }}
                      >
                        Convert
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {filteredLeads.length === 0 && (
              <tr><td colSpan="8" style={{ textAlign: 'center' }}>No leads found.</td></tr>
            )}
          </tbody>
        </table>
      </div>

      {selectedLead && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', width: '500px', maxWidth: '90%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ margin: 0, color: '#184e7f' }}>Lead Details: L{selectedLead.lead_id}</h2>
              <button onClick={() => setSelectedLead(null)} style={{ background: 'none', border: 'none', fontSize: '24px', cursor: 'pointer' }}>×</button>
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div>
                <strong>Reference ID:</strong> {selectedLead.reference_id}
              </div>
              <div>
                <strong>Service Interest:</strong> {selectedLead.service_interest}
              </div>
              <div>
                <strong>Product:</strong> {selectedLead.product || 'N/A'}
              </div>
              <div>
                <strong>Interest Details:</strong>
                <p style={{ margin: '5px 0', backgroundColor: '#f8fafc', padding: '10px', borderRadius: '4px' }}>
                  {selectedLead.interest_details || 'No details provided.'}
                </p>
              </div>
              <div>
                <strong>Session ID:</strong> {selectedLead.session_id || 'N/A'}
              </div>
            </div>
            <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button onClick={() => setSelectedLead(null)} style={{ padding: '8px 16px', borderRadius: '4px', border: 'none', backgroundColor: '#184e7f', color: 'white', cursor: 'pointer' }}>Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Leads;
