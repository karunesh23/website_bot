import { useLocation } from 'react-router-dom';
import { LogOut } from 'lucide-react';

function Header({ onLogout }) {
  const location = useLocation();
  
  const getPageTitle = () => {
    switch(location.pathname) {
      case '/dashboard': return 'Dashboard';
      case '/clients': return 'Clients & Contacts';
      case '/leads': return 'Leads';
      case '/tickets': return 'Tickets';
      case '/callbacks': return 'Callbacks';
      case '/team': return 'Team & Escalations';
      default: return 'CRM';
    }
  };

  return (
    <header className="top-header">
      <div className="header-title">
        {getPageTitle()}
      </div>
      <div className="user-profile">
        <button 
          onClick={onLogout}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            backgroundColor: '#184e7f',
            border: '1px solid #184e7f',
            color: 'white',
            fontWeight: '600',
            cursor: 'pointer',
            padding: '8px 16px',
            borderRadius: '6px',
            transition: 'all 0.2s',
            fontSize: '0.9rem'
          }}
          onMouseOver={(e) => {
            e.currentTarget.style.backgroundColor = '#154168';
          }}
          onMouseOut={(e) => {
            e.currentTarget.style.backgroundColor = '#184e7f';
          }}
        >
          <LogOut size={16} />
          Logout
        </button>
      </div>
    </header>
  );
}

export default Header;
