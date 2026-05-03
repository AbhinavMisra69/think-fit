'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Dumbbell, Info, CheckCircle2, CircleDashed, ChevronRight, Target, Plus, Loader2 } from 'lucide-react';
import data from '@/data/exercises_enriched.json';
import { useAuth } from "app/context/AuthContext"; // Import your auth hook!
import { toast } from "sonner"; // For success popups

// 1. Types (Updated with progression targets)
export type ExerciseData = {
  exercise_id: string;
  exercise_name: string;
  youtube_id: string;
  description?: string;
  animation_frames?: string[];
  target_sets?: number;          // NEW: From Progression Engine
  target_reps?: number | string; // NEW: From Progression Engine
  target_weight?: number | string; // NEW: From Progression Engine
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
    hypertrophy_tiers: Record<string, string>; 
  };
};

type ExerciseCardProps = {
  exercise: ExerciseData;
  onOpenDetails: () => void;
  onProgressUpdate?: (ratio: number) => void; 
};

// 2. Animation Component
function ExerciseAnimation({ frames }: { frames: string[] }) {
  const [currentFrame, setCurrentFrame] = useState(0);
  
  useEffect(() => {
    if (!frames || frames.length !== 2) return;
    const interval = setInterval(() => {
      setCurrentFrame((prev) => (prev === 0 ? 1 : 0));
    }, 800);
    return () => clearInterval(interval);
  }, [frames]);

  if (!frames || frames.length === 0) {
    return (
      <div className="w-full aspect-square bg-slate-50 flex items-center justify-center rounded-xl border border-slate-200">
        <span className="text-slate-400 font-bold text-xs uppercase tracking-widest">Image Pending</span>
      </div>
    );
  }

  return (
    <div className="w-full aspect-square bg-white rounded-xl border border-slate-200 overflow-hidden relative p-1">
      <img
        src={frames[currentFrame]}
        alt="Exercise Demonstration"
        className="w-full h-full object-cover object-center scale-[1.05] mix-blend-multiply transition-opacity duration-200"
      />
    </div>
  );
}

