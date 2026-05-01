import { X, Target, Activity, Settings2 } from 'lucide-react';
import type { ExerciseData } from '@/components/ExerciseCard'; // Adjust path if needed

function ExerciseDetailPanel({ exercise, onClose }: { exercise: ExerciseData; onClose: () => void }) {
  // Format the M&S URL (e.g., "Walking Lunges" -> "walking-lunges")
  const urlSafeName = exercise.exercise_name.toLowerCase().replace(/\s+/g, '-');
  const msUrl = `https://www.muscleandstrength.com/exercises/${urlSafeName}.html`;

  return (
    <div className="h-full flex flex-col bg-zinc-50 animate-in slide-in-from-right-4 duration-300">
      {/* Header with Close Button */}
      <div className="flex items-center justify-between p-6 border-b border-zinc-200 bg-white shadow-sm z-10">
        <h2 className="text-xl font-bold text-zinc-900 tracking-tight">{exercise.exercise_name}</h2>
        <button 
          onClick={onClose}
          className="p-2 hover:bg-zinc-100 rounded-full text-zinc-500 hover:text-zinc-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-8">
        
        {/* M&S Video iframe Player */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
            <Settings2 className="w-4 h-4" /> Demonstration
          </h3>
          <div className="w-full aspect-video bg-zinc-200 rounded-xl overflow-hidden border border-zinc-300 shadow-inner relative">
             <iframe 
               src={msUrl}
               title={`${exercise.exercise_name} execution video`}
               className="w-full h-full absolute top-0 left-0"
               sandbox="allow-scripts allow-same-origin"
             />
          </div>
          <p className="text-xs text-zinc-500 text-center">Source: Muscle & Strength</p>
        </div>

        {/* Biomechanics & Specs */}
        <div className="space-y-4">
           <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
            <Activity className="w-4 h-4" /> Biomechanics
          </h3>
          <div className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm space-y-3">
            <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
              <span className="text-sm text-zinc-500">Movement Pattern</span>
              <span className="text-sm font-semibold text-zinc-800 capitalize">{exercise.muscle_data.movement_pattern.replace('_', ' ')}</span>
            </div>
            <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
              <span className="text-sm text-zinc-500">Joint Stress</span>
              <span className="text-sm font-semibold text-orange-600 capitalize">{exercise.biomechanics.joint_stress.join(', ').replace('_', ' ') || 'None'}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-zinc-500">Facility Needs</span>
              <span className="text-sm font-semibold text-zinc-800 capitalize">{exercise.facility_requirements.specific_tools.join(', ')}</span>
            </div>
          </div>
        </div>

        {/* Hypertrophy Profile */}
        <div className="space-y-4">
           <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
            <Target className="w-4 h-4" /> Hypertrophy Profile
          </h3>
          <div className="flex flex-wrap gap-2">
            {Object.entries(exercise.periodization_tags.hypertrophy_tiers).map(([muscle, tier]) => (
              <div key={muscle} className="flex flex-col bg-white border border-zinc-200 px-3 py-2 rounded-lg shadow-sm">
                <span className="text-xs text-zinc-500 capitalize">{muscle}</span>
                <span className="text-sm font-bold text-blue-600">{tier as React.ReactNode}</span>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}