import { useState, useEffect } from 'react';
import '../index.css';

function TeamEscalations() {
  const [team, setTeam] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingMember, setEditingMember] = useState(null);
  const [dateRange, setDateRange] = useState('month');

  const fetchTeam = () => {
    setLoading(true);
    fetch(`http://localhost:8000/api/crm/team?range=${dateRange}`)
      .then(res => res.json())
      .then(data => {
        setTeam(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching team:', err);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchTeam();
  }, [dateRange]);

  const handleEditSave = () => {
    fetch(`http://localhost:8000/api/crm/team/${editingMember.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(editingMember)
    }).then(() => {
        setEditingMember(null);
        fetchTeam();
    });
  };

  const headerStyle = { backgroundColor: '#184e7f', color: 'white', borderBottom: 'none', padding: '16px 20px', textTransform: 'uppercase', fontSize: '0.85rem' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ color: '#184e7f', fontSize: '1.25rem', margin: 0 }}>Team & Escalations</h2>
        <select 
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value)}
          style={{ padding: '8px 12px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
        >
          <option value="today">Today</option>
          <option value="week">This Week</option>
          <option value="month">This Month</option>
        </select>
      </div>

      <div className="table-container" style={{ padding: '16px', backgroundColor: 'white' }}>
        {loading ? (
            <div style={{ padding: '2rem', textAlign: 'center' }}>Loading team members...</div>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: 0 }}>
              <thead>
                <tr>
                  <th style={{ ...headerStyle, borderTopLeftRadius: '8px' }}>Team Member</th>
                  <th style={{ ...headerStyle }}>Role</th>
                  <th style={{ ...headerStyle }}>Service Desk</th>
                  <th style={{ ...headerStyle }}>Escalation Level</th>
                  <th style={{ ...headerStyle }}>Calls Received</th>
                  <th style={{ ...headerStyle }}>Calls Picked</th>
                  <th style={{ ...headerStyle }}>Pickup Rate</th>
                  <th style={{ ...headerStyle }}>Avg Time to Pick</th>
                  <th style={{ ...headerStyle }}>Escalated</th>
                  <th style={{ ...headerStyle }}>Status</th>
                  <th style={{ ...headerStyle, borderTopRightRadius: '8px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {team.map((member, idx) => (
                  <tr key={idx}>
                    <td>
                      <div className="font-medium">{member.name}</div>
                      <div className="text-xs text-secondary">TM-{member.id}</div>
                    </td>
                    <td>{member.role || 'N/A'}</td>
                    <td>{member.service_desk || 'IT Support'}</td>
                    <td>
                      <span className={`status-badge ${member.escalation_level === 'Level 1' ? 'status-resolved' : 'status-open'}`}>
                        {member.escalation_level || 'N/A'}
                      </span>
                    </td>
                    <td>{member.calls_received || 0}</td>
                    <td>{member.calls_picked || 0}</td>
                    <td style={{ minWidth: '150px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        <span>{member.pickup_rate}</span>
                        <div style={{ flex: 1, height: '8px', backgroundColor: '#e2e8f0', borderRadius: '4px', overflow: 'hidden' }}>
                          <div style={{ 
                            height: '100%', 
                            width: member.pickup_rate, 
                            backgroundColor: parseInt(member.pickup_rate) === 100 ? '#22c55e' : (parseInt(member.pickup_rate) > 0 ? '#f97316' : '#94a3b8')
                          }}></div>
                        </div>
                      </div>
                    </td>
                    <td>{member.avg_time_to_pick || '0s'}</td>
                    <td>{member.escalated_count || 0}</td>
                    <td><span className={`status-badge ${member.is_active ? 'status-new' : 'status-open'}`}>{member.is_active ? 'Active' : 'Inactive'}</span></td>
                    <td>
                      <button onClick={() => setEditingMember(member)} style={{ padding: '4px 8px', cursor: 'pointer', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '4px' }}>
                        Configure
                      </button>
                    </td>
                  </tr>
                ))}
                {team.length === 0 && (
                  <tr>
                    <td colSpan="8" style={{ textAlign: 'center', padding: '2rem' }}>
                      No team members found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>

      {editingMember && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', width: '400px', maxWidth: '90%' }}>
            <h2 style={{ margin: '0 0 20px 0', color: '#184e7f' }}>Configure Escalation Chain</h2>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Role</label>
                <input 
                  type="text" 
                  value={editingMember.role || ''} 
                  onChange={(e) => setEditingMember({...editingMember, role: e.target.value})} 
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Service Desk</label>
                <input 
                  type="text" 
                  value={editingMember.service_desk || ''} 
                  onChange={(e) => setEditingMember({...editingMember, service_desk: e.target.value})} 
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Escalation Level</label>
                <select 
                  value={editingMember.escalation_level || ''} 
                  onChange={(e) => setEditingMember({...editingMember, escalation_level: e.target.value})} 
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                >
                  <option value="Level 1">Level 1</option>
                  <option value="Level 2">Level 2</option>
                  <option value="Level 3">Level 3</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontWeight: 'bold' }}>
                  <input 
                    type="checkbox" 
                    checked={editingMember.is_active} 
                    onChange={(e) => setEditingMember({...editingMember, is_active: e.target.checked})} 
                  />
                  Active
                </label>
              </div>
            </div>
            
            <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button onClick={() => setEditingMember(null)} style={{ padding: '8px 16px', borderRadius: '4px', border: '1px solid #cbd5e1', backgroundColor: 'white', cursor: 'pointer' }}>Cancel</button>
              <button onClick={handleEditSave} style={{ padding: '8px 16px', borderRadius: '4px', border: 'none', backgroundColor: '#184e7f', color: 'white', cursor: 'pointer' }}>Save Changes</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default TeamEscalations;
