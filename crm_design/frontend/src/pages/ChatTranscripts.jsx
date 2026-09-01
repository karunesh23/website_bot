import { useState, useEffect } from 'react';
import '../index.css';

function ChatTranscripts() {
  const [transcripts, setTranscripts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedSummaries, setExpandedSummaries] = useState({});
  const [expandedTranscriptId, setExpandedTranscriptId] = useState(null);
  const [expandedSessionId, setExpandedSessionId] = useState(null);
  const [selectedChat, setSelectedChat] = useState(null);

  const toggleSummary = (id) => {
    setExpandedSummaries(prev => ({ ...prev, [id]: !prev[id] }));
  };

  useEffect(() => {
    fetch('http://localhost:8000/api/crm/chat-transcripts')
      .then(res => res.json())
      .then(data => {
        if (Array.isArray(data)) {
          setTranscripts(data);
        } else {
          console.error('API returned non-array:', data);
          setTranscripts([]);
        }
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching chat transcripts:', err);
        setLoading(false);
      });
  }, []);

  const headerStyle = { backgroundColor: '#184e7f', color: 'white', borderBottom: 'none', padding: '16px 20px', textTransform: 'uppercase', fontSize: '0.85rem' };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2 style={{ color: '#184e7f', fontSize: '1.25rem', margin: 0 }}>Chat Transcripts</h2>
      </div>

      <div className="table-container" style={{ padding: '16px', backgroundColor: 'white' }}>
        {loading ? (
            <div style={{ padding: '2rem', textAlign: 'center' }}>Loading chat transcripts...</div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: 0 }}>
                <thead>
                  <tr>
                    <th style={{ ...headerStyle, borderTopLeftRadius: '8px' }}>Transcript ID</th>
                    <th style={{ ...headerStyle }}>Session ID</th>
                    <th style={{ ...headerStyle }}>Related ID</th>
                    <th style={{ ...headerStyle }}>Channel</th>
                    <th style={{ ...headerStyle }}>Started At</th>
                    <th style={{ ...headerStyle }}>Ended At</th>
                    <th style={{ ...headerStyle, borderTopRightRadius: '8px' }}>Summary</th>
                  </tr>
                </thead>
                <tbody>
                  {transcripts.map((t, idx) => (
                    <tr key={idx}>
                      <td>
                        <div 
                          onClick={() => setExpandedTranscriptId(expandedTranscriptId === t.transcript_id ? null : t.transcript_id)}
                          style={{ 
                            maxWidth: expandedTranscriptId === t.transcript_id ? '300px' : '100px', 
                            overflow: expandedTranscriptId === t.transcript_id ? 'visible' : 'hidden', 
                            textOverflow: expandedTranscriptId === t.transcript_id ? 'clip' : 'ellipsis', 
                            whiteSpace: expandedTranscriptId === t.transcript_id ? 'normal' : 'nowrap',
                            wordBreak: 'break-all',
                            cursor: 'pointer'
                          }} 
                          title={t.transcript_id}
                        >
                          {t.transcript_id || '-'}
                        </div>
                      </td>
                      <td>
                        <div 
                          onClick={() => setExpandedSessionId(expandedSessionId === t.transcript_id ? null : t.transcript_id)}
                          style={{ 
                            maxWidth: expandedSessionId === t.transcript_id ? '300px' : '100px', 
                            overflow: expandedSessionId === t.transcript_id ? 'visible' : 'hidden', 
                            textOverflow: expandedSessionId === t.transcript_id ? 'clip' : 'ellipsis', 
                            whiteSpace: expandedSessionId === t.transcript_id ? 'normal' : 'nowrap',
                            wordBreak: 'break-all',
                            cursor: 'pointer'
                          }} 
                          title={t.session_id}
                        >
                          {t.session_id || '-'}
                        </div>
                      </td>
                      <td>{t.related_id}</td>
                      <td>{t.channel}</td>
                      <td style={{ whiteSpace: 'nowrap' }}>{t.started_at ? new Date(t.started_at).toLocaleString() : '-'}</td>
                      <td style={{ whiteSpace: 'nowrap' }}>{t.ended_at ? new Date(t.ended_at).toLocaleString() : '-'}</td>
                      <td>
                         <button 
                            style={{ padding: '6px 12px', backgroundColor: '#f0f4f8', color: '#184e7f', border: '1px solid #184e7f', borderRadius: '4px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: '500' }}
                            onClick={() => setSelectedChat(t)}
                          >
                            View Chat
                          </button>
                      </td>
                    </tr>
                  ))}
                  {transcripts.length === 0 && (
                    <tr>
                      <td colSpan="7" style={{ textAlign: 'center', padding: '2rem' }}>
                        No chat transcripts found.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
        
        {/* Chat View Modal */}
        {selectedChat && (
          <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1000 }}>
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', width: '80%', maxWidth: '700px', maxHeight: '85vh', display: 'flex', flexDirection: 'column' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid #eee', paddingBottom: '12px' }}>
                <h3 style={{ margin: 0, color: '#184e7f' }}>Chat Transcript: {selectedChat.session_id}</h3>
                <button onClick={() => setSelectedChat(null)} style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: '#666' }}>&times;</button>
              </div>
              <div style={{ overflowY: 'auto', flex: 1, display: 'flex', flexDirection: 'column', gap: '12px', paddingRight: '8px' }}>
                {Array.isArray(selectedChat.transcript) && selectedChat.transcript.length > 0 ? (
                  selectedChat.transcript.map((msg, i) => (
                    <div key={i} style={{ 
                      padding: '12px', 
                      borderRadius: '8px', 
                      backgroundColor: msg.role === 'user' ? '#f0f7ff' : '#f8f9fa', 
                      alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start', 
                      maxWidth: '85%',
                      border: msg.role === 'user' ? '1px solid #cce5ff' : '1px solid #e9ecef'
                    }}>
                      <div style={{ fontSize: '0.75rem', color: '#6c757d', marginBottom: '6px', fontWeight: 'bold' }}>
                        {msg.role === 'user' ? 'User' : 'Assistant'} {msg.time && <span style={{fontWeight: 'normal'}}>• {new Date(msg.time).toLocaleTimeString()}</span>}
                      </div>
                      <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.95rem', color: '#333' }}>{msg.content}</div>
                    </div>
                  ))
                ) : (
                  <div style={{ padding: '20px', textAlign: 'center', color: '#666' }}>No transcript data available.</div>
                )}
              </div>
            </div>
          </div>
        )}
    </div>
  );
}

export default ChatTranscripts;
