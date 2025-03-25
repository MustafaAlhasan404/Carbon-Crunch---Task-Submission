import React, { useEffect, useRef } from 'react';
import './ResultsDisplay.css';

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

interface ResultsDisplayProps {
  results: AnalysisResult;
}

const ResultsDisplay = ({ results }: ResultsDisplayProps) => {
  const { overall_score, breakdown, recommendations } = results;
  const scoreRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    // Set the CSS variable for the score percentage
    if (scoreRef.current) {
      scoreRef.current.style.setProperty('--score-percentage', overall_score.toString());
      
      // Add typing animation class to trigger animations on first load
      setTimeout(() => {
        document.querySelectorAll('.score-bar').forEach(bar => {
          bar.classList.add('animated');
        });
      }, 300);
    }
  }, [overall_score]);
  
  // Determine score color
  const getScoreColor = (score: number): string => {
    if (score >= 80) return 'var(--success-color)'; // Green
    if (score >= 60) return 'var(--warning-color)'; // Orange
    return 'var(--danger-color)'; // Red
  };
  
  // Get category label
  const getCategoryLabel = (key: string): string => {
    const labels: Record<string, string> = {
      naming: 'Naming Conventions',
      modularity: 'Function Length & Modularity',
      comments: 'Comments & Documentation',
      formatting: 'Formatting & Indentation',
      reusability: 'Reusability & DRY',
      best_practices: 'Best Practices'
    };
    
    return labels[key] || key;
  };
  
  // Get max possible score for each category
  const getMaxScore = (key: string): number => {
    const maxScores: Record<string, number> = {
      naming: 10,
      modularity: 20,
      comments: 20,
      formatting: 15,
      reusability: 15,
      best_practices: 20
    };
    
    return maxScores[key] || 0;
  };
  
  return (
    <div className="results-container">
      <h2>Analysis Results</h2>
      
      <div className="overall-score-container">
        <div 
          className="overall-score" 
          style={{ 
            backgroundColor: getScoreColor(overall_score),
            color: 'white'
          }}
          ref={scoreRef}
        >
          <span className="score-number">{overall_score}</span>
          <span className="score-label">Overall Score</span>
        </div>
      </div>
      
      <div className="breakdown-container">
        <h3>Score Breakdown</h3>
        
        <div className="categories">
          {Object.entries(breakdown).map(([category, score]: [string, number]) => (
            <div className="category" key={category}>
              <div className="category-header">
                <span className="category-name">{getCategoryLabel(category)}</span>
                <span className="category-score">
                  {score}/{getMaxScore(category)}
                </span>
              </div>
              
              <div className="score-bar-container">
                <div 
                  className="score-bar" 
                  style={{ 
                    width: `${(score / getMaxScore(category)) * 100}%`,
                    backgroundColor: getScoreColor((score / getMaxScore(category)) * 100)
                  }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
      
      <div className="recommendations-container">
        <h3>Recommendations</h3>
        
        {recommendations.length === 0 ? (
          <p className="no-recommendations">No recommendations. Your code looks great!</p>
        ) : (
          <ul className="recommendations-list">
            {recommendations.map((recommendation: string, index: number) => (
              <li key={index}>{recommendation}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default ResultsDisplay; 