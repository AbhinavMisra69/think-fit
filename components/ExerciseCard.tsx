'use client';

import React, { useState } from 'react';
import { Dumbbell, Info, CheckCircle2, CircleDashed, ChevronRight } from 'lucide-react';

// 1. Define the exact shape of the data coming from your Python dataset
export type ExerciseData = {
  exercise_id: string;
  exercise_name: string;
  youtube_id: string;
  description?: string;
  card_image?: string;
  muscle_data: {
    primary_targets: string[];
    secondary_muscles: string[];
    movement_pattern: string;
    is_compound: boolean;
  };
  facility_requirements: {
    facility_tier: string;
    specific_tools: string[];
  };
  biomechanics: {
    joint_stress: string[];
    pre_hab_for: string[];
  };
  periodization_tags: {
    allowed_phases: string[];
    hypertrophy_tiers: Record<string, string>; // This handles the dynamic "glutes": "S_Plus" mapping
  };
};

// 2. Tell the Component to expect this data
export default function ExerciseCard({ exercise , onOpenDetails }: { exercise: ExerciseData ; onOpenDetails: () => void; }) {
  const [sets, setSets] = useState([
    { id: 1, reps: '', weight: '', isDropset: false, dropEndWeight: '' },
    { id: 2, reps: '', weight: '', isDropset: false, dropEndWeight: '' },
    { id: 3, reps: '', weight: '', isDropset: false, dropEndWeight: '' },
  ]);

  const handleInputChange = (id: number, field: string, value: string) => {
    const numericValue = value.replace(/[^0-9.]/g, ''); // Allowed decimals just in case
    setSets(prev => prev.map(set => 
      set.id === id ? { ...set, [field]: numericValue } : set
    ));
  };

  const toggleDropset = (id: number) => {
    setSets(prev => prev.map(set => 
      set.id === id ? { ...set, isDropset: !set.isDropset, dropEndWeight: '' } : set
    ));
  };

  const getStatus = () => {
    let filledSets = 0;
    sets.forEach(set => {
      const hasBasicData = set.reps !== '' && set.weight !== '';
      const hasDropsetData = set.isDropset ? set.dropEndWeight !== '' : true;
      if (hasBasicData && hasDropsetData) filledSets += 1;
    });

    if (filledSets === 0) return { label: 'Not Done', style: 'bg-zinc-100 text-zinc-500', icon: <CircleDashed className="w-4 h-4" /> };
    if (filledSets > 0 && filledSets < sets.length) return { label: 'Partially Done', style: 'bg-amber-100 text-amber-700', icon: <CircleDashed className="w-4 h-4" /> };
    return { label: 'Completed', style: 'bg-blue-600 text-white shadow-md', icon: <CheckCircle2 className="w-4 h-4" /> };
  };

  const status = getStatus();

  // 3. Dynamically format the Pelank Image URL
  // "Walking Lunges" -> "walking-lunges" and "Walking-Lunges"
  const folderName = exercise.exercise_name.toLowerCase().replace(/\s+/g, '-');
  const fileName = exercise.exercise_name.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('-');
  const imageUrl = `https://pelank.com/exercises/${folderName}/${fileName}.gif`;

  return (
    <div className="w-full bg-white border border-zinc-200 rounded-2xl shadow-sm overflow-hidden font-sans">
      
      {/* Top Header - Now Dynamic */}
      <div className="bg-slate-50 border-b border-zinc-100 px-5 py-4 flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Dumbbell className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="font-semibold text-lg text-slate-800 tracking-tight">{exercise.exercise_name}</h3>
          </div>
          <button 
            onClick={onOpenDetails}
            className="text-xs font-semibold text-blue-600 hover:text-blue-800 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-full transition-colors flex items-center gap-1"
          >
            <Info className="w-3.5 h-3.5" />
            View Deep Dive
          </button>
        </div>
        
        {/* Dynamic Badges based on Python muscle_data */}
        <div className="flex gap-2 ml-12">
          {exercise.muscle_data.primary_targets.map(muscle => (
            <span key={muscle} className="px-2 py-0.5 bg-slate-200 text-slate-600 text-xs font-semibold rounded-md capitalize">
              {muscle}
            </span>
          ))}
          {exercise.muscle_data.is_compound && (
            <span className="px-2 py-0.5 bg-indigo-100 text-indigo-600 text-xs font-semibold rounded-md">
              Compound
            </span>
          )}
        </div>
      </div>

      <div className="p-5 flex flex-col md:flex-row gap-6">
        {/* Left Side: Dynamic Image */}
        <div className="w-full md:w-1/3 shrink-0 flex flex-col gap-2">
        <div className="aspect-square bg-slate-100 rounded-xl border border-slate-200 overflow-hidden flex items-center justify-center relative">
            <img 
              // 1. Try to load the Wger image first
              // 2. If it's blank, fall back to a sleek placeholder
              src={exercise.card_image || 'https://placehold.co/400x400/f8fafc/94a3b8?text=Illustration+Pending'} 
              alt={exercise.exercise_name} 
              className="w-full h-full object-contain p-2 mix-blend-multiply opacity-90 transition-opacity duration-300"
              onError={(e) => {
                 // 3. Safety net: If the Wger link ever breaks, it safely defaults to the placeholder
                 // instead of showing a broken image icon.
                (e.target as HTMLImageElement).src = 'https://placehold.co/400x400/f8fafc/94a3b8?text=Illustration+Pending';
              }}
            />
          </div>
        </div>

        <div className="w-full md:w-2/3 flex flex-col">
          {/* Tips Section - Dynamically pulling from biomechanics */}
          {exercise.biomechanics.joint_stress.length > 0 && (
            <div className="bg-blue-50/50 border border-blue-100 rounded-xl p-4 mb-6">
              <div className="flex items-center gap-2 mb-1">
                <Info className="w-4 h-4 text-blue-500" />
                <h4 className="font-medium text-blue-900 text-sm">Form & Joint Stress Warning</h4>
              </div>
              <p className="text-sm text-slate-600 leading-relaxed capitalize">
                Be mindful of: {exercise.biomechanics.joint_stress.join(', ').replace('_', ' ')}.
              </p>
            </div>
          )}

          {/* Sets Tracking (Remains the same) */}
          <div className="space-y-3 mb-6">
            <div className="flex items-center px-2 text-xs font-semibold text-slate-400 tracking-wider uppercase">
              <div className="w-10">Set</div>
              <div className="w-20 text-center">Reps</div>
              <div className="flex-1 px-4">Weight (kg)</div>
              <div className="w-20 text-center">Dropset</div>
            </div>

            {sets.map((set, index) => (
              <div key={set.id} className="flex items-center bg-slate-50 border border-slate-100 rounded-lg p-2 focus-within:bg-white focus-within:border-blue-200 focus-within:shadow-sm">
                <div className="w-10 flex justify-center"><span className="font-medium text-slate-500">{index + 1}</span></div>
                <div className="w-20">
                  <input type="text" inputMode="numeric" placeholder="0" value={set.reps} onChange={(e) => handleInputChange(set.id, 'reps', e.target.value)} className="w-full text-center bg-transparent font-semibold text-slate-700 outline-none placeholder:text-slate-300" />
                </div>
                <div className="flex-1 flex items-center justify-center px-2">
                  <input type="text" inputMode="numeric" placeholder="Start" value={set.weight} onChange={(e) => handleInputChange(set.id, 'weight', e.target.value)} className="w-16 text-center bg-white border border-slate-200 rounded-md py-1 font-medium text-slate-700 outline-none focus:border-blue-400 placeholder:text-slate-300" />
                  {set.isDropset && (
                    <div className="flex items-center animate-in fade-in slide-in-from-left-2 duration-200">
                      <ChevronRight className="w-4 h-4 mx-1 text-slate-400" />
                      <input type="text" inputMode="numeric" placeholder="End" value={set.dropEndWeight} onChange={(e) => handleInputChange(set.id, 'dropEndWeight', e.target.value)} className="w-16 text-center bg-white border border-orange-200 rounded-md py-1 font-medium text-orange-700 outline-none focus:border-orange-400 placeholder:text-orange-300" />
                    </div>
                  )}
                </div>
                <div className="w-20 flex justify-center">
                  <input type="checkbox" checked={set.isDropset} onChange={() => toggleDropset(set.id)} className="w-4 h-4 text-blue-600 rounded border-slate-300 cursor-pointer" />
                </div>
              </div>
            ))}
          </div>

          <div className="mt-auto">
            <button className={`w-full py-3 rounded-xl flex items-center justify-center gap-2 font-semibold transition-all duration-300 ${status.style}`}>
              {status.icon}
              {status.label}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}