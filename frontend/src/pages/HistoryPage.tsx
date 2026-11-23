import React, { useState, useEffect } from 'react';
import { 
  History, 
  Search, 
  Trash2, 
  MessageSquare, 
  Calendar, 
  ArrowRight, 
  Bot, 
  Clock, 
  AlertCircle 
} from 'lucide-react';
import { chatApi, type Conversation } from '../api/chat';

interface HistoryPageProps {
  onNavigate: (page: string, params?: any) => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ onNavigate }) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [search, setSearch] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  const fetchConversations = async () => {
    try {
      const data = await chatApi.getConversations();
      setConversations(data);
    } catch (err) {
      console.error("Failed to load history", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchConversations();
  }, []);

  const handleDelete = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm("Are you sure you want to permanently delete this consultation record?")) return;
    try {
      await chatApi.deleteConversation(id);
      setConversations(conversations.filter(c => c.id !== id));
    } catch (err) {
      console.error("Failed to delete", err);
    }
  };

  const filtered = conversations.filter(c => 
    c.title.toLowerCase().includes(search.toLowerCase()) ||
    (c.last_message?.text && c.last_message.text.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="max-w-4xl mx-auto py-8 space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-50 text-cyan-800 text-xs font-semibold mb-1">
            <History className="w-3.5 h-3.5" />
            <span>Consultation Archive</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            Past Medical AI Consultations
          </h1>
          <p className="text-xs text-slate-500">
            Review previous interactions, questions asked, and educational responses provided.
          </p>
        </div>

        <button
          onClick={() => onNavigate('chat')}
          className="px-4 py-2.5 rounded-xl font-semibold text-xs text-white bg-cyan-700 hover:bg-cyan-800 shadow-sm transition-all self-start sm:self-auto flex items-center gap-1.5"
        >
          <Bot className="w-4 h-4" />
          New Consultation
        </button>
      </div>

      {/* Search box */}
      <div className="relative">
        <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search by topic, symptom, or conversation title..."
          className="w-full text-xs pl-10 pr-4 py-3 rounded-2xl bg-white border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600 shadow-xs"
        />
      </div>

      {/* Conversations List */}
      {loading ? (
        <div className="py-16 text-center text-xs text-slate-400">Loading history...</div>
      ) : filtered.length === 0 ? (
        <div className="bg-white rounded-3xl p-12 text-center border border-slate-200 shadow-xs space-y-3">
          <MessageSquare className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No Consultations Found</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            {search ? "No consultation logs matched your search terms." : "You haven't initiated any AI medical consultations yet."}
          </p>
          <button
            onClick={() => onNavigate('chat')}
            className="text-xs font-semibold text-cyan-700 hover:underline pt-2 block mx-auto"
          >
            Launch Medical Chatbot
          </button>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((conv) => (
            <div
              key={conv.id}
              onClick={() => onNavigate('chat', { conversationId: conv.id })}
              className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs hover:shadow-md hover:border-cyan-400/60 transition-all cursor-pointer flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
            >
              <div className="space-y-1.5 flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-slate-900 group-hover:text-cyan-700 transition-colors truncate">
                    {conv.title}
                  </h3>
                  {conv.message_count !== undefined && (
                    <span className="text-[10px] font-semibold bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full shrink-0">
                      {conv.message_count} messages
                    </span>
                  )}
                </div>
                {conv.last_message && (
                  <p className="text-xs text-slate-500 truncate">
                    <span className="font-medium text-slate-700">Last:</span> {conv.last_message.text}
                  </p>
                )}
                <div className="flex items-center gap-3 text-[10px] text-slate-400 pt-0.5">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {new Date(conv.created_at).toLocaleDateString()}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-3 h-3" />
                    {new Date(conv.updated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-2 shrink-0 self-end sm:self-center">
                <button
                  onClick={(e) => handleDelete(conv.id, e)}
                  className="p-2 rounded-xl text-slate-400 hover:text-red-600 hover:bg-red-50 transition-colors"
                  title="Delete consultation log"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
                <div className="px-3 py-1.5 rounded-xl bg-slate-50 group-hover:bg-cyan-50 text-slate-700 group-hover:text-cyan-700 text-xs font-semibold flex items-center gap-1 transition-colors">
                  <span>Resume</span>
                  <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

