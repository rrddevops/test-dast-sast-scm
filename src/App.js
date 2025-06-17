import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    setIsLoading(true);
    
    // Simulação de uma chamada de API
    setTimeout(() => {
      setMessage(`Olá, ${inputValue}! Bem-vindo ao projeto de teste com SAST, SCM e DAST.`);
      setIsLoading(false);
    }, 1000);
  };

  useEffect(() => {
    setMessage('Bem-vindo ao projeto de teste de segurança!');
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔒 Projeto de Teste de Segurança</h1>
        <p>SAST • SCM • DAST</p>
      </header>
      
      <main className="App-main">
        <div className="card">
          <h2>Teste de Funcionalidade</h2>
          <form onSubmit={handleSubmit} className="form">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Digite seu nome..."
              className="input"
              disabled={isLoading}
            />
            <button 
              type="submit" 
              className="button"
              disabled={isLoading || !inputValue.trim()}
            >
              {isLoading ? 'Processando...' : 'Enviar'}
            </button>
          </form>
          
          {message && (
            <div className="message">
              <p>{message}</p>
            </div>
          )}
        </div>

        <div className="security-info">
          <h3>🔍 Ferramentas de Segurança Implementadas:</h3>
          <ul>
            <li><strong>SAST:</strong> SonarCloud - Análise estática de código</li>
            <li><strong>SCM:</strong> Trivy - Segurança de containers</li>
            <li><strong>DAST:</strong> ZAP Proxy - Testes de segurança dinâmica</li>
          </ul>
        </div>
      </main>
    </div>
  );
}

export default App; 