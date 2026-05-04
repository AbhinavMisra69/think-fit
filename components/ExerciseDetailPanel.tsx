import { X, Target, Activity, Settings2, Info, VideoOff } from 'lucide-react';
import type { ExerciseData } from '@/components/ExerciseCard'; 

export default function ExerciseDetailPanel({ exercise, onClose }: { exercise: ExerciseData; onClose: () => void }) {
  // 1. Safely extract the name
  const actualName = exercise.exercise_name || (exercise as any).name || (exercise as any).exercise || "Unknown Exercise";
  
  // 2. Check if we have a valid YouTube ID
  const isMissingVideo = !exercise.youtube_id || exercise.youtube_id === "REPLACE_ME";
  const youtubeEmbedUrl = `https://www.youtube.com/embed/${exercise.youtube_id}?rel=0`;

  return (
    <div className="h-full flex flex-col bg-zinc-50 animate-in slide-in-from-right-4 duration-300">
      
      {/* Header with Close Button */}
      <div className="flex items-center justify-between p-6 border-b border-zinc-200 bg-white shadow-sm z-10 shrink-0">
        <h2 className="text-xl font-bold text-zinc-900 tracking-tight">{actualName}</h2>
        <button 
          onClick={onClose}
          className="p-2 hover:bg-zinc-100 rounded-full text-zinc-500 hover:text-zinc-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-8 pb-20">
        
        {/* --- NEW: Description / Overview Section --- */}
        {exercise.description && exercise.description !== "Description coming soon." && (
          <div className="space-y-3">
             <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
              <Info className="w-4 h-4" /> Overview
            </h3>
            <p className="text-sm text-slate-600 leading-relaxed bg-white p-5 rounded-xl border border-zinc-200 shadow-sm">
              {exercise.description}
            </p>
          </div>
        )}

        {/* --- UPDATED: YouTube iframe Player --- */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
            <Settings2 className="w-4 h-4" /> Demonstration
          </h3>
          
          <div className="w-full aspect-video bg-zinc-900 rounded-xl overflow-hidden shadow-inner relative flex items-center justify-center">
            {isMissingVideo ? (
              <div className="flex flex-col items-center text-zinc-500">
                <VideoOff className="w-8 h-8 mb-2 opacity-50" />
                <span className="text-sm font-medium">Video tutorial coming soon</span>
              </div>
            ) : (
              <iframe 
                src={youtubeEmbedUrl}
                title={`${actualName} execution video`}
                className="w-full h-full absolute top-0 left-0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            )}
          </div>
          {!isMissingVideo && <p className="text-xs text-zinc-500 text-center">Source: YouTube</p>}
        </div>

        {/* Biomechanics & Specs */}
        {(exercise.muscle_data || exercise.biomechanics || exercise.facility_requirements) && (
          <div className="space-y-4">
             <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
              <Activity className="w-4 h-4" /> Biomechanics
            </h3>
            <div className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm space-y-3">
              <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
                <span className="text-sm text-zinc-500">Movement Pattern</span>
                <span className="text-sm font-semibold text-zinc-800 capitalize">
                  {exercise.muscle_data?.movement_pattern?.replace(/_/g, ' ') || 'N/A'}
                </span>
              </div>
              <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
                <span className="text-sm text-zinc-500">Joint Stress</span>
                <span className="text-sm font-semibold text-orange-600 capitalize text-right">
                  {exercise.biomechanics?.joint_stress?.length 
                    ? exercise.biomechanics.joint_stress.join(', ').replace(/_/g, ' ') 
                    : 'None'}
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-zinc-500">Facility Needs</span>
                <span className="text-sm font-semibold text-zinc-800 capitalize text-right">
                  {exercise.facility_requirements?.specific_tools?.length 
                    ? exercise.facility_requirements.specific_tools.join(', ').replace(/_/g, ' ') 
                    : 'None'}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* Hypertrophy Profile */}
        {exercise.periodization_tags?.hypertrophy_tiers && Object.keys(exercise.periodization_tags.hypertrophy_tiers).length > 0 && (
          <div className="space-y-4">
             <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
              <Target className="w-4 h-4" /> Hypertrophy Profile
            </h3>
            <div className="flex flex-wrap gap-2">
              {Object.entries(exercise.periodization_tags.hypertrophy_tiers).map(([muscle, tier]) => (
                <div key={muscle} className="flex flex-col bg-white border border-zinc-200 px-3 py-2 rounded-lg shadow-sm flex-1 min-w-[100px]">
                  <span className="text-xs text-zinc-500 capitalize">{muscle.replace(/_/g, ' ')}</span>
                  <span className="text-sm font-bold text-blue-600">{tier as React.ReactNode}</span>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}