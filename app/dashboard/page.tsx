'use client';

import React, { useState, useMemo } from 'react';
import { 
  ChevronLeft, 
  ChevronRight, 
  User, 
  Dumbbell, 
  BatteryCharging,
  X,
  Target,
  Activity,
  Settings2,
  Info,
  VideoOff
} from 'lucide-react';
import StreakCalendar from "@/components/StreakCalendar";
import ExerciseCard, { type ExerciseData } from "@/components/ExerciseCard";
import RestDayCard from "@/components/RestDayCard";
import exerciseDataset from "@/data/exercises_enriched.json";

// --- Helper to get clean YYYY-MM-DD strings for state tracking ---
const toDateString = (date: Date) => {
  const d = new Date(date);
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().split('T')[0];
};

type DayData = {
  type: 'workout' | 'rest';
  progress: number; // 0 to 100
};

export default function Page() {
  // 1. Structural State: Which week are we looking at?
  const [currentWeekStart, setCurrentWeekStart] = useState(() => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const day = today.getDay();
    const diff = today.getDate() - day + (day === 0 ? -6 : 1); 
    return new Date(today.setDate(diff));
  });

  // 2. Selection State: Which day did the user click? (Defaults to today)
  const [selectedDate, setSelectedDate] = useState(() => {
    const today = new Date();
    today.setHours(0,0,0,0);
    return today;
  });

  // 3. Functional State: Track actual progress AND day type
  const [dayDataMap, setDayDataMap] = useState<Record<string, DayData>>(() => {
    const start = new Date();
    const day = start.getDay();
    const diff = start.getDate() - day + (day === 0 ? -6 : 1);
    start.setDate(diff);
    
    // Setting up a week with mixed workout and rest days
    return {
      [toDateString(new Date(start.setDate(start.getDate() + 0)))]: { type: 'workout', progress: 50 },  // Mon
      [toDateString(new Date(start.setDate(start.getDate() + 1)))]: { type: 'workout', progress: 100 }, // Tue
      [toDateString(new Date(start.setDate(start.getDate() + 1)))]: { type: 'rest', progress: 100 },    // Wed
      [toDateString(new Date(start.setDate(start.getDate() + 1)))]: { type: 'workout', progress: 75 },  // Thu
      [toDateString(new Date(start.setDate(start.getDate() + 1)))]: { type: 'workout', progress: 0 },   // Fri
    };
  });

  // 4. NEW STATE: Tracks which exercise is open on the right side
  const [activeExercise, setActiveExercise] = useState<ExerciseData | null>(null);

  const handlePrevWeek = () => setCurrentWeekStart(prev => new Date(prev.setDate(prev.getDate() - 7)));
  const handleNextWeek = () => setCurrentWeekStart(prev => new Date(prev.setDate(prev.getDate() + 7)));

  // Generate the 7 day objects dynamically
  const weekDays = useMemo(() => {
    const todayStr = toDateString(new Date());
    const selectedStr = toDateString(selectedDate);

    return Array.from({ length: 7 }).map((_, i) => {
      const date = new Date(currentWeekStart);
      date.setDate(currentWeekStart.getDate() + i);
      const dateStr = toDateString(date);
      const data = dayDataMap[dateStr] || { type: 'workout', progress: 0 };
      
      return {
        date,
        dateStr,
        label: date.toLocaleDateString('en-US', { weekday: 'short' }).slice(0, 2),
        ...data,
        isToday: dateStr === todayStr,
        isSelected: dateStr === selectedStr,
      };
    });
  }, [currentWeekStart, dayDataMap, selectedDate]);

  // Pull the data for whatever day the user clicked
  const selectedStr = toDateString(selectedDate);
  const selectedData = dayDataMap[selectedStr] || { type: 'workout', progress: 0 };
  
  // Format the title dynamically
  const isSelectedToday = selectedStr === toDateString(new Date());
  const protocolTitle = isSelectedToday 
    ? "Today's Protocol" 
    : `${selectedDate.toLocaleDateString('en-US', { weekday: 'long' })}'s Protocol`;

  return (
    <div>
      {/* RIGHT SIDE: Dynamic Info Panel vs Calendar */}
      <section className="fixed top-0 right-0 w-1/3 h-screen bg-zinc-50 border-l border-zinc-200 overflow-hidden font-sans shadow-lg hidden md:block">
        {activeExercise ? (
          <ExerciseDetailPanel 
            exercise={activeExercise} 
            onClose={() => setActiveExercise(null)} 
          />
        ) : (
          <div className="h-full overflow-y-auto pt-8">
            <h2 className="text-2xl font-semibold tracking-tight text-gray-800 mb-4 ml-6">
              Monthly Progress
            </h2>
            <div className="px-6">
              <StreakCalendar />
            </div>
          </div>
        )}
      </section>

      {/* LEFT SIDE: Weekly Progress & Protocol */}
      <div className="fixed top-0 left-0 w-full md:w-2/3 h-screen bg-white overflow-y-auto font-sans shadow-sm">
        <div className="p-8 max-w-4xl mx-auto">
          
          {/* Header */}
          <div className="flex items-center justify-between mb-10">
            <div className="flex items-center gap-6">
              <span className="font-semibold text-3xl text-slate-800">0</span>
              <div className="flex items-center space-x-3 bg-slate-50 p-1.5 rounded-full border border-slate-100">
                <button onClick={handlePrevWeek} className="p-2 bg-white shadow-sm rounded-full hover:bg-slate-100 transition-colors active:scale-95">
                  <ChevronLeft className="w-5 h-5 text-slate-700" />
                </button>
                <span className="text-sm font-semibold tracking-wide text-slate-700 min-w-[90px] text-center uppercase">
                  {toDateString(currentWeekStart) === toDateString(new Date(new Date().setDate(new Date().getDate() - new Date().getDay() + 1))) 
                    ? "This week" 
                    : currentWeekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </span>
                <button onClick={handleNextWeek} className="p-2 bg-white shadow-sm rounded-full hover:bg-slate-100 transition-colors active:scale-95">
                  <ChevronRight className="w-5 h-5 text-slate-700" />
                </button>
              </div>
            </div>
            <button className="p-3 bg-slate-100 rounded-full hover:bg-slate-200 transition-colors">
              <User className="w-6 h-6 text-slate-700" />
            </button>
          </div>

          {/* Progress Days Row */}
          <div className="flex justify-between w-full px-2 sm:px-4 select-none mb-10 overflow-x-auto pb-4">
            {weekDays.map((day, index) => {
              const isComplete = day.progress === 100;
              const prevComplete = index > 0 && weekDays[index - 1].progress === 100;
              const nextComplete = index < 6 && weekDays[index + 1].progress === 100;
              const isRest = day.type === 'rest';

              let streakBgClass = "bg-transparent";
              if (isComplete) {
                streakBgClass = isRest ? "bg-emerald-100/50" : "bg-blue-100/50";
                if (!prevComplete && nextComplete) streakBgClass += " rounded-l-full scale-y-110";
                else if (prevComplete && !nextComplete) streakBgClass += " rounded-r-full scale-y-110";
                else if (prevComplete && nextComplete) streakBgClass += " scale-y-110";
                else streakBgClass += " rounded-full scale-y-110";
              }

              return (
                <div 
                  key={day.dateStr} 
                  className="relative flex-1 min-w-[60px] flex flex-col items-center group cursor-pointer" 
                  onClick={() => setSelectedDate(day.date)}
                >
                  <div className={`absolute top-0 bottom-[36px] w-full transition-all duration-300 ease-in-out ${streakBgClass}`} />

                  <div className={`relative z-10 pt-2 transform transition-transform ${isRest ? '' : 'group-hover:scale-105 active:scale-95'}`}>
                    <div className={`rounded-full transition-all duration-200 ${day.isSelected ? 'ring-4 ring-slate-100 shadow-sm scale-105' : ''}`}>
                      <CircularProgress 
                        progress={day.progress} 
                        label={day.label} 
                        isToday={day.isToday} 
                        theme={isRest ? 'green' : 'blue'}
                      />
                    </div>
                  </div>

                  <div className="mt-4 relative z-10">
                    {isRest ? (
                      <BatteryCharging className={`w-5 h-5 transition-colors duration-300 ${isComplete ? 'text-emerald-500 fill-emerald-500' : 'text-slate-300 fill-slate-300'}`} />
                    ) : (
                      <Dumbbell className={`w-5 h-5 transition-colors duration-300 ${isComplete ? 'text-blue-500 fill-blue-500' : 'text-slate-300 fill-slate-300'}`} />
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          {/* Dynamic Protocol Area */}
          {/* Dynamic Protocol Area */}
          <div className="mt-12 border-t border-zinc-100 pt-8">
            <h3 className="text-xl font-bold text-zinc-900 mb-6">{protocolTitle}</h3>
            
            <div className="flex flex-col gap-6">
              {selectedData.type === 'rest' ? (
                <RestDayCard />
              ) : (
                <>
                  {/* We convert your JSON object into an array and map over it! */}
                  {/* Note: I added a .slice(0, 5) just so it doesn't render all 60 exercises at once while testing! */}
                  {Object.values(exerciseDataset).slice(0, 5).map((exerciseData: any) => (
                    <ExerciseCard 
                      key={exerciseData.exercise_id} 
                      // We pass the data down as a prop, exactly as you suggested
                      exercise={exerciseData} 
                      onOpenDetails={() => setActiveExercise(exerciseData)} 
                    />
                  ))}
                </>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

// --- The NEW Exercise Detail Panel ---
// Make sure to add 'Info' and 'VideoOff' to your lucide-react imports at the top of the file!
// import { X, Target, Activity, Settings2, Info, VideoOff } from 'lucide-react';

function ExerciseDetailPanel({ exercise, onClose }: { exercise: ExerciseData; onClose: () => void }) {
  // 1. Safely check if we have a real YouTube ID yet
  const isMissingVideo = !exercise.youtube_id || exercise.youtube_id === "REPLACE_ME";
  const youtubeEmbedUrl = `https://www.youtube.com/embed/${exercise.youtube_id}?rel=0`;

  return (
    <div className="h-full flex flex-col bg-zinc-50 animate-in slide-in-from-right-4 duration-300">
      
      {/* Header with Close Button */}
      <div className="flex items-center justify-between p-6 border-b border-zinc-200 bg-white shadow-sm z-10 shrink-0">
        <h2 className="text-xl font-bold text-zinc-900 tracking-tight">{exercise.exercise_name}</h2>
        <button 
          onClick={onClose}
          className="p-2 hover:bg-zinc-100 rounded-full text-zinc-500 hover:text-zinc-800 transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-8 pb-20">
        
        {/* NEW: Overview / Description Section */}
        {exercise.description && (
          <div className="space-y-3">
             <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
              <Info className="w-4 h-4" /> Overview
            </h3>
            <p className="text-sm text-slate-600 leading-relaxed bg-white p-5 rounded-xl border border-zinc-200 shadow-sm">
              {exercise.description}
            </p>
          </div>
        )}

        {/* UPGRADED: YouTube Video Player */}
        <div className="space-y-3">
          <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
            <Settings2 className="w-4 h-4" /> Demonstration
          </h3>
          
          <div className="w-full aspect-video bg-zinc-900 rounded-xl overflow-hidden shadow-inner relative flex items-center justify-center">
            {isMissingVideo ? (
              // Sleek fallback state for exercises that still have "REPLACE_ME"
              <div className="flex flex-col items-center text-zinc-500">
                <VideoOff className="w-8 h-8 mb-2 opacity-50" />
                <span className="text-sm font-medium">Video tutorial coming soon</span>
              </div>
            ) : (
              // Real YouTube iframe
              <iframe 
                src={youtubeEmbedUrl}
                title={`${exercise.exercise_name} execution video`}
                className="w-full h-full absolute top-0 left-0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            )}
          </div>
          {!isMissingVideo && <p className="text-xs text-zinc-500 text-center">Source: YouTube</p>}
        </div>

        {/* Biomechanics & Specs */}
        <div className="space-y-4">
           <h3 className="text-sm font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
            <Activity className="w-4 h-4" /> Biomechanics
          </h3>
          <div className="bg-white border border-zinc-200 rounded-xl p-4 shadow-sm space-y-3">
            <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
              <span className="text-sm text-zinc-500">Movement Pattern</span>
              <span className="text-sm font-semibold text-zinc-800 capitalize">{exercise.muscle_data.movement_pattern.replace(/_/g, ' ')}</span>
            </div>
            <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
              <span className="text-sm text-zinc-500">Joint Stress</span>
              <span className="text-sm font-semibold text-orange-600 capitalize text-right">
                {exercise.biomechanics.joint_stress.length > 0 ? exercise.biomechanics.joint_stress.join(', ').replace(/_/g, ' ') : 'None'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-zinc-500">Facility Needs</span>
              <span className="text-sm font-semibold text-zinc-800 capitalize text-right">
                {exercise.facility_requirements.specific_tools.join(', ').replace(/_/g, ' ')}
              </span>
            </div>
          </div>
        </div>

        {/* Hypertrophy Profile */}
        {exercise.periodization_tags?.hypertrophy_tiers && (
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

// --- SVG Circular Progress Component ---
function CircularProgress({ progress, label, isToday, theme }: { progress: number; label: string; isToday: boolean; theme: 'blue' | 'green' }) {
  const radius = 24; 
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;
  const isComplete = progress === 100;
  
  const colors = {
    blue: { textActive: 'text-blue-600', strokeFull: 'text-blue-500', strokePartial: 'text-blue-500' },
    green: { textActive: 'text-emerald-600', strokeFull: 'text-emerald-500', strokePartial: 'text-emerald-500' }
  };

  const currentTheme = colors[theme];
  const textColor = isToday || isComplete ? `${currentTheme.textActive} font-bold` : 'text-slate-400 font-medium';

  return (
    <div className="relative flex items-center justify-center w-16 h-16 bg-white rounded-full">
      <svg className="w-full h-full transform -rotate-90 drop-shadow-sm" viewBox="0 0 56 56">
        <circle cx="28" cy="28" r={radius} stroke="currentColor" strokeWidth="5" fill="transparent" className={isComplete ? currentTheme.strokeFull : "text-slate-100"} />
        {progress > 0 && !isComplete && (
          <circle cx="28" cy="28" r={radius} stroke="currentColor" strokeWidth="5" fill="transparent" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset} strokeLinecap="round" className={`${currentTheme.strokePartial} transition-all duration-500 ease-out`} />
        )}
      </svg>
      <span className={`absolute text-base tracking-wide ${textColor}`}>{label}</span>
    </div>
  );
}