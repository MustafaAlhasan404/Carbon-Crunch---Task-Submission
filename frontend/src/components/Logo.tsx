import React from 'react';
import './Logo.css';

const Logo = () => {
  return (
    <div className="logo-container">
      <svg 
        className="logo" 
        width="100" 
        height="100" 
        viewBox="0 0 100 100" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle className="logo-circle" cx="50" cy="50" r="45" stroke="white" strokeWidth="2" />
        
        {/* Leaf shape */}
        <path 
          className="logo-leaf" 
          d="M65,35 C65,35 75,45 75,60 C75,75 60,80 50,70 C40,60 45,35 65,35 Z" 
          fill="white" 
        />
        
        {/* Stem */}
        <path 
          className="logo-stem" 
          d="M50,70 L50,80" 
          stroke="white" 
          strokeWidth="2" 
          strokeLinecap="round" 
        />
        
        {/* Code brackets */}
        <path 
          className="logo-bracket left" 
          d="M30,40 L20,50 L30,60" 
          stroke="white" 
          strokeWidth="2" 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          fill="none" 
        />
        
        <path 
          className="logo-bracket right" 
          d="M70,40 L80,50 L70,60" 
          stroke="white" 
          strokeWidth="2" 
          strokeLinecap="round" 
          strokeLinejoin="round" 
          fill="none" 
        />
      </svg>
      <div className="logo-text">
        <span className="logo-carbon">Carbon</span>
        <span className="logo-crunch">Crunch</span>
      </div>
    </div>
  );
};

export default Logo; 