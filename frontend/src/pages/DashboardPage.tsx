import React, { useState, useEffect } from 'react';
import { 
  Bot, 
  Stethoscope, 
  History, 
  BarChart3, 
  User, 
  ShieldCheck, 
  Clock, 
  ArrowRight, 
  PlusCircle, 
  Heart, 
  Droplet, 
  Moon, 
  Salad,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { chatApi, type Conversation } from '../api/chat';

interface DashboardPageProps {
  onNavigate: (page: string, params?: any) => void;
  onQuickChat: (query: string) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ onNavigate, onQuickChat }) => {
  const { user } = useAuth();
  const [recentConversations, setRecentConversations] = useState<Conversation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecent = async () => {
      try {
        const list = await chatApi.getConversations();
        setRecentConversations(list.slice(0, 4));
      } catch (err) {
        console.error("Failed to fetch recent chats", err);
      } finally {
        setLoading(false);
      }
    };
    fetchRecent();
  }, []);

  const wellnessCards = [
    {
      icon: Droplet,
      color: "text-blue-500 bg-blue-50",
      title: "Daily Hydration Balance",
      text: "Drink 2–3 liters of water daily. Hydration regulates body temperature, supports kidney filtration, and prevents tension headaches."
    },
    {
      icon: Heart,
      color: "text-rose-500 bg-rose-50",
      title: "Cardiovascular Health",
      text: "Engage in at least 150 minutes of moderate aerobic exercise weekly. Reduce dietary sodium intake below 2,000 mg/day."
    },
    {
      icon: Moon,
      color: "text-indigo-500 bg-indigo-50",
      title: "Sleep & Immune Defense",
      text: "Aim for 7–9 hours of continuous sleep. Consistent circadian rhythm boosts immune T-cells and lowers chronic cortisol production."
    },
    {
      icon: Salad,
      color: "text-emerald-500 bg-emerald-50",
      title: "Balanced Dietary Fiber",
      text: "Incorporate whole legumes, leafy greens, and colorful vegetables to nourish healthy gut microbiota and stabilize blood sugar."
    }
  ];

  return (
    <div className="space-y-8 py-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-cyan-800 to-blue-900 rounded-3xl p-8 text-white shadow-lg relative overflow-hidden">
        <div className="relative z-10 space-y-3 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/10 text-cyan-200 text-xs font-semibold backdrop-blur-xs">
            <Sparkles className="w-3.5 h-3.5" />
            Patient Health Dashboard
          </div>
          <h1 className="text-3xl font-extrabold text-white">
            Welcome back, {user?.first_name || user?.username || 'Patient'}
          </h1>
          <p className="text-xs sm:text-sm text-cyan-100/90 leading-relaxed">
            Your personal AI healthcare intelligence workspace. Explore symptoms, launch interactive NLP health inquiries, and view clinical references.
          </p>
          <div className="pt-2 flex flex-wrap gap-3">
            <button
              onClick={() => onNavigate('chat')}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-xs text-cyan-900 bg-white hover:bg-cyan-50 shadow-sm transition-all"
            >
              <PlusCircle className="w-4 h-4 text-cyan-700" />
              Start New Consultation
            </button>
            <button
              onClick={() => onNavigate('symptoms')}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl font-semibold text-xs text-white bg-white/15 hover:bg-white/20 border border-white/20 transition-all"
            >
              <Stethoscope className="w-4 h-4" />
              Symptom Guide
            </button>
          </div>
        </div>
      </div>

      {/* Quick Launch Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          {
            title: "AI Medical Chatbot",
            desc: "Ask any medical question with natural language NLP",
            action: () => onNavigate('chat'),
            icon: Bot,
            badge: "Live NLP",
            color: "text-cyan-700 bg-cyan-50 border-cyan-100"
          },
          {
            title: "Symptom Assessment",
            desc: "Select symptoms and review educational associations",
            action: () => onNavigate('symptoms'),
            icon: Stethoscope,
            badge: "Interactive",
            color: "text-blue-700 bg-blue-50 border-blue-100"
          },
          {
            title: "Consultation History",
            desc: "Review or resume your past AI health chat sessions",
            action: () => onNavigate('history'),
            icon: History,
            badge: `${recentConversations.length} Saved`,
            color: "text-violet-700 bg-violet-50 border-violet-100"
          },
          {
            title: "Model & System Analytics",
            desc: "Inspect real-time model accuracy, precision, and F1",
            action: () => onNavigate('admin'),
            icon: BarChart3,
            badge: "Real Metrics",
            color: "text-emerald-700 bg-emerald-50 border-emerald-100"
          }
        ].map((item, idx) => {
          const Icon = item.icon;
          return (
            <div
              key={idx}
              onClick={item.action}
              className="bg-white p-5 rounded-2xl border border-slate-200/90 shadow-xs hover:shadow-md hover:border-cyan-500/50 transition-all cursor-pointer flex flex-col justify-between group"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className={`w-10 h-10 rounded-xl flex items-center justify-center border ${item.color}`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-100 text-slate-600">
                    {item.badge}
                  </span>
                </div>
                <div>
                  <h4 className="text-sm font-bold text-slate-900 group-hover:text-cyan-700 transition-colors">
                    {item.title}
                  </h4>
                  <p className="text-xs text-slate-500 mt-1 leading-relaxed">{item.desc}</p>
                </div>
              </div>
              <div className="pt-4 flex items-center gap-1 text-xs font-semibold text-cyan-700">
                <span>Access module</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Grid: Recent Chats & Health Tips */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Conversations */}
        <div className="lg:col-span-2 bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <History className="w-4 h-4 text-cyan-600" />
              Recent AI Health Consultations
            </h3>
            <button
              onClick={() => onNavigate('history')}
              className="text-xs font-semibold text-cyan-700 hover:underline"
            >
              View All History
            </button>
          </div>

          {loading ? (
            <div className="py-8 text-center text-xs text-slate-400">Loading consultations...</div>
          ) : recentConversations.length === 0 ? (
            <div className="py-10 text-center space-y-2">
              <Bot className="w-10 h-10 text-slate-300 mx-auto" />
              <p className="text-xs font-medium text-slate-600">No chat sessions logged yet.</p>
              <button
                onClick={() => onNavigate('chat')}
                className="text-xs font-semibold text-cyan-700 hover:underline"
              >
                Start your first consultation now
              </button>
            </div>
          ) : (
            <div className="space-y-2.5">
              {recentConversations.map((conv) => (
                <div
                  key={conv.id}
                  onClick={() => onNavigate('chat', { conversationId: conv.id })}
                  className="p-3.5 rounded-2xl border border-slate-100 hover:border-cyan-300 hover:bg-cyan-50/40 transition-all cursor-pointer flex items-center justify-between"
                >
                  <div className="space-y-1 max-w-[80%]">
                    <h4 className="text-xs font-bold text-slate-800 truncate">{conv.title}</h4>
                    <p className="text-[11px] text-slate-400 truncate">
                      {conv.last_message?.text || "New consultation opened"}
                    </p>
                  </div>
                  <div className="text-right text-[10px] text-slate-400 flex items-center gap-1 shrink-0">
                    <Clock className="w-3 h-3" />
                    <span>{new Date(conv.updated_at).toLocaleDateString()}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* User Profile Mini Card */}
        <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <User className="w-4 h-4 text-cyan-600" />
              Patient Profile
            </h3>
            <button
              onClick={() => onNavigate('profile')}
              className="text-xs font-semibold text-cyan-700 hover:underline"
            >
              Edit
            </button>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-2.5 text-xs">
            <div className="flex justify-between">
              <span className="text-slate-500">Name</span>
              <span className="font-semibold text-slate-800">{user?.first_name || user?.username}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Email</span>
              <span className="font-semibold text-slate-800 truncate max-w-[150px]">{user?.email || "Not set"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Blood Group</span>
              <span className="font-semibold text-slate-800">{user?.profile?.blood_group || "Unspecified"}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">Disclaimer Signed</span>
              <span className="font-semibold text-emerald-600 flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" /> Accepted
              </span>
            </div>
          </div>

          <div className="border-t border-slate-100 pt-3">
            <p className="text-[11px] text-slate-500 leading-relaxed">
              Keep your health profile details updated so you can discuss them with your family physician.
            </p>
          </div>
        </div>
      </div>

      {/* Wellness & Preventive Health Tips */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-slate-900">
          Daily Preventive Health Guidelines
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {wellnessCards.map((card, i) => {
            const Icon = card.icon;
            return (
              <div key={i} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-2.5">
                <div className={`w-9 h-9 rounded-xl flex items-center justify-center ${card.color}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <h4 className="text-xs font-bold text-slate-900">{card.title}</h4>
                <p className="text-[11px] text-slate-500 leading-relaxed">{card.text}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

