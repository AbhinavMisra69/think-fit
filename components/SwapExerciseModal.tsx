import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner'; 
import { RefreshCw, X, Loader2 } from 'lucide-react';

interface ExerciseOption {
  exercise_name?: string;
  name?: string;
  facility_requirements?: {
    facility_tier: string;
  };
  muscle_data?: {
    is_compound: boolean;
    primary_targets: string[];
  };
}

interface SwapExerciseModalProps {
  isOpen: boolean;
  onClose: () => void;
  userId: string;
  dayKey: string; // e.g., "Day_1"
  originalExerciseName: string;
}

export default function SwapExerciseModal({ isOpen, onClose, userId, dayKey, originalExerciseName }: SwapExerciseModalProps) {
  const router = useRouter();
  const [options, setOptions] = useState<ExerciseOption[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSwapping, setIsSwapping] = useState(false);

  useEffect(() => {
    if (!isOpen || !originalExerciseName) return;

    const fetchOptions = async () => {
      setIsLoading(true);
      try {
        const res = await fetch(`http://localhost:5001/api/workout/swap_options?user_id=${userId}&exercise=${encodeURIComponent(originalExerciseName)}`);
        const data = await res.json();
        if (data.status === "success") {
          setOptions(data.options);
        }
      } catch (error) {
        console.error("Failed to fetch swap options:", error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchOptions();
  }, [isOpen, originalExerciseName, userId]);

  const handleSwap = async (newExercise: ExerciseOption) => {
    setIsSwapping(true);
    try {
      const res = await fetch(`http://localhost:5001/api/workout/apply_swap`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          day_key: dayKey,
          old_exercise: originalExerciseName,
          new_exercise: newExercise
        })
      });

      const data = await res.json();
      if (data.status === "success") {
        toast.success(data.message);
        onClose();
        setTimeout(() => {
          window.location.reload();
        }, 800);
      } else {
        toast.error(data.message || "Failed to swap exercise.");
      }
    } catch (error) {
      toast.error("Network error occurred.");
    } finally {
      setIsSwapping(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 overflow-hidden flex flex-col max-h-[80vh]">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-slate-800 flex items-center gap-2">
            <RefreshCw className="w-5 h-5 text-blue-600" />
            Swap Exercise
          </h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600"><X /></button>
        </div>

        <p className="text-sm text-slate-500 mb-4">
          Finding alternatives for <span className="font-semibold text-slate-700">{originalExerciseName}</span> targeting the same muscle groups.
        </p>

        <div className="flex-1 overflow-y-auto space-y-3 pr-2">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-10 text-slate-400">
              <Loader2 className="w-8 h-8 animate-spin mb-2" />
              <p className="text-sm font-medium">Scanning biomechanics...</p>
            </div>
          ) : options.length === 0 ? (
            <div className="text-center py-8 text-slate-500 bg-slate-50 rounded-xl border border-slate-100">
              No suitable alternatives found with your current equipment.
            </div>
          ) : (
            options.map((opt, i) => (
              <button
              key={i}
              onClick={() => handleSwap(opt)}
              disabled={isSwapping}
              className="w-full text-left p-4 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50 transition-all group flex justify-between items-center"
            >
              <div>
                {/* 🎯 FIX 1: Look for exercise_name instead of name */}
                <h4 className="font-bold text-slate-800 group-hover:text-blue-700">
                  {opt.exercise_name || opt.name}
                </h4>
                
                {/* 🎯 FIX 2: Dig into the nested JSON for equipment and mechanics */}
                <p className="text-xs text-slate-500 mt-1 capitalize">
                  {opt.facility_requirements?.facility_tier?.replace(/_/g, ' ') || 'Standard'} • 
                  {opt.muscle_data?.is_compound ? ' Compound' : ' Isolation'}
                </p>
              </div>
              <div className="text-xs font-semibold text-blue-600 bg-blue-100 px-3 py-1 rounded-full opacity-0 group-hover:opacity-100 transition-opacity">
                Select
              </div>
            </button>
          )))}
        </div>
      </div>
    </div>
  );
}