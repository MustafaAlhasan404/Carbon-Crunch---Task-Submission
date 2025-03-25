import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import FileUpload from './components/FileUpload';
import ResultsDisplay from './components/ResultsDisplay';
import Logo from './components/Logo';

interface AnalysisResult {
  overall_score: number;
  breakdown: {
    naming: number;
    modularity: number;
    comments: number;
    formatting: number;
    reusability: number;
    best_practices: number;
  };
  recommendations: string[];
}

const App = () => {
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  
  const analyzeCode = async (file: File): Promise<void> => {
    setLoading(true);
    setError('');
    setResults(null);
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const response = await axios.post<AnalysisResult>('http://localhost:8000/analyze-code', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      
      setResults(response.data);
    } catch (err: any) {
      console.error('Error analyzing code:', err);
      setError(
        axios.isAxiosError(err) && err.response?.data?.error 
          ? err.response.data.error 
          : 'Failed to analyze code. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };
  
  const getCurrentYear = () => {
    return new Date().getFullYear();
  };
  
  return (
    <div className="App">
      <header className="App-header">
        <Logo />
        <p>Code Quality Analyzer for JavaScript and Python</p>
      </header>
      
      <main className="App-main">
        <FileUpload onUpload={analyzeCode} loading={loading} />
        
        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}
        
        {results && <ResultsDisplay results={results} />}
      </main>
      
      <footer className="App-footer">
        <p>Carbon Crunch &copy; {getCurrentYear()} | Analyze your code quality with confidence</p>
      </footer>
    </div>
  );
};

export default App; 