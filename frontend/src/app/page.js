'use client';
import { useState, useEffect } from 'react';

export default function Home() {
  const [clientName, setClientName] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [databaseLogs, setDatabaseLogs] = useState([]);

  // This reads the secret phone number address you set up in your .env file
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  // 1. Check if the backend pipe is working as soon as the page opens
  useEffect(() => {
    fetch(`${API_URL}/api/`)
      .then(res => res.json())
      .then(data => console.log("Backend says:", data.message))
      .catch(err => console.error("Pipes are blocked:", err));
    
    fetchLeads();
  }, []);

  // 2. Pull the saved customer entries from the database
  const fetchLeads = async () => {
    try {
      const res = await fetch(`${API_URL}/api/status`);
      const data = await res.json();
      setDatabaseLogs(data);
    } catch (err) {
      console.error("Couldn't read database:", err);
    }
  };

  // 3. Send a new name down the pipe when the customer clicks submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!clientName.trim()) return;

    setStatusMessage('Sending to database...');
    try {
      const res = await fetch(`${API_URL}/api/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_name: clientName })
      });

      if (res.ok) {
        setStatusMessage('Success! Lead saved in MongoDB.');
        setClientName('');
        fetchLeads(); // Automatically refreshes the list below
      } else {
        setStatusMessage('Backend rejected it.');
      }
    } catch (err) {
      setStatusMessage('Pipe broken. Is the backend server running?');
    }
  };

  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif', maxWidth: '600px', margin: '0 auto', color: '#333' }}>
      <header style={{ marginBottom: '2rem', textAlign: 'center' }}>
        <h1>Safety First Solar LLC</h1>
        <p>Europe-Northamerica Network Foundation</p>
      </header>

      {/* THE LEAD INPUT FORM */}
      <section style={{ background: '#f5f5f5', padding: '1.5rem', borderRadius: '8px', marginBottom: '2rem', border: '1px solid #eee' }}>
        <h3 style={{ marginTop: 0 }}>Inquiry Registration Form</h3>
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <input 
            type="text" 
            placeholder="Enter Client Name..." 
            value={clientName}
            onChange={(e) => setClientName(e.target.value)}
            style={{ padding: '0.5rem', fontSize: '1rem', borderRadius: '4px', border: '1px solid #ccc' }}
          />
          <button type="submit" style={{ padding: '0.6rem', background: '#0070f3', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold' }}>
            Submit Lead to Database
          </button>
        </form>
        {statusMessage && <p style={{ marginTop: '1rem', fontWeight: 'bold', color: '#0070f3' }}>{statusMessage}</p>}
      </section>

      {/* THE LIVE STREAM DISPLAY */}
      <section>
        <h3>Live Database Feed</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {databaseLogs.length === 0 ? (
            <p style={{ color: '#666', fontStyle: 'italic' }}>No entries found. Submit a name above to test the network connection.</p>
          ) : (
            databaseLogs.map((log, index) => (
              <div key={index} style={{ border: '1px solid #ddd', padding: '0.5rem', borderRadius: '4px', background: '#fff' }}>
                <strong>{log.client_name}</strong>
                <div style={{ fontSize: '0.8rem', color: '#888' }}>ID: {log.id}</div>
              </div>
            ))
          )}
        </div>
      </section>
    </main>
  );
}
