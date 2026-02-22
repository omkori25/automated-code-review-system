// FileUploader.tsx
import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface FileUploaderProps {
  onFilesUploaded: (files: any[]) => void;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onFilesUploaded }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const files = acceptedFiles.map(file => ({
      path: file.name,
      content: file,
      language: file.name.split('.').pop() || 'text',
      size: file.size
    }));
    onFilesUploaded(files);
  }, [onFilesUploaded]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/x-python': ['.py'],
      'application/javascript': ['.js', '.jsx'],
      'application/typescript': ['.ts', '.tsx'],
      'text/x-java': ['.java']
    }
  });

  return (
    <div 
      {...getRootProps()} 
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
        ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300 hover:border-gray-400'}`}
    >
      <input {...getInputProps()} />
      {isDragActive ? (
        <p className="text-blue-600">Drop the files here...</p>
      ) : (
        <div>
          <p className="text-gray-600 mb-2">Drag & drop files here, or click to select</p>
          <p className="text-sm text-gray-500">Supported: .py, .js, .jsx, .ts, .tsx, .java</p>
        </div>
      )}
    </div>
  );
};

export default FileUploader;