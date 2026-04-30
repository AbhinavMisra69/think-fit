'use client';

import React, { useState } from 'react';
import { Dumbbell, Info, CheckCircle2, CircleDashed, ChevronRight } from 'lucide-react';

type SetData = {
  id: number;
  reps: string;
  weight: string;
  isDropset: boolean;
  dropEndWeight: string;
};

export default function ExerciseCard() {
  // Initialize 3 empty sets
  const [sets, setSets] = useState<SetData[]>([
    { id: 1, reps: '', weight: '', isDropset: false, dropEndWeight: '' },
    { id: 2, reps: '', weight: '', isDropset: false, dropEndWeight: '' },
    { id: 3, reps: '', weight: '', isDropset: false, dropEndWeight: '' },
  ]);

  // Handle number-only inputs
  const handleInputChange = (id: number, field: keyof SetData, value: string) => {
    // Strip out any non-numeric characters (allowing decimals if needed, but keeping it simple with digits)
    const numericValue = value.replace(/[^0-9]/g, '');
    
    setSets(prev => prev.map(set => 
      set.id === id ? { ...set, [field]: numericValue } : set
    ));
  };

  const toggleDropset = (id: number) => {
    setSets(prev => prev.map(set => 
      set.id === id ? { ...set, isDropset: !set.isDropset, dropEndWeight: '' } : set
    ));
  };

  // Evaluate the completion status of the exercise
  const getStatus = () => {
    let filledSets = 0;
    
    sets.forEach(set => {
      const hasBasicData = set.reps !== '' && set.weight !== '';
      const hasDropsetData = set.isDropset ? set.dropEndWeight !== '' : true;
      
      // A set is 'filled' if it has reps, weight, and the drop weight (if dropset is active)
      if (hasBasicData && hasDropsetData) {
        filledSets += 1;
      }
    });

    if (filledSets === 0) return { label: 'Not Done', style: 'bg-zinc-100 text-zinc-500', icon: <CircleDashed className="w-4 h-4" /> };
    if (filledSets > 0 && filledSets < sets.length) return { label: 'Partially Done', style: 'bg-amber-100 text-amber-700', icon: <CircleDashed className="w-4 h-4" /> };
    return { label: 'Completed', style: 'bg-blue-600 text-white shadow-md', icon: <CheckCircle2 className="w-4 h-4" /> };
  };

  const status = getStatus();

  return (
    <div className="w-full bg-white border border-zinc-200 rounded-2xl shadow-sm overflow-hidden font-sans">
      
      {/* Top Header */}
      <div className="bg-slate-50 border-b border-zinc-100 px-5 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Dumbbell className="w-5 h-5 text-blue-600" />
          </div>
          <h3 className="font-semibold text-lg text-slate-800 tracking-tight">Dumbell Lateral Raise</h3>
        </div>
      </div>

      <div className="p-5 flex flex-col md:flex-row gap-6">
        
        {/* Left Side: Infographic Placeholder */}
        <div className="w-full md:w-1/3 shrink-0 flex flex-col gap-2">
          <div className="aspect-square bg-slate-100 rounded-xl border border-slate-200 overflow-hidden flex items-center justify-center relative">
            {/* Replace this img src with your actual infographic later */}
            <img 
              src="/Dumbbell-Lateral-Raise.gif" 
              alt="Exercise visualization" 
              className="w-full h-full object-cover opacity-90 mix-blend-multiply"
            />
            
          </div>
        </div>

        {/* Right Side: Tips and Logging */}
        <div className="w-full md:w-2/3 flex flex-col">
          
          {/* Tips Section */}
          <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-4 mb-6">
            <div className="flex items-center gap-2 mb-1">
              <Info className="w-4 h-4 text-blue-500" />
              <h4 className="font-medium text-blue-900 text-sm">Form Recommendation</h4>
            </div>
            <p className="text-sm text-slate-600 leading-relaxed">
              Keep your front knee aligned with your toes.
            </p>
          </div>

          {/* Sets Tracking */}
          <div className="space-y-3 mb-6">
            {/* Table Headers */}
            <div className="flex items-center px-2 text-xs font-semibold text-slate-400 tracking-wider uppercase">
              <div className="w-10">Set</div>
              <div className="w-20 text-center">Reps</div>
              <div className="flex-1 px-4">Weight (kg)</div>
              <div className="w-20 text-center">Dropset</div>
            </div>

            {/* Set Rows */}
            {sets.map((set, index) => (
              <div key={set.id} className="flex items-center bg-slate-50 border border-slate-100 rounded-lg p-2 transition-colors focus-within:bg-white focus-within:border-blue-200 focus-within:shadow-sm">
                
                {/* Set Number */}
                <div className="w-10 flex justify-center">
                  <span className="font-medium text-slate-500">{index + 1}</span>
                </div>

                {/* Reps Input */}
                <div className="w-20">
                  <input
                    type="text"
                    inputMode="numeric"
                    placeholder="0"
                    value={set.reps}
                    onChange={(e) => handleInputChange(set.id, 'reps', e.target.value)}
                    className="w-full text-center bg-transparent font-semibold text-slate-700 outline-none placeholder:text-slate-300"
                  />
                </div>

                {/* Weight Input(s) */}
                <div className="flex-1 flex items-center justify-center px-2">
                  <input
                    type="text"
                    inputMode="numeric"
                    placeholder="Start"
                    value={set.weight}
                    onChange={(e) => handleInputChange(set.id, 'weight', e.target.value)}
                    className="w-16 text-center bg-white border border-slate-200 rounded-md py-1 font-medium text-slate-700 outline-none focus:border-blue-400 placeholder:text-slate-300 placeholder:font-normal"
                  />
                  
                  {/* Dynamic Dropset Reveal */}
                  {set.isDropset && (
                    <div className="flex items-center animate-in fade-in slide-in-from-left-2 duration-200">
                      <ChevronRight className="w-4 h-4 mx-1 text-slate-400" />
                      <input
                        type="text"
                        inputMode="numeric"
                        placeholder="End"
                        value={set.dropEndWeight}
                        onChange={(e) => handleInputChange(set.id, 'dropEndWeight', e.target.value)}
                        className="w-16 text-center bg-white border border-orange-200 rounded-md py-1 font-medium text-orange-700 outline-none focus:border-orange-400 placeholder:text-orange-300 placeholder:font-normal"
                      />
                    </div>
                  )}
                </div>

                {/* Dropset Checkbox */}
                <div className="w-20 flex justify-center">
                  <input 
                    type="checkbox" 
                    checked={set.isDropset}
                    onChange={() => toggleDropset(set.id)}
                    className="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500 accent-blue-600 cursor-pointer"
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Dynamic Status Button */}
          <div className="mt-auto">
            <button 
              className={`w-full py-3 rounded-xl flex items-center justify-center gap-2 font-semibold transition-all duration-300 ${status.style}`}
            >
              {status.icon}
              {status.label}
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}