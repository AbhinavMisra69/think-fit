'use client';

import React, { useState, useMemo, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { 
  ChevronLeft, ChevronRight, User, Dumbbell, BatteryCharging,
  X, Target, Activity, Settings2, Info, VideoOff,
  Map, CalendarDays, Zap, Shield, TrendingUp, CheckCircle2, AlertTriangle, ArrowRight, Merge, Loader2 
} from 'lucide-react';
import { toast } from 'sonner';
import StreakCalendar from "@/components/StreakCalendar";
import ExerciseCard, { type ExerciseData } from "@/components/ExerciseCard";
import RestDayCard from "@/components/RestDayCard";
import { Navigation } from '@/components/Navigation';
import EditWeekModal from '@/components/EditWeekModal';
import { useAuth } from "app/context/AuthContext";
import SwapExerciseModal from "@/components/SwapExerciseModal";

const toDateString = (date: Date) => {
  const d = new Date(date);
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().split('T')[0];
};

type DayData = {
  type: 'workout' | 'rest';
  progress: number; 
};

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
  const router = useRouter();
  const { user } = useAuth();
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
  const [showInterventionModal, setShowInterventionModal] = useState(false);
  const [interventionData, setInterventionData] = useState<any>(null);
  const [isResolving, setIsResolving] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [currentWeekDays, setCurrentWeekDays] = useState<string[]>([]); 
  const [userActivePhase, setUserActivePhase] = useState(""); 
  const [isDashboardLoading, setIsDashboardLoading] = useState(true);
  const [swapModalOpen, setSwapModalOpen] = useState(false);
  const [exerciseToSwap, setExerciseToSwap] = useState<string>("");


  useEffect(() => {
    if (!userId) return;

    const fetchDashboardData = async () => {
      try {
        const res = await fetch(`http://localhost:5001/api/dashboard/user_data?user_id=${userId}`);
        const data = await res.json();

        if (data.status === "success") {
          setCurrentWeekDays(data.current_week_days);
          setUserActivePhase(data.active_phase);
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      } finally {
        setIsDashboardLoading(false); 
      }
    };

    fetchDashboardData();
  }, [userId]);

  const handleSaveNewSchedule = async (newDaysArray: string[]) => {
    try {
      const res = await fetch(`http://localhost:5001/api/workout/edit_week`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          new_days: newDaysArray
        })
      });
      
      const data = await res.json();

      if (data.status === "success") {
        toast.success(data.message);
        setIsEditModalOpen(false);
        
        // 3. RELOAD THE UI! 
        setTimeout(() => {
          window.location.reload();
        }, 800);
        
        router.refresh(); 
      } else if (data.status === "conflict" || data.status === "error") {
        toast.error(data.message);
      }
    } catch (error) {
      console.error("Failed to update schedule:", error);
      toast.error("A network error occurred while saving.");
    }
  };

  const checkWorkoutStatus = async () => {
    if (!userId) return;
    try {
      const res = await fetch(`http://localhost:5001/api/workout/check_status?user_id=${userId}`);
      const data = await res.json();

      if (data.status === "intervention_needed") {
        if (data.type === "missed_completely") {
          setInterventionData(data);
          setShowInterventionModal(true);
        } else if (data.type === "partial_completion") {
          await handleResolution('triage_partial', data.missed_day_key);
          toast.success("We noticed you couldn't finish your last session. We've optimized today's plan to keep you on track!");
        }
      }
    } catch (error) {
      console.error("Failed to check workout status:", error);
    }
  };

  useEffect(() => {
    checkWorkoutStatus();
  }, [userId]);

  const handleResolution = async (interventionType: string, specificMissedDay: string | null = null) => {
    const targetDay = specificMissedDay || interventionData?.missed_day_key;

    if (!targetDay) {
      toast.error("Could not determine which day was missed.");
      return;
    }

    try {
      const res = await fetch('http://localhost:5001/api/workout/resolve_intervention', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: userId,
          type: interventionType,
          missed_day_key: targetDay
        })
      });
      
      const data = await res.json();

      if (data.status === "success") {
        toast.success(data.message);
        setShowInterventionModal(false);
        router.refresh();
        checkWorkoutStatus(); 
        setTimeout(() => {
            window.location.reload();
          }, 800);
        checkWorkoutStatus(); // Reload the freshly fixed schedule!
      } else if (data.status === "conflict") {
        toast.error(data.message); 
      } else {
        toast.error(data.error || "An error occurred while updating your schedule.");
      }
    } catch (error) {
      console.error("Intervention Error:", error);
      toast.error("Failed to connect to the server.");
    }
  };

  useEffect(() => {
    const fetchWeekData = async () => {
      if (!userId) return;
      setIsLoading(true);
      try {
        const dayIndex = selectedDate.getDay();
        const dayKey = `Day_${dayIndex === 0 ? 7 : dayIndex}`;

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

  // --- THE NEW LOG PROGRESS FUNCTION ---
  const handleLogExercise = (status: 'complete' | 'partial') => {
    const dateStr = toDateString(selectedDate);
    const increment = status === 'complete' ? 20 : 10;
    
    setDayDataMap(prev => {
      const currentDay = prev[dateStr] || { type: 'workout', progress: 0 };
      const newProgress = Math.min(currentDay.progress + increment, 100);
      
      if (newProgress === 100) toast.success("Daily Protocol 100% Complete! 🔥");
      
      return {
        ...prev,
        [dateStr]: { ...currentDay, progress: newProgress }
      };
    });

    // Optional: Add fetch call here if you want to save the % progress directly to the DB!
  };

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
          <div className="h-full overflow-y-auto pt-10 pb-20">
            <h2 className="text-2xl font-semibold tracking-tight text-gray-800 mb-7 ml-6">
              Monthly Progress
            </h2>
            <div className="px-6 mb-10">
              <StreakCalendar history={dayDataMap} />
            </div>
            
            <MacrocycleSidebar userId={userId as string} />
          </div>
        )}
      </section>

      <div className="fixed top-0 left-0 w-full md:w-2/3 h-screen bg-white overflow-y-auto font-sans shadow-sm">
        <div className="px-8 pt-12 pb-8 max-w-4xl mx-auto">
          
          <div className="flex items-center justify-between mb-10">
            <div className="flex items-center gap-6">
              <div className="flex items-center space-x-3 bg-slate-50 p-1.5 rounded-full border border-slate-100">
                <button onClick={handlePrevWeek} className="p-2 bg-white shadow-sm rounded-full hover:bg-slate-100 transition-colors active:scale-95">
                  <ChevronLeft className="w-5 h-5 text-slate-700" />
                </button>
                <span className="text-sm font-semibold tracking-wide text-slate-700 min-w-22.5 text-center uppercase">
                  {toDateString(currentWeekStart) === toDateString(new Date(new Date().setDate(new Date().getDate() - new Date().getDay() + 1))) 
                    ? "This week" 
                    : currentWeekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                </span>
                <button onClick={handleNextWeek} className="p-2 bg-white shadow-sm rounded-full hover:bg-slate-100 transition-colors active:scale-95">
                  <ChevronRight className="w-5 h-5 text-slate-700" />
                </button>
              </div>
            </div>
          </div>

          <div className="flex justify-between w-full px-2 sm:px-4 select-none mb-10 overflow-x-auto pb-4">
            {weekDays.map((day, index) => {
              // --- STREAK NOW MAINTAINS IF PROGRESS IS >= 70% ---
              const isComplete = day.progress >= 70;
              const prevComplete = index > 0 && weekDays[index - 1].progress >= 70;
              const nextComplete = index < 6 && weekDays[index + 1].progress >= 70;
              const isRest = day.type === 'rest';

              let streakBgClass = "bg-transparent";
              if (isComplete) {
                // Color match the background pill to the progress status
                if (isRest) {
                  streakBgClass = "bg-emerald-100/50";
                } else if (day.progress === 100) {
                  streakBgClass = "bg-emerald-100/50";
                } else if (day.progress >= 75) {
                  streakBgClass = "bg-yellow-100/50";
                } else {
                  streakBgClass = "bg-blue-100/50";
                }

                if (!prevComplete && nextComplete) streakBgClass += " rounded-l-full scale-y-110";
                else if (prevComplete && !nextComplete) streakBgClass += " rounded-r-full scale-y-110";
                else if (prevComplete && nextComplete) streakBgClass += " scale-y-110";
                else streakBgClass += " rounded-full scale-y-110";
              }

              return (
                <div 
                  key={day.dateStr} 
                  className="relative flex-1 min-w-15 flex flex-col items-center group cursor-pointer" 
                  onClick={() => setSelectedDate(day.date)}
                >
                  <div className={`absolute top-0 bottom-9 w-full transition-all duration-300 ease-in-out ${streakBgClass}`} />

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
                      <Dumbbell className={`w-5 h-5 transition-colors duration-300 ${isComplete ? (day.progress === 100 ? 'text-emerald-500 fill-emerald-500' : day.progress >= 75 ? 'text-yellow-500 fill-yellow-500' : 'text-blue-500 fill-blue-500') : 'text-slate-300 fill-slate-300'}`} />
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-end mt-4 pr-4">
         <button 
              onClick={() => setIsEditModalOpen(true)}
              className="flex items-center text-sm font-semibold text-slate-700 bg-white border border-slate-200 shadow-sm hover:border-blue-300 hover:bg-blue-50 hover:text-blue-600 px-4 py-2 rounded-full transition-all"
            >
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
              </svg>
              Edit Week
            </button>
          </div>

      <EditWeekModal 
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        initialDays={currentWeekDays}       // <--- Now perfectly dynamic!
        activePhase={userActivePhase}       // <--- Now perfectly dynamic!
        onSave={handleSaveNewSchedule}
      />
    
      <SwapExerciseModal 
        isOpen={swapModalOpen}
        onClose={() => setSwapModalOpen(false)}
        userId={userId as string}
        dayKey={getDayKey(selectedDate)} // e.g. "Day_3"
        originalExerciseName={exerciseToSwap}
      />

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
                        onLog={(status: 'complete' | 'partial') => handleLogExercise(status)} // <-- PASSING THE PROP HERE
                        onSwapClick={() => {
                          setExerciseToSwap(exerciseData.exercise_name || exerciseData.exercise);
                          setSwapModalOpen(true);
                        }}

                      />
                    );
                  })
              )}
            </div>
          </div>

        </div>
      </div>
    
     {/* --- NEW: The Intervention Modal --- */}
        {showInterventionModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-sm p-4 animate-in fade-in duration-300">
            <div className="bg-white rounded-3xl shadow-2xl max-w-md w-full overflow-hidden border border-slate-200 animate-in zoom-in-95 duration-300">
              
              {/* Header */}
              <div className="p-6 border-b border-orange-100 flex items-center gap-4 bg-orange-50/50">
                <div className="p-2 bg-orange-100 rounded-full">
                  <AlertTriangle className="w-6 h-6 text-orange-600" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-800 tracking-tight">Missed Workout</h3>
                  <p className="text-xs font-semibold text-orange-600 uppercase tracking-wider">Intervention Required</p>
                </div>
              </div>
              
              {/* Body */}
              <div className="p-6">
                <p className="text-sm text-slate-600 mb-6 leading-relaxed">
                  It looks like you missed your last scheduled workout. How would you like the AI engine to adjust your macrocycle to keep you on track?
                </p>
                
                <div className="flex flex-col gap-3">
                  {/* 🎯 Trigger handleResolution with 'shift' */}
                  <button 
                    onClick={() => {
                      setIsResolving(true);
                      handleResolution('shift');
                    }}
                    disabled={isResolving}
                    className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition-all flex justify-center items-center gap-2 shadow-sm"
                  >
                    {isResolving ? <Loader2 className="w-5 h-5 animate-spin" /> : <Merge className="w-5 h-5" />}
                    Shift Schedule (Recommended)
                  </button>
                  
                  {/* 🎯 Trigger handleResolution with 'skip' */}
                  <button 
                    onClick={() => {
                      setIsResolving(true);
                      handleResolution('skip');
                    }}
                    disabled={isResolving}
                    className="w-full py-3 px-4 bg-white border-2 border-slate-200 hover:border-red-200 hover:bg-red-50 text-slate-600 hover:text-red-600 font-semibold rounded-xl transition-all flex justify-center items-center gap-2"
                  >
                    <X className="w-5 h-5" />
                    Skip Workout
                  </button>
                </div>
              </div>

            </div>
          </div>
        )}
      </div> {/* <--- THIS WAS MISSING! */}
  );
}

