import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, 
  Send, 
  Plus, 
  Trash2, 
  RotateCcw, 
  Sparkles, 
  AlertTriangle, 
  ThumbsUp, 
  ThumbsDown, 
  Copy, 
  Check, 
  Tag, 
  Stethoscope, 
  Info,
  Clock,
  User,
  ArrowRight
} from 'lucide-react';
import { chatApi, type Conversation, type ChatMessage } from '../api/chat';
import { FeedbackModal } from '../components/FeedbackModal';

interface ChatbotPageProps {
  initialConversationId?: string;
  initialQuery?: string;
  onNavigate: (page: string) => void;
}

export const ChatbotPage: React.FC<ChatbotPageProps> = ({ 
  initialConversationId, 
  initialQuery,
  onNavigate 
}) => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = useState<string | null>(initialConversationId || null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputText, setInputText] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [feedbackMessageId, setFeedbackMessageId] = useState<string | null>(null);
  const [isHelpfulState, setIsHelpfulState] = useState<boolean>(true);
  const [feedbackOpen, setFeedbackOpen] = useState<boolean>(false);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const suggestedQuestions = [
    "What is diabetes?",
    "What are common symptoms of fever?",
    "What causes headaches?",
    "What is hypertension?",
    "What are the symptoms of dehydration?",
    "How can I maintain a healthy lifestyle?"
  ];

  // Scroll to bottom of message list
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Load conversations list
  const loadConversations = async () => {
    try {
      const list = await chatApi.getConversations();
      setConversations(list);
      if (!activeConvId && list.length > 0) {
        setActiveConvId(list[0].id);
      }
    } catch (err) {
      console.error("Failed to load conversations", err);
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  // Load active conversation messages
  useEffect(() => {
    if (activeConvId) {
      const fetchDetail = async () => {
        try {
          const detail = await chatApi.getConversation(activeConvId);
          setMessages(detail.messages || []);
        } catch (err) {
          console.error("Failed to fetch conversation details", err);
        }
      };
      fetchDetail();
    } else {
      setMessages([]);
    }
  }, [activeConvId]);

  // Handle initial query if passed (e.g. from quick button or landing page)
  useEffect(() => {
    if (initialQuery && initialQuery.trim()) {
      handleSendMessage(initialQuery);
    }
  }, [initialQuery]);

  const handleNewConversation = async () => {
    try {
      const newConv = await chatApi.createConversation("New Health Consultation");
      setConversations([newConv, ...conversations]);
      setActiveConvId(newConv.id);
      setMessages([]);
    } catch (err) {
      console.error("Failed to create new conversation", err);
    }
  };

  const handleDeleteConversation = async (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!confirm("Are you sure you want to delete this consultation log?")) return;
    try {
      await chatApi.deleteConversation(id);
      const remaining = conversations.filter(c => c.id !== id);
      setConversations(remaining);
      if (activeConvId === id) {
        setActiveConvId(remaining.length > 0 ? remaining[0].id : null);
      }
    } catch (err) {
      console.error("Failed to delete conversation", err);
    }
  };

  const handleClearCurrentChat = async () => {
    if (!activeConvId) return;
    if (!confirm("Clear all messages in this consultation?")) return;
    try {
      await chatApi.clearConversation(activeConvId);
      setMessages([]);
    } catch (err) {
      console.error("Failed to clear conversation", err);
    }
  };

  const handleSendMessage = async (queryText?: string) => {
    const textToSend = queryText || inputText;
    if (!textToSend.trim() || loading) return;

    setInputText('');
    setLoading(true);

    // Optimistically add user message to list
    const tempUserMsg: ChatMessage = {
      id: `temp-${Date.now()}`,
      conversation: activeConvId || '',
      sender: 'user',
      text: textToSend.trim(),
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, tempUserMsg]);

    try {
      const response = await chatApi.sendMessage(textToSend.trim(), activeConvId || undefined);
      
      // If we didn't have an active conversation, set it now
      if (!activeConvId && response.conversation_id) {
        setActiveConvId(response.conversation_id);
        loadConversations();
      }

      // Replace messages with updated server payload
      setMessages(prev => {
        const filtered = prev.filter(m => m.id !== tempUserMsg.id);
        return [...filtered, response.user_message, response.assistant_message];
      });

      // Update current title in conversations list if changed
      setConversations(prev => prev.map(c => 
        c.id === response.conversation_id 
          ? { ...c, title: response.conversation_title, updated_at: new Date().toISOString() } 
          : c
      ));

    } catch (err) {
      console.error("Chat error", err);
      // Append fallback error message
      const errorBotMsg: ChatMessage = {
        id: `err-${Date.now()}`,
        conversation: activeConvId || '',
        sender: 'assistant',
        text: "I apologize, but I encountered an issue connecting to the NLP processing service. Please ensure the backend server is running and try again.",
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorBotMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const copyToClipboard = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const openFeedback = (msgId: string, helpful: boolean) => {
    setFeedbackMessageId(msgId);
    setIsHelpfulState(helpful);
    setFeedbackOpen(true);
  };

  return (
    <div className="h-[calc(100vh-8.5rem)] flex gap-4 py-2">
      {/* Sidebar: Conversations List */}
      <aside className="w-80 bg-white rounded-3xl border border-slate-200 shadow-xs flex flex-col shrink-0 hidden lg:flex overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bot className="w-5 h-5 text-cyan-600" />
            <h3 className="font-bold text-sm text-slate-800">Consultations</h3>
          </div>
          <button
            onClick={handleNewConversation}
            className="p-1.5 rounded-xl bg-cyan-50 hover:bg-cyan-100 text-cyan-700 transition-colors flex items-center gap-1 text-xs font-semibold"
            title="Start new consultation"
          >
            <Plus className="w-4 h-4" />
            New
          </button>
        </div>

        {/* Sessions scrollable list */}
        <div className="flex-1 overflow-y-auto p-2 space-y-1.5">
          {conversations.length === 0 ? (
            <div className="text-center py-10 px-4 text-xs text-slate-400">
              No saved conversations. Start asking a question to create one.
            </div>
          ) : (
            conversations.map((conv) => {
              const isActive = conv.id === activeConvId;
              return (
                <div
                  key={conv.id}
                  onClick={() => setActiveConvId(conv.id)}
                  className={`group p-3 rounded-2xl cursor-pointer text-xs transition-all flex items-center justify-between ${
                    isActive
                      ? 'bg-cyan-50/80 text-cyan-900 font-semibold border border-cyan-200/60 shadow-2xs'
                      : 'text-slate-600 hover:bg-slate-50 border border-transparent'
                  }`}
                >
                  <div className="truncate pr-2">
                    <p className="truncate text-xs">{conv.title}</p>
                    <span className="text-[10px] text-slate-400 font-normal">
                      {new Date(conv.updated_at).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                    </span>
                  </div>
                  <button
                    onClick={(e) => handleDeleteConversation(conv.id, e)}
                    className="opacity-0 group-hover:opacity-100 p-1 rounded-lg text-slate-400 hover:text-red-600 hover:bg-red-50 transition-all shrink-0"
                    title="Delete session"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              );
            })
          )}
        </div>

        {/* Bottom Actions */}
        {activeConvId && (
          <div className="p-3 border-t border-slate-100 bg-slate-50/50">
            <button
              onClick={handleClearCurrentChat}
              className="w-full flex items-center justify-center gap-1.5 py-1.5 text-xs text-slate-500 hover:text-red-600 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              Clear Current Chat
            </button>
          </div>
        )}
      </aside>

      {/* Main Chat Interface */}
      <section className="flex-1 bg-white rounded-3xl border border-slate-200 shadow-xs flex flex-col overflow-hidden">
        {/* Chat Header */}
        <div className="px-6 py-3.5 border-b border-slate-100 flex items-center justify-between bg-white/50 backdrop-blur-xs">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-cyan-600 text-white flex items-center justify-center shadow-xs">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="font-bold text-sm text-slate-900">Dr. MediNLP AI Assistant</h2>
                <span className="bg-emerald-50 text-emerald-700 text-[10px] font-semibold px-2 py-0.5 rounded-full flex items-center gap-1 border border-emerald-200/60">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                  Online
                </span>
              </div>
              <p className="text-[11px] text-slate-500">
                Natural Language Healthcare Guidance (WHO, MedlinePlus & NHS Knowledge)
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleNewConversation}
              className="lg:hidden p-2 rounded-xl bg-cyan-50 text-cyan-700 text-xs font-semibold flex items-center gap-1"
            >
              <Plus className="w-4 h-4" />
              New
            </button>
            <button
              onClick={() => onNavigate('about')}
              className="text-xs text-slate-400 hover:text-cyan-700 p-1.5 rounded-lg transition-colors flex items-center gap-1"
              title="View NLP pipeline architecture"
            >
              <Info className="w-4 h-4" />
              <span className="hidden sm:inline text-[11px]">Pipeline Info</span>
            </button>
          </div>
        </div>

        {/* Messages Stream */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center max-w-xl mx-auto space-y-6 py-8">
              <div className="w-16 h-16 rounded-3xl bg-gradient-to-tr from-cyan-600 to-blue-700 text-white flex items-center justify-center shadow-lg shadow-cyan-600/20">
                <Stethoscope className="w-8 h-8" />
              </div>
              <div className="space-y-2">
                <h3 className="text-xl font-bold text-slate-900">
                  How can I help with your health questions today?
                </h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Ask in plain natural English about common conditions, symptoms, healthy diet, or preventive care. Our NLP engine will analyze your query and retrieve verified clinical guidance.
                </p>
              </div>

              {/* Suggested Questions Grid */}
              <div className="w-full space-y-2 text-left">
                <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider text-center">
                  Recommended Inquiries:
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {suggestedQuestions.map((q, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSendMessage(q)}
                      className="p-3 text-xs bg-slate-50 hover:bg-cyan-50/70 border border-slate-200/80 hover:border-cyan-400 rounded-xl text-slate-700 transition-all flex items-center justify-between text-left group"
                    >
                      <span className="truncate">{q}</span>
                      <ArrowRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-cyan-600 group-hover:translate-x-0.5 transition-transform shrink-0 ml-2" />
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            messages.map((msg) => {
              const isUser = msg.sender === 'user';
              return (
                <div
                  key={msg.id}
                  className={`flex gap-3 max-w-3xl ${isUser ? 'ml-auto flex-row-reverse' : 'mr-auto'}`}
                >
                  {/* Avatar */}
                  <div
                    className={`w-8 h-8 rounded-xl flex items-center justify-center text-xs font-bold shrink-0 ${
                      isUser
                        ? 'bg-slate-800 text-white'
                        : 'bg-cyan-600 text-white shadow-xs'
                    }`}
                  >
                    {isUser ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                  </div>

                  {/* Message Bubble Content */}
                  <div
                    className={`rounded-2xl p-4 text-xs leading-relaxed space-y-2.5 ${
                      isUser
                        ? 'bg-slate-900 text-white rounded-tr-none'
                        : msg.is_emergency
                        ? 'bg-red-50 text-red-950 border border-red-300 rounded-tl-none shadow-xs'
                        : 'bg-slate-50 border border-slate-200/80 text-slate-800 rounded-tl-none shadow-2xs'
                    }`}
                  >
                    {/* Emergency Alert Banner if message is an emergency */}
                    {msg.is_emergency && (
                      <div className="flex items-center gap-1.5 text-red-700 font-bold bg-red-100/80 px-2.5 py-1 rounded-lg text-[11px]">
                        <AlertTriangle className="w-3.5 h-3.5" />
                        <span>URGENT EMERGENCY ADVISORY</span>
                      </div>
                    )}

                    {/* Formatted Message Body with Markdown formatting support */}
                    <div className="whitespace-pre-wrap leading-relaxed">
                      {msg.text}
                    </div>

                    {/* NLP Metadata Tags for Assistant Responses */}
                    {!isUser && !msg.is_emergency && (msg.intent || msg.matched_topic || msg.entities?.symptoms?.length) && (
                      <div className="pt-2 border-t border-slate-200/60 flex flex-wrap items-center gap-1.5 text-[10px]">
                        {msg.intent && (
                          <span className="bg-cyan-100/80 text-cyan-800 font-semibold px-2 py-0.5 rounded-md flex items-center gap-1">
                            <Tag className="w-2.5 h-2.5" />
                            Intent: {msg.intent}
                          </span>
                        )}
                        {typeof msg.confidence === 'number' && msg.confidence > 0 && (
                          <span className="bg-slate-200/70 text-slate-700 font-medium px-2 py-0.5 rounded-md">
                            Score: {(msg.confidence * 100).toFixed(0)}%
                          </span>
                        )}
                        {msg.matched_topic && (
                          <span className="bg-blue-100/80 text-blue-800 font-semibold px-2 py-0.5 rounded-md">
                            Topic: {msg.matched_topic}
                          </span>
                        )}
                        {msg.entities?.symptoms?.map((s, idx) => (
                          <span key={idx} className="bg-amber-100/80 text-amber-900 px-2 py-0.5 rounded-md">
                            Symptom: {s}
                          </span>
                        ))}
                      </div>
                    )}

                    {/* Bottom Actions Bar (Assistant messages) */}
                    {!isUser && (
                      <div className="pt-1 flex items-center justify-between text-[10px] text-slate-400">
                        <span className="flex items-center gap-1">
                          <Clock className="w-2.5 h-2.5" />
                          {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>

                        <div className="flex items-center gap-1.5">
                          <button
                            onClick={() => copyToClipboard(msg.text, msg.id)}
                            className="p-1 hover:text-cyan-700 rounded transition-colors"
                            title="Copy response"
                          >
                            {copiedId === msg.id ? (
                              <Check className="w-3.5 h-3.5 text-emerald-600" />
                            ) : (
                              <Copy className="w-3.5 h-3.5" />
                            )}
                          </button>
                          <button
                            onClick={() => openFeedback(msg.id, true)}
                            className="p-1 hover:text-emerald-600 rounded transition-colors"
                            title="Helpful response"
                          >
                            <ThumbsUp className="w-3.5 h-3.5" />
                          </button>
                          <button
                            onClick={() => openFeedback(msg.id, false)}
                            className="p-1 hover:text-rose-600 rounded transition-colors"
                            title="Not helpful response"
                          >
                            <ThumbsDown className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Follow-up Questions Suggestions */}
                    {!isUser && msg.suggested_questions && msg.suggested_questions.length > 0 && (
                      <div className="pt-2 border-t border-slate-200/50 space-y-1">
                        <p className="text-[10px] font-semibold text-slate-500">Related follow-ups:</p>
                        <div className="flex flex-wrap gap-1.5">
                          {msg.suggested_questions.slice(0, 3).map((sq, i) => (
                            <button
                              key={i}
                              onClick={() => handleSendMessage(sq)}
                              className="text-[10px] px-2.5 py-1 bg-white hover:bg-cyan-50 border border-slate-200 rounded-lg text-slate-700 transition-colors"
                            >
                              {sq}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })
          )}

          {/* Typing Indicator */}
          {loading && (
            <div className="flex gap-3 max-w-md mr-auto items-center animate-in fade-in">
              <div className="w-8 h-8 rounded-xl bg-cyan-600 text-white flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-slate-100 rounded-2xl rounded-tl-none px-4 py-3 text-slate-500 text-xs flex items-center gap-1.5">
                <span className="text-[11px] font-medium mr-1 text-slate-600">MediNLP is analyzing</span>
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-600 typing-dot"></span>
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-600 typing-dot"></span>
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-600 typing-dot"></span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="p-4 border-t border-slate-100 bg-white">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-end gap-2 bg-slate-50 border border-slate-200/80 rounded-2xl p-2 focus-within:border-cyan-600 focus-within:ring-2 focus-within:ring-cyan-600/20 transition-all"
          >
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask a medical question (e.g. 'What is diabetes?', 'Causes of headache')..."
              rows={1}
              className="flex-1 bg-transparent border-none text-xs p-2 text-slate-800 placeholder:text-slate-400 focus:outline-none resize-none max-h-32"
            />
            <button
              type="submit"
              disabled={!inputText.trim() || loading}
              className="p-2.5 rounded-xl bg-cyan-700 hover:bg-cyan-800 text-white disabled:opacity-40 transition-all shadow-xs"
              title="Send message"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>

          <p className="text-[10px] text-slate-400 text-center mt-2">
            Educational assistant only. Not a medical doctor. In severe emergencies, call 911 / 999 / 112 immediately.
          </p>
        </div>
      </section>

      {/* Interactive Feedback Modal */}
      <FeedbackModal
        isOpen={feedbackOpen}
        onClose={() => setFeedbackOpen(false)}
        messageId={feedbackMessageId || undefined}
        conversationId={activeConvId || undefined}
        initialHelpful={isHelpfulState}
      />
    </div>
  );
};

