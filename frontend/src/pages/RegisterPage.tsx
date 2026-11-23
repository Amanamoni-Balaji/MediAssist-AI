import React, { useState } from 'react';
import { UserPlus, ShieldAlert, CheckCircle2, AlertCircle, Eye, EyeOff, Lock, User, Mail } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const RegisterPage: React.FC<{ onNavigate: (page: string) => void }> = ({ onNavigate }) => {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    first_name: '',
    last_name: '',
    password: '',
    confirm_password: '',
    medical_disclaimer_accepted: false,
  });

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Compute password strength score (0-4)
  const computePasswordStrength = (pwd: string) => {
    let score = 0;
    if (pwd.length >= 8) score++;
    if (/[A-Z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^A-Za-z0-9]/.test(pwd)) score++;
    return score;
  };

  const strength = computePasswordStrength(formData.password);

  const getStrengthLabel = (s: number) => {
    if (formData.password.length === 0) return { label: 'Empty', color: 'bg-slate-200' };
    if (s <= 1) return { label: 'Weak', color: 'bg-rose-500' };
    if (s === 2) return { label: 'Fair', color: 'bg-amber-500' };
    if (s === 3) return { label: 'Good', color: 'bg-blue-500' };
    return { label: 'Strong', color: 'bg-emerald-500' };
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (formData.password !== formData.confirm_password) {
      setError("Passwords do not match.");
      return;
    }

    if (!formData.medical_disclaimer_accepted) {
      setError("You must acknowledge that this assistant is an educational tool and not a doctor.");
      return;
    }

    setLoading(true);
    try {
      await register(formData);
      onNavigate('dashboard');
    } catch (err: any) {
      const errData = err.response?.data;
      if (typeof errData === 'object') {
        const firstKey = Object.keys(errData)[0];
        const val = errData[firstKey];
        setError(Array.isArray(val) ? val[0] : String(val));
      } else {
        setError("Registration failed. Please verify your details.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-10 px-4">
      <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-xl space-y-6">
        <div className="text-center space-y-1.5">
          <div className="w-12 h-12 rounded-2xl bg-cyan-100 text-cyan-700 flex items-center justify-center mx-auto mb-2">
            <UserPlus className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-slate-900">Create Patient Account</h2>
          <p className="text-xs text-slate-500">
            Sign up to save chat consultations, customize medical history, and explore personalized health topics.
          </p>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">First Name</label>
              <input
                type="text"
                required
                value={formData.first_name}
                onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                placeholder="Alex"
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-slate-700 block mb-1">Last Name</label>
              <input
                type="text"
                required
                value={formData.last_name}
                onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                placeholder="Vance"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">Username</label>
            <div className="relative">
              <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                required
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                placeholder="alexvance"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                placeholder="alex@health.com"
              />
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type={showPassword ? 'text' : 'password'}
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full text-xs pl-9 pr-10 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                placeholder="••••••••"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2.5 text-slate-400 hover:text-slate-600"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>

            {/* Password strength visual meter */}
            {formData.password && (
              <div className="mt-2 space-y-1">
                <div className="flex justify-between items-center text-[10px] text-slate-500">
                  <span>Strength</span>
                  <span className="font-semibold">{getStrengthLabel(strength).label}</span>
                </div>
                <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden flex gap-1">
                  {[1, 2, 3, 4].map((step) => (
                    <div
                      key={step}
                      className={`h-full flex-1 rounded-full ${
                        strength >= step ? getStrengthLabel(strength).color : 'bg-slate-200'
                      }`}
                    />
                  ))}
                </div>
              </div>
            )}
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-700 block mb-1">Confirm Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type={showPassword ? 'text' : 'password'}
                required
                value={formData.confirm_password}
                onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
                className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                placeholder="••••••••"
              />
            </div>
          </div>

          {/* Medical Disclaimer consent */}
          <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200 space-y-2">
            <label className="flex items-start gap-2.5 cursor-pointer">
              <input
                type="checkbox"
                required
                checked={formData.medical_disclaimer_accepted}
                onChange={(e) => setFormData({ ...formData, medical_disclaimer_accepted: e.target.checked })}
                className="mt-0.5 rounded text-cyan-600 focus:ring-cyan-500"
              />
              <span className="text-[11px] text-slate-600 leading-snug">
                I acknowledge that <strong>MediNLP AI</strong> is an educational healthcare assistant and <strong>not a medical professional or diagnosis tool</strong>. I agree to consult qualified clinicians for diagnosis and treatment.
              </span>
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl font-semibold text-xs text-white bg-cyan-700 hover:bg-cyan-800 disabled:opacity-50 transition-colors shadow-sm"
          >
            {loading ? "Registering Patient..." : "Create Account"}
          </button>
        </form>

        <div className="text-center pt-2 text-xs text-slate-500">
          Already registered?{' '}
          <button
            onClick={() => onNavigate('login')}
            className="text-cyan-700 font-semibold hover:underline"
          >
            Log In here
          </button>
        </div>
      </div>
    </div>
  );
};