// ... [MacrocycleSidebar & ExerciseDetailPanel stay exactly the same] ...
function MacrocycleSidebar({ userId }: { userId?: string }) {
  const [data, setData] = useState<MacrocycleData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;

    const fetchMacrocycle = async () => {
      setIsLoading(true);
      setErrorMsg(null);
      try {
        const res = await fetch(`http://127.0.0.1:5001/api/workout/macrocycle?user_id=${userId}`);
        if (!res.ok) throw new Error(`Server crashed with status: ${res.status}`);
        const result = await res.json();
        if (result.status === "success" && result.phases) {
          setData(result);
        } else {
          setErrorMsg(result.message || "Invalid data format received.");
        }
      } catch (err: any) {
        setErrorMsg("Failed to connect to the ThinkFit engine.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchMacrocycle();
  }, [userId]);

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

  if (isLoading) {
    return (
      <div className="px-6 pb-8 border-t border-zinc-200 pt-8 mt-2">
        <div className="animate-pulse">
          <div className="h-6 w-48 bg-slate-200 rounded mb-2"></div>
          <div className="h-4 w-32 bg-slate-100 rounded mb-8"></div>
          <div className="h-24 w-full bg-slate-100 rounded-xl mb-6"></div>
          <div className="space-y-4">
            <div className="h-16 w-full bg-slate-50 rounded-lg border border-slate-100"></div>
            <div className="h-16 w-full bg-slate-50 rounded-lg border border-slate-100"></div>
          </div>
        </div>
      </div>
    );
  }

  if (errorMsg || !data) return null;

  const progressPercentage = Math.round((data.current_week / data.total_weeks) * 100);

  return (
    <div className="px-6 pb-8 border-t border-zinc-200 pt-8 mt-2">
      <div className="mb-6">
        <h3 className="text-xl font-bold text-slate-800 tracking-tight flex items-center gap-2 mb-1">
          <Map className="w-5 h-5 text-blue-600" /> Program Roadmap
        </h3>
        <p className="text-sm text-slate-500">
          Optimized for <span className="font-semibold text-slate-700 capitalize">{data.goal?.replace(/_/g, ' ') || 'Recomposition'}</span>
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

      <div className="space-y-4 relative before:absolute before:inset-0 before:ml-3.75 before:h-full before:w-0.5 before:bg-linear-to-b before:from-transparent before:via-slate-200 before:to-transparent">
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
                <h4 className={`text-sm font-bold mb-1 ${isPast ? 'text-slate-500' : 'text-slate-800'}`}>{phase.phase?.replace(/_/g, ' ')}</h4>
                <p className={`text-xs leading-relaxed ${isPast ? 'text-slate-400' : 'text-slate-600'}`}>{phase.focus}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ExerciseDetailPanel({ exercise, onClose }: { exercise: ExerciseData; onClose: () => void }) {
  return ( 
    <div className="p-6">
       <button onClick={onClose} className="mb-4 text-blue-500 flex items-center gap-2 text-sm font-semibold hover:text-blue-700">
           <X className="w-4 h-4" /> Close Details
       </button>
       <h3 className="text-xl font-bold text-slate-800">{exercise.exercise_name || (exercise as any).name}</h3>
       {/* Details content will render here based on your existing implementation */}
    </div> 
  );
}

// --- UPDATED PROGRESS COMPONENT WITH NEW COLOR LOGIC ---
function CircularProgress({ progress, label, isToday, theme }: { progress: number; label: string; isToday: boolean; theme: 'blue' | 'green' }) {
  const radius = 24; 
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;
  
  // Base colors for Blue (Workout) vs Green (Rest Day)
  let colorTheme = { 
    textActive: 'text-blue-600', 
    strokeFull: 'text-blue-500', 
    strokePartial: 'text-blue-500' 
  };

  if (theme === 'green') {
    colorTheme = { textActive: 'text-emerald-600', strokeFull: 'text-emerald-500', strokePartial: 'text-emerald-500' };
  } else {
    // Dynamic color logic for workout progress
    if (progress === 100) {
      colorTheme = { textActive: 'text-emerald-600', strokeFull: 'text-emerald-500', strokePartial: 'text-emerald-500' };
    } else if (progress >= 75) {
      colorTheme = { textActive: 'text-yellow-600', strokeFull: 'text-yellow-500', strokePartial: 'text-yellow-500' };
    }
  }

  const textColor = isToday || progress > 0 ? `${colorTheme.textActive} font-bold` : 'text-slate-400 font-medium';

  return (
    <div className="relative flex items-center justify-center w-16 h-16 bg-white rounded-full">
      <svg className="w-full h-full transform -rotate-90 drop-shadow-sm" viewBox="0 0 56 56">
        <circle cx="28" cy="28" r={radius} stroke="currentColor" strokeWidth="5" fill="transparent" className="text-slate-100" />
        {progress > 0 && (
          <circle cx="28" cy="28" r={radius} stroke="currentColor" strokeWidth="5" fill="transparent" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset} strokeLinecap="round" className={`${colorTheme.strokePartial} transition-all duration-500 ease-out`} />
        )}
      </svg>
      <span className={`absolute text-base tracking-wide ${textColor}`}>{label}</span>
    </div>
  );
}