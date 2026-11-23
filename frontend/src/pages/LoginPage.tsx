import React, { useState } from 'react';
import { LogIn, Lock, User, AlertCircle, ShieldCheck, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const LoginPage: React.FC<{ onNavigate: (page: string) => void }> = ({ onNavigate }) => {
  const { login } = useAuth();
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(credentials);
      onNavigate('dashboard');
    } catch (err: any) {
      setError("Invalid username or password. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async (username: string, pwd: string) => {
    setCredentials({ username, password: pwd });
    setError(null);
    setLoading(true);
    try {
      await login({ username, password: pwd });
      onNavigate('dashboard');
    } catch {
      setError("Demo login failed. Please register a new user.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-12 px-4">
      <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-xl space-y-6">
        <div className="text-center space-y-1.5">
          <div className="w-12 h-12 rounded-2xl bg-cyan-100 text-cyan-700 flex items-center justify-center mx-auto mb-2">
            <LogIn className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Sign In to MediNLP</h2>
          <p className="text-xs text-slate-500">
            Access your healthcare dashboard, AI consultation sessions, and symptom logs.
          </p>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">Username</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                required
                value={credentials.username}
                onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
                className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                placeholder="Enter username (e.g. admin)"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="password"
                required
                value={credentials.password}
                onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                placeholder="••••••••"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl font-semibold text-xs text-white bg-cyan-700 hover:bg-cyan-800 disabled:opacity-50 transition-colors shadow-sm"
          >
            {loading ? "Authenticating..." : "Sign In"}
          </button>
        </form>

        {/* Demo Fast Login Buttons */}
        <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-2">
          <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-cyan-600" />
            Quick Demo Access (Portfolio Review)
          </p>
          <div className="grid grid-cols-2 gap-2 pt-1">
            <button
              type="button"
              onClick={() => handleDemoLogin('admin', 'admin123')}
              className="py-2 px-3 rounded-xl bg-white border border-slate-200 hover:border-cyan-600 hover:text-cyan-700 text-xs font-medium text-slate-700 transition-colors text-left"
            >
              <div className="font-semibold">Demo Admin</div>
              <div className="text-[10px] text-slate-400">admin / admin123</div>
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('testpatient', 'Password123!')}
              className="py-2 px-3 rounded-xl bg-white border border-slate-200 hover:border-cyan-600 hover:text-cyan-700 text-xs font-medium text-slate-700 transition-colors text-left"
            >
              <div className="font-semibold">Demo Patient</div>
              <div className="text-[10px] text-slate-400">patient / pass</div>
            </button>
          </div>
        </div>

        <div className="text-center pt-1 text-xs text-slate-500">
          Don't have an account yet?{' '}
          <button
            onClick={() => onNavigate('register')}
            className="text-cyan-700 font-semibold hover:underline"
          >
            Register here
          </button>
        </div>
      </div>
    </div>
  );
};

