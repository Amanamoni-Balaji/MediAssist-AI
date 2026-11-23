import React, { useState } from 'react';
import { Star, ThumbsUp, ThumbsDown, X, CheckCircle2 } from 'lucide-react';
import { feedbackApi } from '../api/feedback';

interface FeedbackModalProps {
  isOpen: boolean;
  onClose: () => void;
  messageId?: string;
  conversationId?: string;
  initialHelpful?: boolean;
}

export const FeedbackModal: React.FC<FeedbackModalProps> = ({
  isOpen,
  onClose,
  messageId,
  conversationId,
  initialHelpful = true,
}) => {
  const [isHelpful, setIsHelpful] = useState<boolean>(initialHelpful);
  const [rating, setRating] = useState<number>(5);
  const [hoverRating, setHoverRating] = useState<number>(0);
  const [comment, setComment] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);
  const [submitted, setSubmitted] = useState<boolean>(false);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await feedbackApi.submit({
        message: messageId,
        conversation: conversationId,
        is_helpful: isHelpful,
        rating,
        comment: comment.trim(),
      });
      setSubmitted(true);
      setTimeout(() => {
        setSubmitted(false);
        onClose();
      }, 1500);
    } catch (err) {
      console.error("Failed to submit feedback", err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-in fade-in duration-150">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-100 max-w-md w-full p-6 relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-slate-400 hover:text-slate-600 p-1 rounded-lg"
        >
          <X className="w-5 h-5" />
        </button>

        {submitted ? (
          <div className="py-8 text-center space-y-3">
            <CheckCircle2 className="w-12 h-12 text-emerald-500 mx-auto animate-bounce" />
            <h3 className="text-lg font-semibold text-slate-900">Thank you for your feedback!</h3>
            <p className="text-xs text-slate-500">Your review helps improve our NLP healthcare intelligence models.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <h3 className="text-base font-semibold text-slate-900">Rate this AI Medical Response</h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Was this information clear, accurate, and educational?
              </p>
            </div>

            {/* Helpful / Not Helpful Toggle */}
            <div className="flex gap-2.5">
              <button
                type="button"
                onClick={() => setIsHelpful(true)}
                className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl border text-xs font-medium transition-all ${
                  isHelpful
                    ? 'border-cyan-600 bg-cyan-50 text-cyan-800 shadow-xs'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <ThumbsUp className="w-4 h-4" />
                Helpful
              </button>
              <button
                type="button"
                onClick={() => setIsHelpful(false)}
                className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xl border text-xs font-medium transition-all ${
                  !isHelpful
                    ? 'border-rose-500 bg-rose-50 text-rose-800 shadow-xs'
                    : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <ThumbsDown className="w-4 h-4" />
                Not Helpful
              </button>
            </div>

            {/* Star Rating */}
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-700">Quality Rating (1 to 5 Stars):</label>
              <div className="flex items-center gap-1.5">
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setRating(star)}
                    onMouseEnter={() => setHoverRating(star)}
                    onMouseLeave={() => setHoverRating(0)}
                    className="p-1 focus:outline-none transition-transform hover:scale-110"
                  >
                    <Star
                      className={`w-6 h-6 ${
                        (hoverRating || rating) >= star
                          ? 'text-amber-400 fill-amber-400'
                          : 'text-slate-200'
                      }`}
                    />
                  </button>
                ))}
                <span className="text-xs font-semibold text-slate-600 ml-2">
                  {rating} of 5
                </span>
              </div>
            </div>

            {/* Written feedback comment */}
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-slate-700">Additional Comments (Optional):</label>
              <textarea
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="What could be improved or clarified in this medical explanation?"
                rows={3}
                className="w-full text-xs p-3 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-cyan-600/20 focus:border-cyan-600 resize-none text-slate-800 placeholder:text-slate-400"
              />
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-2 pt-2">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl text-xs font-medium text-slate-600 hover:bg-slate-100"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={submitting}
                className="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-cyan-700 hover:bg-cyan-800 disabled:opacity-50 transition-colors shadow-xs"
              >
                {submitting ? 'Submitting...' : 'Submit Feedback'}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

