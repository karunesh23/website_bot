import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import ClientsContacts from './pages/ClientsContacts';
import Leads from './pages/Leads';
import Tickets from './pages/Tickets';
import Callbacks from './pages/Callbacks';
import TeamEscalations from './pages/TeamEscalations';
import TeamMembers from './pages/TeamMembers';
import CallLogs from './pages/CallLogs';
import ChatTranscripts from './pages/ChatTranscripts';
import Login from './pages/Login';
import './index.css';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      {isLoggedIn ? (
        <div className="app-container">
          <Sidebar />
          <div className="main-content">
            <Header onLogout={() => setIsLoggedIn(false)} />
            <div className="page-container">
              <Routes>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/clients" element={<ClientsContacts />} />
                <Route path="/leads" element={<Leads />} />
                <Route path="/tickets" element={<Tickets />} />
                <Route path="/callbacks" element={<Callbacks />} />
                <Route path="/team" element={<TeamEscalations />} />
                <Route path="/team-members" element={<TeamMembers />} />
                <Route path="/call-logs" element={<CallLogs />} />
                <Route path="/chat-transcripts" element={<ChatTranscripts />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </div>
          </div>
        </div>
      ) : (
        <Routes>
          <Route path="/login" element={<Login onLogin={() => setIsLoggedIn(true)} />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      )}
    </Router>
  );
}

export default App;
