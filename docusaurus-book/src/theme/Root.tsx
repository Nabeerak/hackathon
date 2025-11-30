import React from 'react';
import Chatbot from '../../frontend/src/components/Chatbot';

export default function Root({ children }) {
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}
