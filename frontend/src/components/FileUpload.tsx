import React, { useState, useRef } from 'react';
import './FileUpload.css';

interface FileUploadProps {
  onUpload: (file: File) => Promise<void>;
  loading: boolean;
}

const FileUpload = ({ onUpload, loading }: FileUploadProps) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (selectedFile) {
      await onUpload(selectedFile);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    
    if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
      const file = event.dataTransfer.files[0];
      const extension = file.name.split('.').pop()?.toLowerCase();
      
      if (extension === 'js' || extension === 'jsx' || extension === 'py') {
        setSelectedFile(file);
      } else {
        alert('Please upload a .js, .jsx, or .py file.');
      }
    }
  };

  const handleBrowseClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="file-upload-container">
      <h2>Upload Code File</h2>
      <p className="file-upload-info">
        Drag and drop your JavaScript, React, or Python file here, or click to browse.
      </p>
      
      <form onSubmit={handleSubmit}>
        <div 
          className={`drop-area ${isDragging ? 'dragging' : ''} ${selectedFile ? 'has-file' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={handleBrowseClick}
        >
          <input 
            type="file" 
            onChange={handleFileChange} 
            accept=".js,.jsx,.py"
            ref={fileInputRef}
            style={{ display: 'none' }}
          />
          
          {selectedFile ? (
            <div className="file-info">
              <p className="file-name">{selectedFile.name}</p>
              <p className="file-size">{(selectedFile.size / 1024).toFixed(2)} KB</p>
            </div>
          ) : (
            <div className="upload-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="17 8 12 3 7 8"></polyline>
                <line x1="12" y1="3" x2="12" y2="15"></line>
              </svg>
              <p>Drag & drop or click to browse</p>
            </div>
          )}
        </div>
        
        <button 
          type="submit" 
          className="analyze-button"
          disabled={!selectedFile || loading}
        >
          {loading ? 'Analyzing...' : 'Analyze Code'}
        </button>
      </form>
    </div>
  );
};

export default FileUpload; 