'use client';

import React, { useState, useMemo, useEffect, useCallback } from 'react';
import { 
  ChevronLeft, ChevronRight, Dumbbell, BatteryCharging,
  X, Target, Activity, Settings2, Info, VideoOff
} from 'lucide-react';
import StreakCalendar from "@/components/StreakCalendar";
import ExerciseCard, { type ExerciseData } from "@/components/ExerciseCard";
import RestDayCard from "@/components/RestDayCard";

const toDateString = (date: Date) => {
  const d = new Date(date);
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().split('T')[0];
};

type DayData = {
  type: 'workout' | 'rest';
  progress: number; 
  exerciseCompletion: Record<string, number>; 
};

export default function Page() {
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

  const TEST_USER_ID = "ALEX_001";

  const getDayKey = (date: Date) => {
    const dayIndex = date.getDay();
    return `Day_${dayIndex === 0 ? 7 : dayIndex}`;
  };

  useEffect(() => {
    const fetchWeekData = async () => {
      setIsLoading(true);
      try {
        const dayKey = getDayKey(selectedDate);
        let res = await fetch(`http://127.0.0.1:5001/api/workout/today?user_id=${TEST_USER_ID}&day_key=${dayKey}`);
        
        if (res.status === 404) {
          await fetch(`http://127.0.0.1:5001/api/workout/generate_week`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: TEST_USER_ID, equipment: [] })
          });
          res = await fetch(`http://127.0.0.1:5001/api/workout/today?user_id=${TEST_USER_ID}&day_key=${dayKey}`);
        }

        const data = await res.json();
        const dateStr = toDateString(selectedDate);

        if (data.status === "success" || data.is_rest_day) {
           setWeeklyProgram((prev: any) => ({ ...prev, [dayKey]: data.today_workout }));
           
           setDayDataMap(prevMap => {
             if (prevMap[dateStr]) return prevMap;
             return {
               ...prevMap,
               [dateStr]: {
                 type: data.is_rest_day ? 'rest' : 'workout',
                 progress: data.is_rest_day ? 100 : 0,
                 exerciseCompletion: {}
               }
             };
           });
        }
      } catch (err) { console.error(err); } finally { setIsLoading(false); }
    };
    fetchWeekData();
  }, [selectedDate]);

  // --- STABILIZED PROGRESS LOGIC ---
  const handleExerciseProgress = useCallback((exerciseId: string, completionRatio: number) => {
    const dateStr = toDateString(selectedDate);
    const dayKey = getDayKey(selectedDate);
    
    setDayDataMap(prev => {
      const currentDay = prev[dateStr] || { type: 'workout', progress: 0, exerciseCompletion: {} };
      
      // Guard: If the completion for this specific exercise hasn't changed, do nothing
      if (currentDay.exerciseCompletion[exerciseId] === completionRatio) {
        return prev;
      }

      const updatedCompletions = { ...currentDay.exerciseCompletion, [exerciseId]: completionRatio };
      const exercises = weeklyProgram?.[dayKey] || [];
      const totalExercises = exercises.length;
      
      let newProgress = currentDay.type === 'rest' ? 100 : 0;
      if (totalExercises > 0) {
        const sumOfCompletion = Object.values(updatedCompletions).reduce((a, b) => a + b, 0);
        newProgress = Math.round((sumOfCompletion / totalExercises) * 100);
      }

      // Guard: If the total daily progress hasn't changed, don't trigger a re-render
      if (currentDay.progress === newProgress && currentDay.exerciseCompletion[exerciseId] === completionRatio) {
        return prev;
      }

      return { 
        ...prev, 
        [dateStr]: { ...currentDay, exerciseCompletion: updatedCompletions, progress: newProgress } 
      };
    });
  }, [selectedDate, weeklyProgram]);

  const weekDays = useMemo(() => {
    const todayStr = toDateString(new Date());
    const selectedStr = toDateString(selectedDate);

    return Array.from({ length: 7 }).map((_, i) => {
      const date = new Date(currentWeekStart);
      date.setDate(currentWeekStart.getDate() + i);
      const dateStr = toDateString(date);
      const data = dayDataMap[dateStr] || { type: 'workout', progress: 0 };
      
      return {
        date, dateStr,
        label: date.toLocaleDateString('en-US', { weekday: 'short' }).slice(0, 2),
        ...data,
        isToday: dateStr === todayStr,
        isSelected: dateStr === selectedStr,
      };
    });
  }, [currentWeekStart, dayDataMap, selectedDate]);

  const currentDayExercises = weeklyProgram ? (weeklyProgram[getDayKey(selectedDate)] || []) : [];
  const selectedStr = toDateString(selectedDate);

  return (
    <div className="flex min-h-screen bg-white">
      <div className="w-full md:w-2/3 h-screen overflow-y-auto">
        <div className="px-6 md:px-12 pt-10 pb-20 max-w-4xl mx-auto">
          
          <div className="flex items-center justify-left mb-12">
            <div className="flex items-center space-x-3 bg-slate-50 p-1.5 rounded-full border border-slate-100 shadow-sm">
              <button onClick={() => setCurrentWeekStart(new Date(currentWeekStart.setDate(currentWeekStart.getDate() - 7)))} className="p-2 bg-white shadow-sm rounded-full">
                <ChevronLeft className="w-5 h-5 text-slate-700" />
              </button>
              <span className="text-sm font-semibold min-w-25 text-center uppercase">
                {toDateString(currentWeekStart) === toDateString(new Date(new Date().setDate(new Date().getDate() - new Date().getDay() + 1))) ? "This week" : currentWeekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </span>
              <button onClick={() => setCurrentWeekStart(new Date(currentWeekStart.setDate(currentWeekStart.getDate() + 7)))} className="p-2 bg-white shadow-sm rounded-full">
                <ChevronRight className="w-5 h-5 text-slate-700" />
              </button>
            </div>
          </div>

          <div className="flex justify-between w-full px-2 mb-10 overflow-x-auto pb-4 gap-2">
            {weekDays.map((day) => (
              <div key={day.dateStr} className="flex-1 min-w-15 flex flex-col items-center cursor-pointer" onClick={() => setSelectedDate(day.date)}>
                 <CircularProgress progress={day.progress} label={day.label} isToday={day.isToday} isSelected={day.isSelected} />
                 <div className="mt-4">
                   {day.type === 'rest' ? (
                     <BatteryCharging className={`w-5 h-5 ${day.progress === 100 ? 'text-emerald-500' : 'text-slate-300'}`} />
                   ) : (
                     <Dumbbell className={`w-5 h-5 ${day.progress === 100 ? 'text-emerald-500' : day.progress >= 75 ? 'text-amber-500' : 'text-slate-300'}`} />
                   )}
                 </div>
              </div>
            ))}
          </div>

          <div className="mt-12 border-t border-zinc-100 pt-8">
            <h3 className="text-xl font-bold text-zinc-900 mb-6">
               {selectedStr === toDateString(new Date()) ? "Today's Protocol" : `${selectedDate.toLocaleDateString('en-US', { weekday: 'long' })}'s Protocol`}
            </h3>
            
            <div className="flex flex-col gap-6">
              {isLoading ? (
                <div className="py-10 text-center text-zinc-400 animate-pulse">Syncing...</div>
              ) : currentDayExercises.length === 0 ? (
                <RestDayCard />
              ) : (
                currentDayExercises.map((ex: any, i: number) => (
                  <ExerciseCard 
                    key={i} 
                    exercise={ex} 
                    onOpenDetails={() => setActiveExercise(ex)}
                    onProgressUpdate={(ratio) => handleExerciseProgress(ex.exercise_id, ratio)} 
                  />
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      <section className="hidden md:block w-1/3 h-screen bg-zinc-50 border-l border-zinc-200 fixed right-0 top-0 overflow-y-auto">
        <div className="pt-10 px-8">
          {activeExercise ? (
            <ExerciseDetailPanel exercise={activeExercise} onClose={() => setActiveExercise(null)} />
          ) : (
            <div className="animate-in fade-in slide-in-from-right-4">
              <h2 className="text-2xl font-bold tracking-tight text-gray-800 mb-6">Monthly Progress</h2>
              <StreakCalendar history={dayDataMap} />
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

function CircularProgress({ progress, label, isToday, isSelected }: { progress: number; label: string; isToday: boolean; isSelected: boolean }) {
  const radius = 24; 
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (progress / 100) * circumference;
  const themeColor = progress === 100 ? 'text-emerald-500' : progress >= 75 ? 'text-amber-500' : 'text-blue-500';

  return (
    <div className="relative flex items-center justify-center w-16 h-16 bg-white rounded-full">
      <svg className="w-full h-full transform -rotate-90" viewBox="0 0 56 56">
        <circle cx="28" cy="28" r={radius} stroke="currentColor" strokeWidth="5" fill="transparent" className="text-slate-100" />
        {progress > 0 && <circle cx="28" cy="28" r={radius} stroke="currentColor" strokeWidth="5" fill="transparent" strokeDasharray={circumference} strokeDashoffset={strokeDashoffset} strokeLinecap="round" className={`${themeColor} transition-all duration-700 ease-in-out`} />}
      </svg>
      <span className={`absolute text-xs tracking-tighter ${isSelected ? 'font-bold text-slate-900' : 'text-slate-500'}`}>{label}</span>
      {isToday && <div className="absolute -top-1 w-1.5 h-1.5 bg-blue-500 rounded-full" />}
    </div>
  );
}

function ExerciseDetailPanel({ exercise, onClose }: { exercise: ExerciseData; onClose: () => void }) {
  const youtubeEmbedUrl = `https://www.youtube.com/embed/${exercise.youtube_id}?rel=0`;
  return (
    <div className="h-full flex flex-col animate-in slide-in-from-right-4 duration-300">
      <div className="flex items-center justify-between mb-8">
        <h2 className="text-xl font-bold text-zinc-900">{exercise.exercise_name}</h2>
        <button onClick={onClose} className="p-2 hover:bg-zinc-200 rounded-full transition-colors"><X className="w-5 h-5 text-zinc-500" /></button>
      </div>
      <div className="space-y-8 overflow-y-auto pb-10">
        <div className="w-full aspect-video bg-zinc-900 rounded-2xl overflow-hidden shadow-lg relative">
          <iframe src={youtubeEmbedUrl} className="w-full h-full absolute top-0 left-0" allowFullScreen />
        </div>
      </div>
    </div>
  );
}