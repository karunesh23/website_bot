import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Eye, EyeOff } from 'lucide-react';
import itcLogo from '../assets/site_logo_03-1.png (1).webp';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (username === 'admin' && password === 'ITC_INDIA_2026') {
      onLogin();
      navigate('/dashboard');
    } else {
      alert('Invalid credentials. Please try again.');
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      width: '100vw',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#184e7f',
      fontFamily: "'Inter', sans-serif",
      margin: 0,
      padding: 0,
      position: 'absolute',
      top: 0,
      left: 0
    }}>
      <div style={{
        backgroundColor: 'white',
        padding: '40px',
        borderRadius: '8px',
        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
        width: '100%',
        maxWidth: '420px',
        textAlign: 'center'
      }}>
        {/* ITC Logo */}
        <div style={{ marginBottom: '24px', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <img src={itcLogo} alt="ITC India Logo" style={{ height: '110px', width: 'auto', objectFit: 'contain' }} />
          <div style={{ marginTop: '16px', color: '#184e7f', fontSize: '1.1rem', fontWeight: '600', textAlign: 'center' }}>
            Priya (ITC INDIA AI Compliance Companion Bot)
          </div>
        </div>

        <h2 style={{ color: '#184e7f', fontSize: '1.35rem', marginBottom: '8px', fontWeight: '700' }}>Admin Login</h2>
        <p style={{ color: '#64748b', fontSize: '0.875rem', marginBottom: '32px' }}>
          Please enter your credentials to access the CRM.
        </p>

        <form onSubmit={handleLogin} style={{ textAlign: 'left' }} autoComplete="off">
          <div style={{ marginBottom: '16px' }}>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: '#0f172a', marginBottom: '6px' }}>
              Username
            </label>
            <input 
              type="text" 
              name="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="off"
              required
              style={{
                width: '100%',
                padding: '12px 14px',
                borderRadius: '6px',
                border: '1px solid #cbd5e1',
                backgroundColor: '#f8fafc',
                outline: 'none',
                color: '#334155',
                fontSize: '0.95rem'
              }}
            />
          </div>

          <div style={{ marginBottom: '28px' }}>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '600', color: '#0f172a', marginBottom: '6px' }}>
              Password
            </label>
            <div style={{ position: 'relative' }}>
              <input 
                type={showPassword ? "text" : "password"} 
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="new-password"
                required
                style={{
                  width: '100%',
                  padding: '12px 14px',
                  paddingRight: '40px',
                  borderRadius: '6px',
                  border: '1px solid #cbd5e1',
                  backgroundColor: '#f8fafc',
                  outline: 'none',
                  color: '#334155',
                  fontSize: '0.95rem'
                }}
              />
              <div 
                style={{ position: 'absolute', right: '14px', top: '12px', color: '#94a3b8', cursor: 'pointer' }}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </div>
            </div>
          </div>

          <button 
            type="submit"
            style={{
              width: '100%',
              backgroundColor: '#184e7f',
              color: 'white',
              border: 'none',
              padding: '14px',
              borderRadius: '6px',
              fontWeight: '600',
              fontSize: '1rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '10px',
              cursor: 'pointer',
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#154168'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#184e7f'}
          >
            <Lock size={18} />
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