// 3. Main Exercise Card Component
export default function ExerciseCard({ exercise, onOpenDetails, onProgressUpdate }: ExerciseCardProps) {
  // NEW: Dynamically initialize the number of sets based on the engine's target
  const { user } = useAuth(); 
  const initialSetsCount = exercise.target_sets || 3;
  const [sets, setSets] = useState(() => 
    Array.from({ length: initialSetsCount }, (_, i) => ({
      id: i + 1, reps: '', weight: '', isDropset: false, dropEndWeight: ''
    }))
  );

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLogged, setIsLogged] = useState(false);
  const lastReportedProgress = useRef<number>(-1);

  useEffect(() => {
    if (onProgressUpdate) {
      const filled = sets.filter(s => {
        const hasBasic = s.reps !== '' && s.weight !== '';
        const hasDropset = s.isDropset ? s.dropEndWeight !== '' : true;
        return hasBasic && hasDropset;
      }).length;
      
      const currentRatio = filled / sets.length;

      if (currentRatio !== lastReportedProgress.current) {
        lastReportedProgress.current = currentRatio;
        onProgressUpdate(currentRatio);
      }
    }
  }, [sets, onProgressUpdate]);


  const handleLogExercise = async () => {
    // 1. Filter out empty sets
    const validSets = sets.filter(s => s.reps !== '' && s.weight !== '');
    if (validSets.length === 0) {
      toast.error("Please fill out at least one set!");
      return;
    }

    setIsSubmitting(true);

    // 2. Aggregate the data for your Postgres Schema
    const setsCompleted = validSets.length;
    // Find the highest weight lifted
    const maxWeight = Math.max(...validSets.map(s => parseFloat(s.weight)));
    // Calculate the average reps across all valid sets
    const avgReps = Math.round(validSets.reduce((sum, s) => sum + parseInt(s.reps), 0) / setsCompleted);

    try {
      const payload = {
        user_id: user?.id,
        exercises: [{
          name: exercise.exercise_name || (exercise as any).exercise,
          sets: setsCompleted,
          reps: avgReps,
          weight: maxWeight
        }]
      };

      const res = await fetch("http://127.0.0.1:5001/api/workout/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error("Failed to save to database");

      toast.success("Exercise logged successfully!");
      setIsLogged(true); // Lock the card so they know it's saved
      
    } catch (error) {
      console.error(error);
      toast.error("Network error. Could not save exercise.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleAddSet = () => {
    setSets(prev => {
      // Find the highest current ID so we don't get React key duplicates
      const nextId = prev.length > 0 ? Math.max(...prev.map(s => s.id)) + 1 : 1;
      return [...prev, { id: nextId, reps: '', weight: '', isDropset: false, dropEndWeight: '' }];
    });
  };

  const handleInputChange = (id: number, field: string, value: string) => {
    const numericValue = value.replace(/[^0-9.]/g, ''); 
    setSets(prev => prev.map(s => s.id === id ? { ...s, [field]: numericValue } : s));
  };

  const toggleDropset = (id: number) => {
    setSets(prev => prev.map(s => 
      s.id === id ? { ...s, isDropset: !s.isDropset, dropEndWeight: '' } : s
    ));
  };

  const getStatus = () => {
    const filled = sets.filter(s => s.reps !== '' && s.weight !== '').length;
    if (filled === 0) return { label: 'Not Done', style: 'bg-zinc-100 text-zinc-500', icon: <CircleDashed className="w-4 h-4" /> };
    if (filled < sets.length) return { label: 'Partially Done', style: 'bg-amber-100 text-amber-700', icon: <CircleDashed className="w-4 h-4" /> };
    return { label: 'Completed', style: 'bg-blue-600 text-white shadow-md', icon: <CheckCircle2 className="w-4 h-4" /> };
  };

  const status = getStatus();
  const nameStr = exercise.exercise_name || "Unknown Exercise";

  const getLocalFrames = () => {
    if (!data) return [];
    let exerciseList: any[] = [];
    
    if (Array.isArray(data)) {
      exerciseList = data;
    } else if ('exercises' in data && Array.isArray((data as any).exercises)) {
      exerciseList = (data as any).exercises;
    } else {
      exerciseList = Object.values(data);
    }

    const match = exerciseList.find((ex: any) => 
      ex?.exercise_id === exercise.exercise_id || 
      ex?.exercise_name?.toLowerCase() === exercise.exercise_name?.toLowerCase()
    );
    
    return match?.animation_frames || [];
  };

  const finalAnimationFrames = (exercise.animation_frames && exercise.animation_frames.length === 2) 
    ? exercise.animation_frames 
    : getLocalFrames();

  // Extract Targets with Safe Fallbacks
  const targetReps = exercise.target_reps || '8-12';
  const targetWeight = exercise.target_weight || 'Determine 1RM';

  return (
    <div className="w-full bg-white border border-zinc-200 rounded-2xl shadow-sm overflow-hidden font-sans">
      
      {/* Header */}
      <div className="bg-slate-50 border-b border-zinc-100 px-5 py-4 flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Dumbbell className="w-5 h-5 text-blue-600" />
            </div>
            <h3 className="font-semibold text-lg text-slate-800 tracking-tight">{nameStr}</h3>
          </div>
          <button 
            onClick={onOpenDetails}
            className="text-xs font-semibold text-blue-600 hover:text-blue-800 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-full transition-colors flex items-center gap-1"
          >
            <Info className="w-3.5 h-3.5" />
            View Details
          </button>
        </div>
        
        {/* Badges */}
        <div className="flex gap-2 ml-12">
          {exercise.muscle_data?.primary_targets?.map((muscle: string) => (
            <span key={muscle} className="px-2 py-0.5 bg-slate-200 text-slate-600 text-xs font-semibold rounded-md capitalize">
              {muscle.replace(/_/g, ' ')}
            </span>
          ))}
          {exercise.muscle_data?.is_compound && (
            <span className="px-2 py-0.5 bg-indigo-100 text-indigo-600 text-xs font-semibold rounded-md">
              Compound
            </span>
          )}
        </div>
      </div>

      <div className="p-5 flex flex-col md:flex-row gap-6">
        {/* Animation */}
        <div className="w-full md:w-1/3 shrink-0">
           <ExerciseAnimation frames={finalAnimationFrames} />
        </div>

        <div className="w-full md:w-2/3 flex flex-col">
          
          {/* NEW: Side-by-Side Information Banners */}
          <div className="flex flex-col xl:flex-row gap-4 mb-6">
            {/* Biomechanics Warning */}
            {exercise.biomechanics?.joint_stress?.length > 0 && (
              <div className="flex-1 bg-blue-50/50 border border-blue-100 rounded-xl p-4">
                <div className="flex items-center gap-2 mb-1">
                  <Info className="w-4 h-4 text-blue-500" />
                  <h4 className="font-medium text-blue-900 text-sm">Form Warning</h4>
                </div>
                <p className="text-sm text-slate-600 leading-relaxed capitalize">
                  Focus on: {exercise.biomechanics.joint_stress.join(', ').replace(/_/g, ' ')}.
                </p>
              </div>
            )}

            {/* Target Goal Banner */}
            <div className="flex-1 bg-slate-50 border border-slate-200 rounded-xl p-4 flex flex-col justify-center">
              <div className="flex items-center gap-2 mb-2 text-slate-500 font-semibold text-xs uppercase tracking-wider">
                <Target className="w-4 h-4 text-blue-500" />
                Target Goal
              </div>
              <div className="flex items-center flex-wrap gap-2 md:gap-3 font-bold text-slate-800 text-[15px]">
                <span>{initialSetsCount} Sets</span>
                <span className="text-slate-300">|</span>
                <span>{targetReps} Reps</span>
                <span className="text-slate-300">|</span>
                <span className={typeof targetWeight === 'string' ? "text-blue-600 text-sm" : ""}>
                  {typeof targetWeight === 'string' ? targetWeight : `${targetWeight} kg`}
                </span>
              </div>
            </div>
          </div>

          {/* Sets Tracking */}
          <div className="space-y-3 mb-6">
            <div className="flex items-center px-2 text-xs font-semibold text-slate-400 tracking-wider uppercase">
              <div className="w-10">Set</div>
              <div className="w-20 text-center">Reps</div>
              <div className="flex-1 px-4 text-center">Weight (kg)</div>
              <div className="w-20 text-center">Drop</div>
            </div>

            {sets.map((set, index) => (
              <div key={set.id} className="flex items-center bg-slate-50 border border-slate-100 rounded-lg p-2 focus-within:bg-white focus-within:border-blue-200 focus-within:shadow-sm">
                <div className="w-10 flex justify-center"><span className="font-medium text-slate-500">{index + 1}</span></div>
                <div className="w-20">
                  {/* Notice the placeholder uses the target reps! */}
                  <input type="text" inputMode="numeric" placeholder={targetReps.toString().split('-')[0]} value={set.reps} onChange={(e) => handleInputChange(set.id, 'reps', e.target.value)} className="w-full text-center bg-transparent font-semibold text-slate-700 outline-none" />
                </div>
                <div className="flex-1 flex items-center justify-center px-2">
                  <input type="text" inputMode="numeric" placeholder="kg" value={set.weight} onChange={(e) => handleInputChange(set.id, 'weight', e.target.value)} className="w-16 text-center bg-white border border-slate-200 rounded-md py-1 font-medium text-slate-700 outline-none" />
                  {set.isDropset && (
                    <div className="flex items-center animate-in fade-in slide-in-from-left-2 duration-200">
                      <ChevronRight className="w-4 h-4 mx-1 text-slate-400" />
                      <input type="text" inputMode="numeric" placeholder="End" value={set.dropEndWeight} onChange={(e) => handleInputChange(set.id, 'dropEndWeight', e.target.value)} className="w-16 text-center bg-white border border-orange-200 rounded-md py-1 font-medium text-orange-700 outline-none" />
                    </div>
                  )}
                </div>
                <div className="w-20 flex justify-center">
                  <input type="checkbox" checked={set.isDropset} onChange={() => toggleDropset(set.id)} className="w-4 h-4 text-blue-600 rounded border-slate-300 cursor-pointer" />
                </div>
              </div>
            ))}
            <button
              type="button"
              onClick={handleAddSet}
              className="w-full py-2.5 mt-2 border-2 border-dashed border-slate-200 text-slate-400 rounded-xl font-semibold text-sm hover:border-blue-300 hover:text-blue-600 hover:bg-blue-50 transition-all flex items-center justify-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Add Another Set
            </button>
          </div>


          <div className="mt-auto">
            <button 
              onClick={handleLogExercise}
              disabled={status.label === 'Not Done' || isSubmitting || isLogged}
              className={`w-full py-3 rounded-xl flex items-center justify-center gap-2 font-semibold transition-all duration-300 
                ${isLogged ? 'bg-emerald-500 text-white shadow-md' : status.style}
                ${(status.label === 'Not Done' && !isLogged) ? 'opacity-70 cursor-not-allowed' : 'hover:scale-[1.02] active:scale-[0.98]'}
              `}
            >
              {isSubmitting ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : isLogged ? (
                <>
                  <CheckCircle2 className="w-5 h-5" />
                  Successfully Logged
                </>
              ) : (
                <>
                  {status.icon}
                  {status.label === 'Completed' ? 'Log Exercise' : status.label === 'Partially Done' ? 'Log Partial Exercise' : 'Not Done'}
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
