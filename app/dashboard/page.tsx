'use client';

import React, { useState, useMemo } from 'react';
import { ChevronLeft, ChevronRight, User, Dumbbell, BatteryCharging } from 'lucide-react';
import StreakCalendar from "@/components/StreakCalendar";
import ExerciseCard from "@/components/ExerciseCard";
import RestDayCard from "@/components/RestDayCard";

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
  
  // Format the title dynamically (e.g. "Today's Protocol" or "Monday's Protocol")
  const isSelectedToday = selectedStr === toDateString(new Date());
  const protocolTitle = isSelectedToday 
    ? "Today's Protocol" 
    : `${selectedDate.toLocaleDateString('en-US', { weekday: 'long' })}'s Protocol`;

  return (
    <div>
      {/* RIGHT SIDE: Calendar */}
      <section className="fixed top-0 right-0 w-1/3 h-screen bg-zinc-50 border-l border-zinc-200 overflow-y-auto font-sans shadow-lg hidden md:block">
        <h2 className="text-2xl font-semibold tracking-tight text-gray-800 mb-4 ml-6 mt-8">
          Monthly Progress
        </h2>
        <div className="px-6">
          <StreakCalendar />
        </div>
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
                  onClick={() => setSelectedDate(day.date)} // Updated: Now selects the day
                >
                  {/* Background continuous streak pill */}
                  <div className={`absolute top-0 bottom-[36px] w-full transition-all duration-300 ease-in-out ${streakBgClass}`} />

                  {/* The Circular Progress & Day Label */}
                  <div className={`relative z-10 pt-2 transform transition-transform ${isRest ? '' : 'group-hover:scale-105 active:scale-95'}`}>
                    {/* Ring to show which day is currently selected */}
                    <div className={`rounded-full transition-all duration-200 ${day.isSelected ? 'ring-4 ring-slate-100 shadow-sm scale-105' : ''}`}>
                      <CircularProgress 
                        progress={day.progress} 
                        label={day.label} 
                        isToday={day.isToday} 
                        theme={isRest ? 'green' : 'blue'}
                      />
                    </div>
                  </div>

                  {/* Icon below the circle */}
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
          <div className="mt-12 border-t border-zinc-100 pt-8">
            <h3 className="text-xl font-bold text-zinc-900 mb-6">{protocolTitle}</h3>
            
            <div className="flex flex-col gap-6">
              {selectedData.type === 'rest' ? (
                <RestDayCard />
              ) : (
                <>
                  <ExerciseCard />
                  {/* You can add more cards here */}
                </>
              )}
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

// --- SVG Circular Progress Component (Unchanged) ---
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