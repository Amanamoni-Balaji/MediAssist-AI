import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { DisclaimerBanner } from './components/DisclaimerBanner';

import { LandingPage } from './pages/LandingPage';
import { RegisterPage } from './pages/RegisterPage';
import { LoginPage } from './pages/LoginPage';
import { DashboardPage } from './pages/DashboardPage';
import { ChatbotPage } from './pages/ChatbotPage';
import { SymptomPage } from './pages/SymptomPage';
import { HistoryPage } from './pages/HistoryPage';
import { ProfilePage } from './pages/ProfilePage';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { AboutPage } from './pages/AboutPage';

const AppContent: React.FC = () => {
  const { isAuthenticated, loading } = useAuth();
  const urlPage = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('page') : null;
  const urlQuery = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('q') : null;
  const [currentPage, setCurrentPage] = useState<string>(urlPage || 'landing');
  const [pageParams, setPageParams] = useState<{ conversationId?: string; initialQuery?: string }>(
    urlQuery ? { initialQuery: urlQuery } : {}
  );

  const handleNavigate = (page: string, params?: { conversationId?: string; initialQuery?: string }) => {
    setCurrentPage(page);
    if (params) {
      setPageParams(params);
    } else {
      setPageParams({});
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleQuickChat = (query: string) => {
    handleNavigate('chat', { initialQuery: query });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <div className="text-center space-y-3">
          <div className="w-10 h-10 border-4 border-cyan-600 border-t-transparent rounded-full animate-spin mx-auto"></div>
          <p className="text-xs text-slate-500 font-medium">Initializing MediNLP Healthcare AI...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      <DisclaimerBanner />
      <Navbar currentPage={currentPage} onNavigate={handleNavigate} />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-4">
        {currentPage === 'landing' && (
          <LandingPage onNavigate={handleNavigate} onQuickChat={handleQuickChat} />
        )}
        {currentPage === 'register' && (
          <RegisterPage onNavigate={handleNavigate} />
        )}
        {currentPage === 'login' && (
          <LoginPage onNavigate={handleNavigate} />
        )}
        {currentPage === 'dashboard' && (
          <DashboardPage onNavigate={handleNavigate} onQuickChat={handleQuickChat} />
        )}
        {currentPage === 'chat' && (
          <ChatbotPage 
            key={pageParams.conversationId || pageParams.initialQuery || 'chat-page'}
            initialConversationId={pageParams.conversationId}
            initialQuery={pageParams.initialQuery}
            onNavigate={handleNavigate}
          />
        )}
        {currentPage === 'symptoms' && (
          <SymptomPage onNavigate={handleNavigate} onConsultBot={handleQuickChat} />
        )}
        {currentPage === 'history' && (
          <HistoryPage onNavigate={handleNavigate} />
        )}
        {currentPage === 'profile' && (
          <ProfilePage />
        )}
        {currentPage === 'admin' && (
          <AdminDashboardPage />
        )}
        {currentPage === 'about' && (
          <AboutPage />
        )}
      </main>

      <Footer onNavigate={handleNavigate} />
    </div>
  );
};

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
