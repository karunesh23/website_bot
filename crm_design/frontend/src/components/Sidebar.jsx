import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Users, Ticket, PhoneOutgoing, PhoneForwarded, ShieldAlert, MessageSquare } from 'lucide-react';
import itcLogo from '../assets/site_logo_03-1.png (1).webp';
import evokeLogo from '../assets/evoke.webp';

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-header" style={{ height: '70px', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: 'var(--primary-color)', padding: 0, margin: 0, borderBottom: 'none', overflow: 'hidden' }}>
        <img src={itcLogo} alt="ITC India Logo" style={{ height: '75%', width: 'auto', objectFit: 'contain', filter: 'brightness(0) invert(1)', transform: 'scale(1.1)' }} />
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/dashboard" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </NavLink>
        <NavLink to="/clients" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          <Users size={20} />
          <span>Clients & Contacts</span>
        </NavLink>
        <NavLink to="/leads" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          <PhoneOutgoing size={20} />
          <span>Leads</span>
        </NavLink>
        <NavLink to="/tickets" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          <Ticket size={20} />
          <span>Tickets</span>
        </NavLink>
        <NavLink to="/callbacks" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          <PhoneForwarded size={20} />
          <span>Callbacks</span>
        </NavLink>
        <NavLink to="/team-members" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          <Users size={20} />
          <span>Team Members</span>
        </NavLink>

        <NavLink to="/call-logs" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          <PhoneForwarded size={20} />
          <span>Call Logs</span>
        </NavLink>
        <NavLink to="/chat-transcripts" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
          <MessageSquare size={20} />
          <span>Chat Transcripts</span>
        </NavLink>
      </nav>

      <div className="sidebar-footer" style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        <a href="https://evokeaisolutions.com/" target="_blank" rel="noopener noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '12px', textDecoration: 'none', color: '#cbd5e1', fontSize: '0.95rem', fontWeight: '500', transition: 'color 0.2s' }} onMouseOver={(e) => e.currentTarget.style.color = 'white'} onMouseOut={(e) => e.currentTarget.style.color = '#cbd5e1'}>
          <img src={evokeLogo} alt="Evoke AI Logo" style={{ width: '36px', height: '36px', objectFit: 'contain', borderRadius: '6px' }} />
          <span>Powered by Evoke AI</span>
        </a>
      </div>
    </aside>
  );
}

export default Sidebar;