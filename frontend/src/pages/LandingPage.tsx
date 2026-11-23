import React from 'react';
import { 
  Bot, 
  Stethoscope, 
  ShieldCheck, 
  Cpu, 
  Brain, 
  Activity, 
  Sparkles, 
  ArrowRight, 
  Search, 
  CheckCircle2, 
  AlertTriangle,
  BookOpen,
  Layers,
  HeartPulse
} from 'lucide-react';

interface LandingPageProps {
  onNavigate: (page: string) => void;
  onQuickChat: (query: string) => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onNavigate, onQuickChat }) => {
  const sampleQueries = [
    "What is hypertension and how is it managed?",
    "What are the common symptoms of fever?",
    "What is the difference between a cold and asthma?",
    "What are the symptoms and causes of dehydration?",
    "How does a balanced diet protect heart health?"
  ];

  const features = [
    {
      icon: Brain,
      title: "TF-IDF & Calibrated NLP Pipeline",
      description: "Classifies user intent using calibrated machine learning (Logistic Regression / Linear SVM) with tokenization, lemmatization, and negation preservation."
    },
    {
      icon: Search,
      title: "Cosine Similarity Information Retrieval",
      description: "Retrieves verified educational healthcare knowledge by calculating vector similarity against structured public medical datasets from WHO, MedlinePlus, and NHS."
    },
    {
      icon: ShieldCheck,
      title: "Automated Red-Flag & Emergency Triage",
      description: "Built-in safety protocols detect life-threatening warning signs (chest pain, stroke signs, dyspnea) and immediately advise contacting emergency services."
    },
    {
      icon: Activity,
      title: "Interactive Symptom Educational Guide",
      description: "Allows multi-symptom exploration with condition correlation scoring, warning signs checklist, and clinical consultation recommendations."
    }
  ];

  const medicalTopics = [
    "Type 2 Diabetes", "Hypertension", "Asthma", "Fever", 
    "Common Cold", "Tension Headache", "Migraine", "Dehydration",
    "Iron-Deficiency Anemia", "Obesity & Weight", "Cardiovascular Health",
    "Digestive Health (GERD)", "General Nutrition", "Mental Wellness"
  ];

  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-6 pb-12">
        <div className="max-w-5xl mx-auto text-center space-y-6">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-800 text-xs font-semibold shadow-xs">
            <Sparkles className="w-3.5 h-3.5 text-cyan-600" />
            <span>Next-Gen NLP Healthcare Intelligence</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.15]">
            Evidence-Based AI <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-600 to-blue-700">Medical Knowledge</span> Assistant
          </h1>

          <p className="text-base sm:text-lg text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Interact with an end-to-end NLP medical assistant. Understand symptoms, explore clinical conditions, and discover preventive lifestyle habits backed by WHO, MedlinePlus, and NHS.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
            <button
              onClick={() => onNavigate('chat')}
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-white bg-cyan-700 hover:bg-cyan-800 shadow-md hover:shadow-lg transition-all"
            >
              <Bot className="w-5 h-5" />
              Start AI Consultation
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigate('symptoms')}
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-slate-700 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 shadow-xs transition-all"
            >
              <Stethoscope className="w-5 h-5 text-cyan-600" />
              Explore Symptoms
            </button>
            <button
              onClick={() => onNavigate('admin')}
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl font-semibold text-slate-700 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 shadow-xs transition-all"
            >
              <Activity className="w-5 h-5 text-blue-600" />
              Model Analytics
            </button>
          </div>

          {/* Quick prompt launcher */}
          <div className="pt-6">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2.5">
              Click to Ask Assistant:
            </p>
            <div className="flex flex-wrap items-center justify-center gap-2 max-w-3xl mx-auto">
              {sampleQueries.map((q, idx) => (
                <button
                  key={idx}
                  onClick={() => onQuickChat(q)}
                  className="text-xs px-3.5 py-1.5 rounded-lg bg-white border border-slate-200 hover:border-cyan-500 hover:text-cyan-700 text-slate-600 shadow-xs transition-colors flex items-center gap-1.5"
                >
                  <Search className="w-3 h-3 text-cyan-600" />
                  {q}
                </button>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Safety & Responsible AI Banner */}
      <section className="bg-gradient-to-r from-blue-900 to-slate-900 text-white rounded-3xl p-8 max-w-5xl mx-auto shadow-xl">
        <div className="flex flex-col md:flex-row items-center gap-6">
          <div className="w-14 h-14 rounded-2xl bg-white/10 flex items-center justify-center shrink-0 border border-white/20">
            <ShieldCheck className="w-8 h-8 text-cyan-400" />
          </div>
          <div className="space-y-1.5 text-center md:text-left flex-1">
            <h3 className="text-lg font-bold text-white flex items-center justify-center md:justify-start gap-2">
              Responsible AI & Medical Ethics Standards
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              This application strictly serves as an educational and preventive health assistant. It never claims to diagnose clinical illnesses, prescribe pharmacological agents, or supersede professional healthcare examination. Life-threatening emergency inquiries immediately trigger emergency hotline guidance.
            </p>
          </div>
          <button
            onClick={() => onNavigate('about')}
            className="px-4 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-semibold shrink-0 transition-colors"
          >
            Read Ethics Policy
          </button>
        </div>
      </section>

      {/* Core Architecture Features */}
      <section className="max-w-6xl mx-auto">
        <div className="text-center space-y-2 mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
            Engineered with Genuine AI & NLP
          </h2>
          <p className="text-sm text-slate-500 max-w-xl mx-auto">
            Decoupled backend service architecture delivering high-accuracy retrieval and calibrated intent classification.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div 
                key={idx}
                className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow flex items-start gap-4"
              >
                <div className="w-12 h-12 rounded-xl bg-cyan-50 text-cyan-700 flex items-center justify-center shrink-0 border border-cyan-100">
                  <Icon className="w-6 h-6" />
                </div>
                <div className="space-y-1.5">
                  <h4 className="text-base font-bold text-slate-900">{feat.title}</h4>
                  <p className="text-xs text-slate-600 leading-relaxed">{feat.description}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* 7-Step NLP Workflow Interactive Pipeline Diagram */}
      <section className="bg-slate-100/70 py-12 px-6 rounded-3xl max-w-6xl mx-auto border border-slate-200">
        <div className="text-center space-y-2 mb-8">
          <span className="text-xs font-semibold text-cyan-700 uppercase tracking-wider">Under The Hood</span>
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
            The 7-Stage End-to-End NLP Pipeline
          </h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-7 gap-3 text-center">
          {[
            { step: "01", title: "User Query", desc: "Receives raw medical inquiry" },
            { step: "02", title: "Preprocessing", desc: "Lowercasing, NLTK Lemmatization & negation retention" },
            { step: "03", title: "Emergency Gate", desc: "Regex triage rules detect life-threatening alerts" },
            { step: "04", title: "TF-IDF Matrix", desc: "Generates unigram to trigram numerical feature vectors" },
            { step: "05", title: "Intent & NER", desc: "Calibrated classification + Medical entity extractor" },
            { step: "06", title: "Cosine Sim", desc: "Vector similarity ranking against clinical knowledge" },
            { step: "07", title: "Safety Validation", desc: "Injects clinical disclaimer and follow-up prompts" },
          ].map((item, i) => (
            <div key={i} className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1 relative">
              <span className="text-[10px] font-bold text-cyan-600 bg-cyan-50 px-2 py-0.5 rounded-full inline-block">
                Step {item.step}
              </span>
              <h4 className="text-xs font-bold text-slate-800">{item.title}</h4>
              <p className="text-[11px] text-slate-500 leading-tight">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Covered Medical Knowledge Topics */}
      <section className="max-w-6xl mx-auto space-y-6">
        <div className="text-center space-y-2">
          <h2 className="text-2xl sm:text-3xl font-bold text-slate-900">
            Comprehensive Medical Knowledge Base
          </h2>
          <p className="text-sm text-slate-500 max-w-xl mx-auto">
            14 verified healthcare topics curated from WHO, MedlinePlus, and NHS guidelines.
          </p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-3">
          {medicalTopics.map((topic, i) => (
            <button
              key={i}
              onClick={() => onQuickChat(`What is ${topic}?`)}
              className="p-3 bg-white rounded-xl border border-slate-200 hover:border-cyan-500 hover:shadow-xs transition-all text-center space-y-1.5 group"
            >
              <div className="w-8 h-8 mx-auto rounded-lg bg-cyan-50 text-cyan-700 flex items-center justify-center group-hover:bg-cyan-600 group-hover:text-white transition-colors">
                <HeartPulse className="w-4 h-4" />
              </div>
              <p className="text-xs font-semibold text-slate-800 group-hover:text-cyan-700 transition-colors">
                {topic}
              </p>
            </button>
          ))}
        </div>
      </section>

      {/* CTA Bottom Banner */}
      <section className="bg-white rounded-3xl p-8 max-w-4xl mx-auto border border-slate-200 shadow-sm text-center space-y-4">
        <h3 className="text-2xl font-bold text-slate-900">
          Ready to test the Medical NLP Chatbot?
        </h3>
        <p className="text-xs sm:text-sm text-slate-600 max-w-md mx-auto">
          Start a real-time conversation, check symptoms, review past chat logs, and inspect real-time classification metrics.
        </p>
        <button
          onClick={() => onNavigate('chat')}
          className="px-6 py-3 rounded-xl font-semibold text-white bg-cyan-700 hover:bg-cyan-800 shadow-md transition-all inline-flex items-center gap-2 text-sm"
        >
          <Bot className="w-4 h-4" />
          Launch Medical Assistant Now
        </button>
      </section>
    </div>
  );
};

