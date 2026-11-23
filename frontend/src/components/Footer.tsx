import React from 'react';
import { Stethoscope, Shield, Heart, ExternalLink, AlertOctagon } from 'lucide-react';

export const Footer: React.FC<{ onNavigate: (page: string) => void }> = ({ onNavigate }) => {
  return (
    <footer className="bg-slate-900 text-slate-400 text-sm mt-auto border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-10">
          {/* Brand info */}
          <div className="md:col-span-1 space-y-3">
            <div className="flex items-center gap-2.5 text-white">
              <div className="w-8 h-8 rounded-lg bg-cyan-600 flex items-center justify-center text-white">
                <Stethoscope className="w-5 h-5" />
              </div>
              <span className="font-bold text-lg tracking-tight">MediNLP AI</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Production-grade End-to-End NLP Healthcare Information System. Built with Django REST Framework, React, Scikit-learn, and verified clinical knowledge.
            </p>
            <div className="flex items-center gap-2 text-xs text-cyan-400 font-medium">
              <Shield className="w-3.5 h-3.5" />
              <span>Evidence-Based Information</span>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">System Navigation</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <button onClick={() => onNavigate('landing')} className="hover:text-cyan-400 transition-colors">
                  Home Overview
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('chat')} className="hover:text-cyan-400 transition-colors">
                  Interactive AI Chatbot
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('symptoms')} className="hover:text-cyan-400 transition-colors">
                  Symptom Assessment Tool
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('admin')} className="hover:text-cyan-400 transition-colors">
                  Analytics & Model Metrics
                </button>
              </li>
              <li>
                <button onClick={() => onNavigate('about')} className="hover:text-cyan-400 transition-colors">
                  NLP Architecture & Workflow
                </button>
              </li>
            </ul>
          </div>

          {/* Public Medical References */}
          <div>
            <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider mb-3">Clinical Knowledge Sources</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <a 
                  href="https://www.who.int" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="flex items-center gap-1 hover:text-cyan-400 transition-colors"
                >
                  World Health Organization (WHO) <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://medlineplus.gov" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="flex items-center gap-1 hover:text-cyan-400 transition-colors"
                >
                  MedlinePlus (NIH National Library) <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://www.nhs.uk/conditions/" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="flex items-center gap-1 hover:text-cyan-400 transition-colors"
                >
                  NHS Health A to Z <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
              <li>
                <a 
                  href="https://www.cdc.gov" 
                  target="_blank" 
                  rel="noreferrer" 
                  className="flex items-center gap-1 hover:text-cyan-400 transition-colors"
                >
                  Centers for Disease Control (CDC) <ExternalLink className="w-3 h-3 text-slate-500" />
                </a>
              </li>
            </ul>
          </div>

          {/* Emergency Crisis Contact */}
          <div className="bg-slate-800/60 p-4 rounded-xl border border-slate-700/60 space-y-2.5">
            <div className="flex items-center gap-2 text-red-400 font-semibold text-xs">
              <AlertOctagon className="w-4 h-4 shrink-0" />
              <span>Emergency Warning</span>
            </div>
            <p className="text-[11px] leading-relaxed text-slate-300">
              If you are experiencing severe chest pain, sudden numbness, breathing distress, or acute trauma, dial emergency services immediately (911 / 999 / 112).
            </p>
            <div className="pt-1 text-[11px] text-slate-400">
              Suicide & Crisis Helpline: <strong className="text-white">988</strong> (USA/Canada)
            </div>
          </div>
        </div>

        {/* Bottom Disclaimer Banner */}
        <div className="pt-8 border-t border-slate-800 text-[11px] leading-relaxed text-slate-400 flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="max-w-4xl text-left">
            <strong>Legal & Medical Disclaimer:</strong> MediNLP AI is an academic and portfolio healthcare information assistant. It utilizes Machine Learning and Natural Language Processing to assist users with general wellness and educational queries. It does NOT provide clinical diagnoses, formal triage, or drug prescriptions. Always seek the advice of a qualified physician or healthcare provider.
          </p>
          <div className="flex items-center gap-1 text-slate-400 text-xs shrink-0">
            <span>Built with</span>
            <Heart className="w-3.5 h-3.5 text-rose-500 fill-rose-500" />
            <span>AI/ML Portfolio Project</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

