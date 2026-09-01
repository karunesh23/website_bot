import { useState, useEffect } from 'react';
import '../index.css';

function TeamMembers() {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [editingMember, setEditingMember] = useState(null);
  const [isAdding, setIsAdding] = useState(false);
  const [formData, setFormData] = useState({
    member_id: '',
    name: '',
    role: 'Service Engineer',
    service_desk: '',
    escalation_level: 1,
    active: true
  });

  const handleSave = () => {
    if (isAdding) {
      setMembers([...members, formData]);
    } else {
      setMembers(members.map(m => m.member_id === formData.member_id ? formData : m));
    }
    setIsAdding(false);
    setEditingMember(null);
  };

  const openEdit = (member) => {
    setFormData(member);
    setEditingMember(member);
    setIsAdding(false);
  };

  const openAdd = () => {
    setFormData({
      member_id: '',
      name: '',
      role: 'Service Engineer',
      service_desk: '',
      escalation_level: 1,
      active: true
    });
    setIsAdding(true);
    setEditingMember(null);
  };

  const headerStyle = { backgroundColor: '#184e7f', color: 'white', borderBottom: 'none', padding: '16px 20px', textTransform: 'uppercase', fontSize: '0.85rem' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ color: '#184e7f', fontSize: '1.25rem', margin: 0 }}>Team Members</h2>
        <button 
          onClick={openAdd}
          style={{ backgroundColor: '#184e7f', color: 'white', padding: '8px 16px', borderRadius: '4px', border: 'none', cursor: 'pointer' }}
        >
          + Add Member
        </button>
      </div>

      <div className="table-container" style={{ padding: '16px', backgroundColor: 'white', borderRadius: '8px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
        {loading && members.length === 0 ? (
            <div style={{ padding: '2rem', textAlign: 'center' }}>Loading team members...</div>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: 0 }}>
              <thead>
                <tr>
                  <th style={{ ...headerStyle, borderTopLeftRadius: '8px' }}>Member ID</th>
                  <th style={{ ...headerStyle }}>Name</th>
                  <th style={{ ...headerStyle }}>Role</th>
                  <th style={{ ...headerStyle }}>Service Desk</th>
                  <th style={{ ...headerStyle }}>Escalation Level</th>
                  <th style={{ ...headerStyle }}>Status</th>
                  <th style={{ ...headerStyle, borderTopRightRadius: '8px' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {members.map((member, idx) => (
                  <tr key={idx}>
                    <td>{member.member_id}</td>
                    <td className="font-medium">{member.name}</td>
                    <td>{member.role}</td>
                    <td>{member.service_desk || '-'}</td>
                    <td>{member.escalation_level}</td>
                    <td>
                      <span className={`status-badge ${member.active ? 'status-new' : 'status-open'}`}>
                        {member.active ? 'Active' : 'Inactive'}
                      </span>
                    </td>
                    <td>
                      <button onClick={() => openEdit(member)} style={{ padding: '4px 8px', cursor: 'pointer', backgroundColor: '#f1f5f9', border: '1px solid #cbd5e1', borderRadius: '4px' }}>
                        Edit
                      </button>
                    </td>
                  </tr>
                ))}
                {members.length === 0 && (
                  <tr>
                    <td colSpan="7" style={{ textAlign: 'center', padding: '2rem' }}>
                      No team members found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>

      {(isAdding || editingMember) && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', width: '400px', maxWidth: '90%' }}>
            <h2 style={{ margin: '0 0 20px 0', color: '#184e7f' }}>{isAdding ? 'Add Team Member' : 'Edit Team Member'}</h2>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Member ID *</label>
                <input 
                  type="text" 
                  value={formData.member_id} 
                  onChange={(e) => setFormData({...formData, member_id: e.target.value})} 
                  disabled={!isAdding}
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1', backgroundColor: !isAdding ? '#f1f5f9' : 'white' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Name *</label>
                <input 
                  type="text" 
                  value={formData.name} 
                  onChange={(e) => setFormData({...formData, name: e.target.value})} 
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Role *</label>
                <select 
                  value={formData.role} 
                  onChange={(e) => setFormData({...formData, role: e.target.value})} 
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                >
                  <option value="Director">Director</option>
                  <option value="Service Head">Service Head</option>
                  <option value="Service Engineer">Service Engineer</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Service Desk</label>
                <input 
                  type="text" 
                  value={formData.service_desk} 
                  onChange={(e) => setFormData({...formData, service_desk: e.target.value})} 
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>Escalation Level *</label>
                <input 
                  type="number"
                  min="1"
                  value={formData.escalation_level} 
                  onChange={(e) => setFormData({...formData, escalation_level: parseInt(e.target.value) || 1})} 
                  style={{ width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #cbd5e1' }}
                />
              </div>
              <div>
                <label style={{ display: 'flex', alignItems: 'center', gap: '10px', fontWeight: 'bold' }}>
                  <input 
                    type="checkbox" 
                    checked={formData.active} 
                    onChange={(e) => setFormData({...formData, active: e.target.checked})} 
                  />
                  Active
                </label>
              </div>
            </div>
            
            <div style={{ marginTop: '20px', display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
              <button onClick={() => { setIsAdding(false); setEditingMember(null); }} style={{ padding: '8px 16px', borderRadius: '4px', border: '1px solid #cbd5e1', backgroundColor: 'white', cursor: 'pointer' }}>Cancel</button>
              <button onClick={handleSave} style={{ padding: '8px 16px', borderRadius: '4px', border: 'none', backgroundColor: '#184e7f', color: 'white', cursor: 'pointer' }}>Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default TeamMembers;
