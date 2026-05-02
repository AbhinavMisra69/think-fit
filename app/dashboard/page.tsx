'use client';

import React, { useState, useMemo, useEffect } from 'react';
import { 
  ChevronLeft, ChevronRight, User, Dumbbell, BatteryCharging,
  X, Target, Activity, Settings2, Info, VideoOff,
  Map, CalendarDays, Zap, Shield, TrendingUp, CheckCircle2 // <-- Added new icons here!
} from 'lucide-react';
import StreakCalendar from "@/components/StreakCalendar";
import ExerciseCard, { type ExerciseData } from "@/components/ExerciseCard";
import RestDayCard from "@/components/RestDayCard";
import { Navigation } from '@/components/Navigation';
import { useAuth } from "app/context/AuthContext";

const toDateString = (date: Date) => {
  const d = new Date(date);
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().split('T')[0];
};

type DayData = {
  type: 'workout' | 'rest';
  progress: number; 
};

// --- Added Types for the Macrocycle ---
type PhaseData = {
  phase: string;
  start_week: number;
  end_week: number;
  focus: string;
  theme: 'blue' | 'orange' | 'emerald' | 'purple';
};

type MacrocycleData = {
  total_weeks: number;
  current_week: number;
  goal: string;
  phases: PhaseData[];
};

