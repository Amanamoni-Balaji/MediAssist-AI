import React, { useState } from 'react';
import { 
  User, 
  Mail, 
  Phone, 
  ShieldCheck, 
  Lock, 
  Save, 
  AlertCircle, 
  CheckCircle2, 
  Heart,
  Calendar
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { authApi } from '../api/auth';

export const ProfilePage: React.FC = () => {
  const { user, refreshProfile } = useAuth();

  const [personalData, setPersonalData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    email: user?.email || '',
    phone: user?.profile?.phone || '',
    gender: user?.profile?.gender || 'Prefer not to say',
    blood_group: user?.profile?.blood_group || '',
    emergency_contact: user?.profile?.emergency_contact || '',
    bio: user?.profile?.bio || '',
  });

  const [passwordData, setPasswordData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: '',
  });

  const [personalMsg, setPersonalMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [pwdMsg, setPwdMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const [savingPersonal, setSavingPersonal] = useState(false);
  const [savingPwd, setSavingPwd] = useState(false);

  const handlePersonalSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPersonalMsg(null);
    setSavingPersonal(true);
    try {
      await authApi.updateProfile({
        first_name: personalData.first_name,
        last_name: personalData.last_name,
        email: personalData.email,
        profile: {
          phone: personalData.phone,
          gender: personalData.gender,
          blood_group: personalData.blood_group,
          emergency_contact: personalData.emergency_contact,
          bio: personalData.bio,
        }
      });
      await refreshProfile();
      setPersonalMsg({ type: 'success', text: 'Profile details updated successfully.' });
    } catch (err: any) {
      setPersonalMsg({ type: 'error', text: 'Failed to update profile. Please check inputs.' });
    } finally {
      setSavingPersonal(false);
    }
  };

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPwdMsg(null);

    if (passwordData.new_password !== passwordData.confirm_password) {
      setPwdMsg({ type: 'error', text: 'New passwords do not match.' });
      return;
    }

    setSavingPwd(true);
    try {
      await authApi.changePassword({
        old_password: passwordData.old_password,
        new_password: passwordData.new_password,
      });
      setPwdMsg({ type: 'success', text: 'Password changed successfully.' });
      setPasswordData({ old_password: '', new_password: '', confirm_password: '' });
    } catch (err: any) {
      setPwdMsg({ type: 'error', text: 'Password change failed. Verify your current password.' });
    } finally {
      setSavingPwd(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-8">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
          Patient Profile & Settings
        </h1>
        <p className="text-xs text-slate-500">
          Manage your personal healthcare metadata, contact details, and account security.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Profile Card Left */}
        <div className="lg:col-span-1 space-y-4">
          <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs text-center space-y-4">
            <div className="w-20 h-20 rounded-full bg-gradient-to-tr from-cyan-600 to-blue-700 text-white font-extrabold text-2xl flex items-center justify-center mx-auto shadow-md">
              {user?.first_name ? user.first_name[0].toUpperCase() : user?.username[0].toUpperCase()}
            </div>
            <div>
              <h3 className="font-bold text-base text-slate-900">
                {user?.first_name ? `${user.first_name} ${user.last_name}` : user?.username}
              </h3>
              <p className="text-xs text-slate-500">@{user?.username}</p>
              {user?.is_staff && (
                <span className="inline-block mt-2 text-[10px] font-semibold bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full border border-blue-200">
                  Staff Administrator
                </span>
              )}
            </div>

            <div className="border-t border-slate-100 pt-4 space-y-2 text-xs text-left">
              <div className="flex justify-between text-slate-500">
                <span>Blood Group:</span>
                <span className="font-semibold text-slate-800">{user?.profile?.blood_group || 'Not set'}</span>
              </div>
              <div className="flex justify-between text-slate-500">
                <span>Gender:</span>
                <span className="font-semibold text-slate-800">{user?.profile?.gender || 'Unspecified'}</span>
              </div>
              <div className="flex justify-between text-slate-500">
                <span>Disclaimer:</span>
                <span className="font-semibold text-emerald-600 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5" /> Acknowledged
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Edit Forms Right */}
        <div className="lg:col-span-2 space-y-6">
          {/* Personal Information Form */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-5">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <User className="w-4 h-4 text-cyan-600" />
              Patient Information
            </h3>

            {personalMsg && (
              <div className={`p-3 rounded-xl text-xs flex items-center gap-2 ${
                personalMsg.type === 'success' 
                  ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' 
                  : 'bg-rose-50 text-rose-800 border border-rose-200'
              }`}>
                {personalMsg.type === 'success' ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                <span>{personalMsg.text}</span>
              </div>
            )}

            <form onSubmit={handlePersonalSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">First Name</label>
                  <input
                    type="text"
                    value={personalData.first_name}
                    onChange={(e) => setPersonalData({ ...personalData, first_name: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">Last Name</label>
                  <input
                    type="text"
                    value={personalData.last_name}
                    onChange={(e) => setPersonalData({ ...personalData, last_name: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">Email Address</label>
                <input
                  type="email"
                  value={personalData.email}
                  onChange={(e) => setPersonalData({ ...personalData, email: e.target.value })}
                  className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">Gender</label>
                  <select
                    value={personalData.gender}
                    onChange={(e) => setPersonalData({ ...personalData, gender: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600 bg-white"
                  >
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                    <option value="Non-binary">Non-binary</option>
                    <option value="Other">Other</option>
                    <option value="Prefer not to say">Prefer not to say</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">Blood Group</label>
                  <input
                    type="text"
                    placeholder="e.g. O+, A-, B+"
                    value={personalData.blood_group}
                    onChange={(e) => setPersonalData({ ...personalData, blood_group: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">Emergency Contact Information</label>
                <input
                  type="text"
                  placeholder="e.g. Jane Vance (Sister) - 555-0199"
                  value={personalData.emergency_contact}
                  onChange={(e) => setPersonalData({ ...personalData, emergency_contact: e.target.value })}
                  className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                />
              </div>

              <div className="pt-2 flex justify-end">
                <button
                  type="submit"
                  disabled={savingPersonal}
                  className="px-5 py-2.5 rounded-xl text-xs font-semibold text-white bg-cyan-700 hover:bg-cyan-800 disabled:opacity-50 transition-colors shadow-xs flex items-center gap-1.5"
                >
                  <Save className="w-3.5 h-3.5" />
                  {savingPersonal ? "Saving..." : "Save Profile Details"}
                </button>
              </div>
            </form>
          </div>

          {/* Change Password Form */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-5">
            <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
              <Lock className="w-4 h-4 text-cyan-600" />
              Security & Password
            </h3>

            {pwdMsg && (
              <div className={`p-3 rounded-xl text-xs flex items-center gap-2 ${
                pwdMsg.type === 'success' 
                  ? 'bg-emerald-50 text-emerald-800 border border-emerald-200' 
                  : 'bg-rose-50 text-rose-800 border border-rose-200'
              }`}>
                {pwdMsg.type === 'success' ? <CheckCircle2 className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                <span>{pwdMsg.text}</span>
              </div>
            )}

            <form onSubmit={handlePasswordSubmit} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-700 block mb-1">Current Password</label>
                <input
                  type="password"
                  required
                  value={passwordData.old_password}
                  onChange={(e) => setPasswordData({ ...passwordData, old_password: e.target.value })}
                  className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">New Password</label>
                  <input
                    type="password"
                    required
                    value={passwordData.new_password}
                    onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                  />
                </div>
                <div>
                  <label className="text-xs font-semibold text-slate-700 block mb-1">Confirm New Password</label>
                  <input
                    type="password"
                    required
                    value={passwordData.confirm_password}
                    onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                    className="w-full text-xs p-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
                  />
                </div>
              </div>

              <div className="pt-2 flex justify-end">
                <button
                  type="submit"
                  disabled={savingPwd}
                  className="px-5 py-2.5 rounded-xl text-xs font-semibold text-white bg-slate-800 hover:bg-slate-900 disabled:opacity-50 transition-colors shadow-xs"
                >
                  {savingPwd ? "Updating..." : "Update Password"}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

