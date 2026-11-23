import React, { useState, useEffect } from 'react';
import { 
  Stethoscope, 
  Search, 
  Plus, 
  X, 
  AlertTriangle, 
  ShieldCheck, 
  BookOpen, 
  Activity, 
  ArrowRight, 
  CheckCircle2,
  HelpCircle,
  PhoneCall
} from 'lucide-react';
import { medicalApi, type SymptomAnalysisResult } from '../api/medical';

interface SymptomPageProps {
  onNavigate: (page: string) => void;
  onConsultBot: (query: string) => void;
}

export const SymptomPage: React.FC<SymptomPageProps> = ({ onNavigate, onConsultBot }) => {
  const [availableSymptoms, setAvailableSymptoms] = useState<string[]>([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [searchFilter, setSearchFilter] = useState<string>('');
  const [freeText, setFreeText] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [analysisResult, setAnalysisResult] = useState<SymptomAnalysisResult | null>(null);

  useEffect(() => {
    const fetchDictionary = async () => {
      try {
        const data = await medicalApi.getSymptomDictionary();
        setAvailableSymptoms(data.symptoms || []);
      } catch (err) {
        console.error("Failed to load symptom dictionary", err);
      }
    };
    fetchDictionary();
  }, []);

  const addSymptom = (sym: string) => {
    if (!selectedSymptoms.includes(sym)) {
      setSelectedSymptoms([...selectedSymptoms, sym]);
    }
  };

  const removeSymptom = (sym: string) => {
    setSelectedSymptoms(selectedSymptoms.filter(s => s !== sym));
  };

  const handleAnalyze = async () => {
    if (selectedSymptoms.length === 0 && !freeText.trim()) return;

    setLoading(true);
    try {
      const res = await medicalApi.analyzeSymptoms(selectedSymptoms, freeText);
      setAnalysisResult(res);
    } catch (err) {
      console.error("Analysis failed", err);
    } finally {
      setLoading(false);
    }
  };

  const filteredList = availableSymptoms.filter(s => 
    s.toLowerCase().includes(searchFilter.toLowerCase()) && !selectedSymptoms.includes(s)
  );

  return (
    <div className="space-y-8 py-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="text-center space-y-2 max-w-2xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-cyan-50 border border-cyan-200 text-cyan-800 text-xs font-semibold">
          <Stethoscope className="w-3.5 h-3.5 text-cyan-600" />
          <span>Educational Symptom Explorer</span>
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          Explore Symptom Associations & Red Flags
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 leading-relaxed">
          Select or describe symptoms you are experiencing to review verified educational health profiles, physiological warning signs, and recommendations. <strong>This tool never provides a medical diagnosis.</strong>
        </p>
      </div>

      {/* Main Interactive Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Symptom Selector */}
        <div className="lg:col-span-5 bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-5">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Search className="w-4 h-4 text-cyan-600" />
            1. Select or Search Symptoms
          </h3>

          {/* Search box */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
            <input
              type="text"
              value={searchFilter}
              onChange={(e) => setSearchFilter(e.target.value)}
              placeholder="Search symptoms (e.g. fever, headache, cough)..."
              className="w-full text-xs pl-9 pr-3 py-2.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600"
            />
          </div>

          {/* Available Symptoms Pill Cloud */}
          <div className="space-y-1.5">
            <p className="text-[11px] font-semibold text-slate-500">Known Clinical Symptoms:</p>
            <div className="flex flex-wrap gap-1.5 max-h-48 overflow-y-auto p-1 border border-slate-100 rounded-xl bg-slate-50/50">
              {filteredList.slice(0, 30).map((sym, idx) => (
                <button
                  key={idx}
                  onClick={() => addSymptom(sym)}
                  className="text-[11px] px-2.5 py-1 rounded-lg bg-white hover:bg-cyan-50 border border-slate-200 hover:border-cyan-400 text-slate-700 transition-colors flex items-center gap-1 group"
                >
                  <span>{sym}</span>
                  <Plus className="w-3 h-3 text-slate-400 group-hover:text-cyan-600" />
                </button>
              ))}
            </div>
          </div>

          {/* Selected Symptoms */}
          <div className="space-y-1.5 pt-2 border-t border-slate-100">
            <div className="flex justify-between items-center text-[11px]">
              <span className="font-semibold text-slate-700">Selected Symptoms ({selectedSymptoms.length})</span>
              {selectedSymptoms.length > 0 && (
                <button
                  onClick={() => setSelectedSymptoms([])}
                  className="text-slate-400 hover:text-red-600 transition-colors"
                >
                  Clear all
                </button>
              )}
            </div>

            {selectedSymptoms.length === 0 ? (
              <p className="text-xs text-slate-400 italic py-2">No symptoms selected yet.</p>
            ) : (
              <div className="flex flex-wrap gap-1.5 pt-1">
                {selectedSymptoms.map((sym, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-lg bg-cyan-50 text-cyan-800 border border-cyan-200"
                  >
                    {sym}
                    <button
                      onClick={() => removeSymptom(sym)}
                      className="text-cyan-600 hover:text-cyan-900 rounded"
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Optional Free Text Description */}
          <div className="space-y-1.5 pt-2 border-t border-slate-100">
            <label className="text-[11px] font-semibold text-slate-700 block">
              2. Additional Details / How are you feeling?
            </label>
            <textarea
              value={freeText}
              onChange={(e) => setFreeText(e.target.value)}
              placeholder="e.g., 'Throbbing headache on one side of head since yesterday morning with mild nausea'..."
              rows={3}
              className="w-full text-xs p-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600 resize-none"
            />
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading || (selectedSymptoms.length === 0 && !freeText.trim())}
            className="w-full py-3 rounded-xl font-semibold text-xs text-white bg-cyan-700 hover:bg-cyan-800 disabled:opacity-40 transition-all shadow-xs flex items-center justify-center gap-2"
          >
            <Activity className="w-4 h-4" />
            {loading ? "Analyzing Medical Correlations..." : "Analyze Symptoms"}
          </button>
        </div>

        {/* Right Column: Educational Insights Result */}
        <div className="lg:col-span-7 space-y-4">
          {!analysisResult ? (
            <div className="bg-white rounded-3xl p-10 border border-slate-200 shadow-xs text-center space-y-4 h-full flex flex-col justify-center items-center">
              <div className="w-16 h-16 rounded-2xl bg-cyan-50 text-cyan-600 flex items-center justify-center">
                <Stethoscope className="w-8 h-8" />
              </div>
              <div className="space-y-1 max-w-sm">
                <h3 className="text-base font-bold text-slate-800">No Assessment Run Yet</h3>
                <p className="text-xs text-slate-500 leading-relaxed">
                  Select one or more symptoms from the left panel or type your sensations, then click <strong>Analyze Symptoms</strong> to view educational condition profiles.
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4 animate-in fade-in duration-200">
              {/* Emergency Alert Banner */}
              {analysisResult.is_emergency && (
                <div className="p-5 rounded-2xl bg-red-600 text-white shadow-lg space-y-2">
                  <div className="flex items-center gap-2 font-bold text-sm">
                    <AlertTriangle className="w-5 h-5" />
                    <span>CRITICAL RED-FLAG ALERT</span>
                  </div>
                  <p className="text-xs text-red-100 leading-relaxed">
                    {analysisResult.emergency_message}
                  </p>
                  <div className="pt-2 flex items-center gap-2 text-xs font-semibold text-white">
                    <PhoneCall className="w-4 h-4" />
                    <span>Emergency Numbers: 911 (US/CA) | 999 (UK) | 112 (EU)</span>
                  </div>
                </div>
              )}

              {/* Guidance & Disclaimer Notice */}
              <div className="p-4 rounded-2xl bg-cyan-50/70 border border-cyan-200 text-xs text-cyan-950 space-y-1">
                <p className="font-semibold">{analysisResult.general_guidance}</p>
                <p className="text-[11px] text-cyan-800 italic">{analysisResult.disclaimer}</p>
              </div>

              {/* Matched Educational Conditions */}
              <div className="space-y-3">
                <h3 className="text-sm font-bold text-slate-900 flex items-center gap-1.5">
                  <BookOpen className="w-4 h-4 text-cyan-600" />
                  Related Medical Topics Sharing These Symptoms ({analysisResult.identified_conditions.length})
                </h3>

                {analysisResult.identified_conditions.length === 0 ? (
                  <div className="p-6 bg-white rounded-2xl border border-slate-200 text-center text-xs text-slate-500">
                    No single condition directly matches this specific combination in our standard database. Consult a physician for accurate diagnostic tests.
                  </div>
                ) : (
                  analysisResult.identified_conditions.map((item, idx) => (
                    <div
                      key={idx}
                      className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-3"
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <div className="flex items-center gap-2">
                            <h4 className="text-sm font-bold text-slate-900">{item.topic}</h4>
                            <span className="text-[10px] font-semibold bg-slate-100 text-slate-600 px-2 py-0.5 rounded-full">
                              {item.category}
                            </span>
                          </div>
                          <p className="text-xs text-slate-600 mt-1 leading-relaxed">{item.description}</p>
                        </div>
                      </div>

                      {/* Matching Symptoms Pills */}
                      <div className="space-y-1">
                        <span className="text-[10px] font-semibold text-slate-500">Matching symptoms detected:</span>
                        <div className="flex flex-wrap gap-1">
                          {item.matching_symptoms.map((ms, i) => (
                            <span key={i} className="text-[10px] font-medium bg-amber-50 text-amber-900 border border-amber-200 px-2 py-0.5 rounded-md">
                              ✓ {ms}
                            </span>
                          ))}
                        </div>
                      </div>

                      {/* Red Flags / When to seek care */}
                      <div className="p-3 rounded-xl bg-amber-50/60 border border-amber-200/80 text-[11px] text-amber-950 space-y-1">
                        <strong className="text-amber-900 flex items-center gap-1 font-semibold">
                          <AlertTriangle className="w-3.5 h-3.5 text-amber-700" />
                          When to Seek Medical Evaluation:
                        </strong>
                        <p>{item.when_to_seek_care}</p>
                      </div>

                      {/* Ask Bot button */}
                      <div className="pt-1 flex justify-end">
                        <button
                          onClick={() => onConsultBot(`Tell me more about ${item.topic} and its symptoms`)}
                          className="text-xs font-semibold text-cyan-700 hover:text-cyan-900 flex items-center gap-1"
                        >
                          <span>Ask AI Assistant about {item.topic}</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Recommended Next Actions */}
              <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-2">
                <h4 className="text-xs font-bold text-slate-900 flex items-center gap-1.5">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  Recommended Next Steps:
                </h4>
                <ul className="space-y-1.5 text-xs text-slate-600">
                  {analysisResult.recommended_actions.map((act, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-cyan-600 mt-1.5 shrink-0"></span>
                      <span>{act}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