export default function Page() {
  const { user } = useAuth(); // Assuming your context returns an object with 'user'
  const userId = user?.id;
  const [currentWeekStart, setCurrentWeekStart] = useState(() => {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const day = today.getDay();
  const diff = today.getDate() - day + (day === 0 ? -6 : 1); 
  return new Date(today.setDate(diff));
  });

  const [selectedDate, setSelectedDate] = useState(() => {
    const today = new Date();
    today.setHours(0,0,0,0);
    return today;
  });

  const [dayDataMap, setDayDataMap] = useState<Record<string, DayData>>({});
  const [weeklyProgram, setWeeklyProgram] = useState<any>(null);
  const [activeExercise, setActiveExercise] = useState<ExerciseData | null>(null);
  const [isLoading, setIsLoading] = useState(true);


  useEffect(() => {
    const fetchWeekData = async () => {
      if (!userId) return;
      setIsLoading(true);
      try {
        const dayIndex = selectedDate.getDay();
        const dayKey = `Day_${dayIndex === 0 ? 7 : dayIndex}`;

        // Ensure this port matches your backend! (5000 or 5001)
        let res = await fetch(`http://127.0.0.1:5001/api/workout/today?user_id=${userId}&day_key=${dayKey}`);
        
        if (res.status === 404) {
          await fetch(`http://127.0.0.1:5001/api/workout/generate_week`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, equipment: [] })
          });
          res = await fetch(`http://127.0.0.1:5001/api/workout/today?user_id=${userId}&day_key=${dayKey}`);
        }


        const data = await res.json();
        
        if (data.status === "success" || data.is_rest_day) {
           setWeeklyProgram((prev: any) => ({ ...prev, [dayKey]: data.today_workout }));
           
           const dateStr = toDateString(selectedDate);
           setDayDataMap(prevMap => ({
             ...prevMap,
             [dateStr]: {
               type: data.is_rest_day ? 'rest' : 'workout',
               progress: prevMap[dateStr]?.progress || 0 
             }
           }));
        }
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchWeekData();
  }, [selectedDate, userId]);

  const handlePrevWeek = () => setCurrentWeekStart(prev => new Date(prev.setDate(prev.getDate() - 7)));
  const handleNextWeek = () => setCurrentWeekStart(prev => new Date(prev.setDate(prev.getDate() + 7)));

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

  const selectedStr = toDateString(selectedDate);
  const isSelectedToday = selectedStr === toDateString(new Date());
  const protocolTitle = isSelectedToday 
    ? "Today's Protocol" 
    : `${selectedDate.toLocaleDateString('en-US', { weekday: 'long' })}'s Protocol`;

  const getDayKey = (date: Date) => {
    let dayIndex = date.getDay();
    return `Day_${dayIndex === 0 ? 7 : dayIndex}`;
  };
  
  const currentDayExercises = weeklyProgram ? (weeklyProgram[getDayKey(selectedDate)] || []) : [];

  return (
    <div>
      <section className="fixed top-0 right-0 w-1/3 h-screen bg-zinc-50 border-l border-zinc-200 overflow-hidden font-sans shadow-lg hidden md:block">
        {activeExercise ? (
          <ExerciseDetailPanel 
            exercise={activeExercise} 
            onClose={() => setActiveExercise(null)} 
          />
        ) : (
          <div className="h-full overflow-y-auto pt-8 pb-20">
            <h2 className="text-2xl font-semibold tracking-tight text-gray-800 mb-4 ml-6">
              Monthly Progress
            </h2>
            <div className="px-6 mb-10">
            <StreakCalendar history={dayDataMap} />
            </div>
            
            {/* NEW: The integrated Macrocycle Overview right below the calendar! */}
            <MacrocycleSidebar userId={userId as string} />
            
          </div>
        )}
      </section>

      <div className="fixed top-0 left-0 w-full md:w-2/3 h-screen bg-white overflow-y-auto font-sans shadow-sm">
        <div className="p-8 max-w-4xl mx-auto">
          
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

          <div className="mt-12 border-t border-zinc-100 pt-8">
            <h3 className="text-xl font-bold text-zinc-900 mb-6">{protocolTitle}</h3>
            
            <div className="flex flex-col gap-6">
              {isLoading ? (
                <div className="py-10 text-center text-zinc-400 animate-pulse">Generating optimal AI protocol...</div>
              ) : (!currentDayExercises || currentDayExercises.length === 0) ? (
                <RestDayCard />
              ) : (
                    currentDayExercises.map((exerciseData: any, index: number) => {
                    const uniqueName = exerciseData.exercise_name || exerciseData.exercise || `fallback-${index}`;
                    
                    return (
                      <ExerciseCard 
                        key={`${uniqueName}-${index}`} 
                        exercise={exerciseData} 
                        onOpenDetails={() => setActiveExercise(exerciseData)} 
                      />
                    );
                  })
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

// --- NEW MACROCYCLE SIDEBAR COMPONENT ---
function MacrocycleSidebar({ userId }: { userId: string }) {
  const [data, setData] = useState<MacrocycleData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchMacrocycle = async () => {
      // --- Add Guard Here Too ---
      if (!userId) return;

      try {
        const res = await fetch(`http://127.0.0.1:5001/api/workout/macrocycle?user_id=${userId}`);
        const result = await res.json();
        if (result.status === "success") setData(result);
      } catch (err) {
        console.error("Failed to fetch macrocycle data", err);
      } finally {
        setIsLoading(false);
      }
    };
    fetchMacrocycle();
  }, [userId]);

  // Using explicit Tailwind classes so the compiler doesn't purge them
  const getThemeStyles = (theme: string, isActive: boolean, isPast: boolean) => {
    if (isPast) return "bg-slate-50 border-slate-200 text-slate-500";
    if (!isActive) return "bg-white border-zinc-200 text-zinc-400";
    
    switch (theme) {
      case 'orange': return "bg-orange-50 border-orange-200 text-orange-700 ring-2 ring-orange-50";
      case 'emerald': return "bg-emerald-50 border-emerald-200 text-emerald-700 ring-2 ring-emerald-50";
      case 'purple': return "bg-purple-50 border-purple-200 text-purple-700 ring-2 ring-purple-50";
      default: return "bg-blue-50 border-blue-200 text-blue-700 ring-2 ring-blue-50";
    }
  };

  const getThemeIcon = (theme: string) => {
    switch (theme) {
      case 'orange': return <Zap className="w-4 h-4" />;
      case 'emerald': return <TrendingUp className="w-4 h-4" />;
      case 'purple': return <Shield className="w-4 h-4" />;
      default: return <Target className="w-4 h-4" />;
    }
  };

  if (isLoading || !data) return null;

  const progressPercentage = Math.round((data.current_week / data.total_weeks) * 100);

  return (
    <div className="px-6 pb-8 border-t border-zinc-200 pt-8 mt-2">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-slate-800 tracking-tight flex items-center gap-2 mb-1">
          <Map className="w-5 h-5 text-blue-600" /> Program Roadmap
        </h3>
        <p className="text-sm text-slate-500">
          Optimized for <span className="font-semibold text-slate-700 capitalize">{data.goal.replace(/_/g, ' ')}</span>
        </p>
      </div>

      <div className="bg-white rounded-xl p-4 shadow-sm border border-zinc-200 mb-8">
        <div className="flex justify-between items-end mb-3">
          <div>
            <p className="text-xs font-bold text-zinc-400 uppercase tracking-wider mb-0.5">Progress</p>
            <p className="text-lg font-bold text-slate-800">Wk {data.current_week} <span className="text-zinc-400 text-sm font-medium">/ {data.total_weeks}</span></p>
          </div>
          <span className="text-xl font-bold text-blue-600">{progressPercentage}%</span>
        </div>
        <div className="w-full h-2 bg-slate-100 rounded-full overflow-hidden">
          <div className="h-full bg-blue-600 rounded-full transition-all duration-1000 ease-out" style={{ width: `${progressPercentage}%` }} />
        </div>
      </div>

      {/* Compact Vertical Timeline */}
      <div className="space-y-4 relative before:absolute before:inset-0 before:ml-[15px] before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
        {data.phases.map((phase, index) => {
          const isPast = data.current_week > phase.end_week;
          const isActive = data.current_week >= phase.start_week && data.current_week <= phase.end_week;
          const cardStyles = getThemeStyles(phase.theme, isActive, isPast);

          return (
            <div key={index} className="relative flex items-start gap-4 group">
              <div className={`flex items-center justify-center w-8 h-8 mt-1 rounded-full border-[3px] border-zinc-50 bg-white shadow-sm shrink-0 z-10 transition-colors ${isActive ? 'ring-2 ring-blue-100' : ''}`}>
                {isPast ? <CheckCircle2 className="w-4 h-4 text-emerald-500" /> : getThemeIcon(phase.theme)}
              </div>
              
              <div className={`flex-1 p-3 rounded-lg shadow-sm border transition-all duration-300 ${cardStyles}`}>
                <div className="flex justify-between items-center mb-1.5">
                  <span className="text-[10px] font-bold uppercase tracking-wider opacity-80 flex items-center gap-1">
                    <CalendarDays className="w-3 h-3" /> Wk {phase.start_week}-{phase.end_week}
                  </span>
                  {isActive && <span className="flex h-1.5 w-1.5 relative">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-current opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-current"></span>
                  </span>}
                </div>
                <h4 className={`text-sm font-bold mb-1 ${isPast ? 'text-slate-500' : 'text-slate-800'}`}>{phase.phase}</h4>
                <p className={`text-xs leading-relaxed ${isPast ? 'text-slate-400' : 'text-slate-600'}`}>{phase.focus}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// --- EXISTING PANELS ---
function ExerciseDetailPanel({ exercise, onClose }: { exercise: ExerciseData; onClose: () => void }) {
  const isMissingVideo = !exercise.youtube_id || exercise.youtube_id === "REPLACE_ME";
  const youtubeEmbedUrl = `https://www.youtube.com/embed/${exercise.youtube_id}?rel=0`;

  return (
    <div className="h-full flex flex-col bg-zinc-50 animate-in slide-in-from-right-4 duration-300">
      <div className="flex items-center justify-between p-6 border-b border-zinc-200 bg-white shadow-sm z-10 shrink-0">
      <h2 className="text-xl font-bold text-zinc-900 tracking-tight">{exercise.exercise_name || (exercise as any).exercise}</h2>
        <button onClick={onClose} className="p-2 hover:bg-zinc-100 rounded-full text-zinc-500 hover:text-zinc-800 transition-colors">
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-8 pb-20">
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
                title={`${exercise.exercise_name || (exercise as any).exercise} execution video`}
                className="w-full h-full absolute top-0 left-0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
              />
            )}
          </div>
          {!isMissingVideo && <p className="text-xs text-zinc-500 text-center">Source: YouTube</p>}
        </div>

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
                {exercise.biomechanics?.joint_stress?.length > 0 ? exercise.biomechanics.joint_stress.join(', ').replace(/_/g, ' ') : 'None'}
              </span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-zinc-500">Facility Needs</span>
              <span className="text-sm font-semibold text-zinc-800 capitalize text-right">
                {exercise.facility_requirements?.specific_tools?.join(', ').replace(/_/g, ' ') || 'None'}
              </span>
            </div>
          </div>
        </div>

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
