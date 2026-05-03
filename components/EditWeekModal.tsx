import React, { useState, useEffect } from 'react';

export const hasConsecutiveDays = (daysArray) => {
  if (!daysArray || daysArray.length < 2) return false;

  const dayMap = {
    "Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4,
    "Friday": 5, "Saturday": 6, "Sunday": 7
  };

  const nums = daysArray.map(d => dayMap[d]).sort((a, b) => a - b);
  const extendedNums = [...nums, ...nums.map(n => n + 7)].sort((a, b) => a - b);

  for (let i = 0; i <= extendedNums.length - 2; i++) {
    if (extendedNums[i] + 1 === extendedNums[i+1]) {
      return true;
    }
  }
  return false;
};

export default function EditWeekModal({ isOpen, onClose, initialDays, activePhase, onSave }) {
  const [selectedDays, setSelectedDays] = useState(initialDays || []);
  const [showWarning, setShowWarning] = useState(false);

  const fullBodyPhases = ["foundation", "strength_foundation", "active_lifestyle"];
  const daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

  useEffect(() => {
    // Reset state when modal opens
    if (isOpen) setSelectedDays(initialDays || []);
  }, [isOpen, initialDays]);

  useEffect(() => {
    const isFullBodyPhase = fullBodyPhases.includes(activePhase);
    const hasConsecutive = hasConsecutiveDays(selectedDays);
    
    // Trigger warning if they are in a full body phase AND picked back-to-back days
    setShowWarning(isFullBodyPhase && hasConsecutive);
  }, [selectedDays, activePhase]);

  const toggleDay = (day) => {
    setSelectedDays(prev => 
      prev.includes(day) ? prev.filter(d => d !== day) : [...prev, day]
    );
  };

  const isFrequencyChanging = initialDays && selectedDays.length !== initialDays.length;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-slate-800">Plan Your Week</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 text-2xl leading-none">&times;</button>
        </div>

        <p className="text-sm text-slate-600 mb-6">
          Select between 2 and 7 days to work out. Your protocol will automatically adjust to fit your availability.
        </p>

        <div className="flex flex-wrap gap-2 mb-6 justify-center">
          {daysOfWeek.map(day => (
            <button
              key={day}
              onClick={() => toggleDay(day)}
              className={`px-4 py-2.5 rounded-xl border text-sm font-semibold transition-all ${
                selectedDays.includes(day) 
                  ? 'bg-blue-600 text-white border-blue-600 shadow-md shadow-blue-200' 
                  : 'bg-white text-slate-600 border-slate-200 hover:border-blue-300 hover:bg-blue-50'
              }`}
            >
              {day.slice(0, 3)}
            </button>
          ))}
        </div>

        {/* Dynamic Information Box */}
        <div className="mb-6">
          {selectedDays.length < 2 && (
            <p className="text-sm text-amber-600 font-medium text-center bg-amber-50 py-2 rounded-lg">
              Please select at least 2 days to maintain progress.
            </p>
          )}
          
          {selectedDays.length >= 2 && isFrequencyChanging && !showWarning && (
            <p className="text-sm text-blue-700 font-medium text-center bg-blue-50 py-2 rounded-lg animate-pulse">
              App will regenerate a new {selectedDays.length}-day protocol!
            </p>
          )}
        </div>

        {/* 🚨 THE CNS WARNING POPUP (Unchanged) */}
        {showWarning && (
           <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl mb-6">
             <p className="font-bold flex items-center text-sm">
               ⚠️ 48-Hour Rule Violated
             </p>
             <p className="text-xs mt-1">
               Your current phase uses Heavy Full-Body workouts. Selecting consecutive days blunts recovery. Please add a rest day.
             </p>
           </div>
        )}

        <div className="flex justify-end gap-3 mt-2">
          <button 
            onClick={onClose}
            className="px-5 py-2.5 text-sm font-semibold text-slate-600 bg-slate-100 rounded-xl hover:bg-slate-200 transition-colors"
          >
            Cancel
          </button>
          <button 
            onClick={() => onSave(selectedDays)}
            // Enforce the 2-day minimum rule right here on the button!
            disabled={showWarning || selectedDays.length < 2}
            className={`px-5 py-2.5 text-sm font-semibold text-white rounded-xl transition-all ${
              (showWarning || selectedDays.length < 2) 
                ? 'bg-slate-300 cursor-not-allowed' 
                : 'bg-blue-600 hover:bg-blue-700 shadow-md hover:shadow-lg'
            }`}
          >
            Save Schedule
          </button>
        </div>
      </div>
    </div>
  );
}