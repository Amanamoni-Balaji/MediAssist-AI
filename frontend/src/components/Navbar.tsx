import React, { useState } from 'react';
import { 
  Activity, 
  MessageSquare, 
  Stethoscope, 
  History, 
  BarChart3, 
  Info, 
  User as UserIcon, 
  LogOut, 
  Menu, 
  X, 
  ShieldCheck,
  ChevronDown
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface NavbarProps {
  currentPage: string;
  onNavigate: (page: string) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ currentPage, onNavigate }) => {
  const { user, isAuthenticated, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userDropdownOpen, setUserDropdownOpen] = useState(false);

  const navItems = [
    { id: 'landing', label: 'Home', icon: Activity },
    { id: 'chat', label: 'AI Chatbot', icon: MessageSquare },
    { id: 'symptoms', label: 'Symptom Guide', icon: Stethoscope },
    { id: 'history', label: 'Chat History', icon: History },
    { id: 'admin', label: 'Analytics', icon: BarChart3 },
    { id: 'about', label: 'Architecture & NLP', icon: Info },
  ];

  const handleNavClick = (pageId: string) => {
    onNavigate(pageId);
    setMobileMenuOpen(false);
    setUserDropdownOpen(false);
  };

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo & Brand */}
          <div 
            onClick={() => handleNavClick('landing')}
            className="flex items-center gap-3 cursor-pointer group select-none"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-700 flex items-center justify-center text-white shadow-md shadow-cyan-600/20 group-hover:scale-105 transition-transform">
              <Stethoscope className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-lg text-slate-900 tracking-tight">MediNLP</span>
                <span className="bg-cyan-100 text-cyan-800 text-[10px] font-semibold px-2 py-0.5 rounded-full uppercase tracking-wider">
                  AI Health
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium">End-to-End NLP Healthcare</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`flex items-center gap-1.5 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'text-cyan-700 bg-cyan-50/80 shadow-xs'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100/80'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-600' : 'text-slate-400'}`} />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* User Section */}
          <div className="hidden md:flex items-center gap-3">
            {isAuthenticated ? (
              <div className="relative">
                <button
                  onClick={() => setUserDropdownOpen(!userDropdownOpen)}
                  className="flex items-center gap-2.5 p-1.5 pl-3 rounded-full border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-all text-sm"
                >
                  <div className="w-7 h-7 rounded-full bg-cyan-700 text-white flex items-center justify-center font-bold text-xs">
                    {user?.first_name ? user.first_name[0].toUpperCase() : user?.username[0].toUpperCase()}
                  </div>
                  <span className="font-medium text-slate-700 max-w-[120px] truncate">
                    {user?.first_name || user?.username}
                  </span>
                  <ChevronDown className="w-3.5 h-3.5 text-slate-400 mr-1.5" />
                </button>

                {userDropdownOpen && (
                  <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl shadow-xl border border-slate-100 py-1.5 z-50 animate-in fade-in zoom-in-95 duration-100">
                    <div className="px-4 py-2 border-b border-slate-100">
                      <p className="text-xs text-slate-500">Signed in as</p>
                      <p className="text-sm font-semibold text-slate-900 truncate">{user?.username}</p>
                      {user?.is_staff && (
                        <span className="inline-block mt-1 text-[10px] font-semibold bg-blue-50 text-blue-700 px-1.5 py-0.5 rounded">
                          Admin Staff
                        </span>
                      )}
                    </div>
                    <button
                      onClick={() => handleNavClick('profile')}
                      className="w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                    >
                      <UserIcon className="w-4 h-4 text-slate-400" />
                      Patient Profile
                    </button>
                    <button
                      onClick={() => handleNavClick('dashboard')}
                      className="w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                    >
                      <Activity className="w-4 h-4 text-slate-400" />
                      User Dashboard
                    </button>
                    <button
                      onClick={() => handleNavClick('history')}
                      className="w-full text-left px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 flex items-center gap-2"
                    >
                      <History className="w-4 h-4 text-slate-400" />
                      Saved Chats
                    </button>
                    <div className="border-t border-slate-100 my-1"></div>
                    <button
                      onClick={() => {
                        logout();
                        setUserDropdownOpen(false);
                      }}
                      className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center gap-2"
                    >
                      <LogOut className="w-4 h-4 text-red-400" />
                      Sign Out
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <button
                  onClick={() => handleNavClick('login')}
                  className="px-4 py-2 text-sm font-medium text-slate-700 hover:text-cyan-700 hover:bg-slate-100 rounded-lg transition-colors"
                >
                  Log In
                </button>
                <button
                  onClick={() => handleNavClick('register')}
                  className="px-4 py-2 text-sm font-medium text-white bg-cyan-700 hover:bg-cyan-800 rounded-lg shadow-sm hover:shadow transition-all"
                >
                  Register
                </button>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex items-center md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-t border-slate-200 bg-white px-4 pt-3 pb-4 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;
            return (
              <button
                key={item.id}
                onClick={() => handleNavClick(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium ${
                  isActive
                    ? 'text-cyan-700 bg-cyan-50'
                    : 'text-slate-700 hover:bg-slate-50'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-cyan-600' : 'text-slate-400'}`} />
                {item.label}
              </button>
            );
          })}

          <div className="pt-3 border-t border-slate-200 mt-2">
            {isAuthenticated ? (
              <>
                <button
                  onClick={() => handleNavClick('profile')}
                  className="w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 rounded-lg"
                >
                  <UserIcon className="w-5 h-5 text-slate-400" />
                  My Profile ({user?.username})
                </button>
                <button
                  onClick={() => {
                    logout();
                    setMobileMenuOpen(false);
                  }}
                  className="w-full flex items-center gap-3 px-3 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50 rounded-lg"
                >
                  <LogOut className="w-5 h-5 text-red-400" />
                  Sign Out
                </button>
              </>
            ) : (
              <div className="flex flex-col gap-2 pt-1">
                <button
                  onClick={() => handleNavClick('login')}
                  className="w-full text-center py-2 text-sm font-medium border border-slate-200 rounded-lg text-slate-700"
                >
                  Log In
                </button>
                <button
                  onClick={() => handleNavClick('register')}
                  className="w-full text-center py-2 text-sm font-medium bg-cyan-700 text-white rounded-lg shadow-xs"
                >
                  Create Account
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

