'use client';

import React, { useState, useMemo } from 'react';
import { ChevronLeft, ChevronRight, Flame } from 'lucide-react';

type Goal = {
  id: string;
  title: string;
};

const DUMMY_GOALS: Goal[] = [
  { id: '1', title: 'Read for 30 minutes' },
  { id: '2', title: '45-minute Workout' },
  { id: '3', title: 'Meditate' },
];

export default function StreakCalendar() {
  const [currentDate, setCurrentDate] = useState(new Date(2022, 0, 1)); // Starting at Jan 2022 to match the image
  const [selectedGoal, setSelectedGoal] = useState<string>(DUMMY_GOALS[0].id);
  
  // Storing completed dates as a Set of 'YYYY-MM-DD' strings for O(1) lookup
  const [completedDates, setCompletedDates] = useState<Record<string, Set<string>>>({
    '1': new Set(['2022-01-04', '2022-01-08', '2022-01-12', '2022-01-17', '2022-01-18', '2022-01-19', '2022-01-20', '2022-01-21', '2022-01-22', '2022-01-23', '2022-01-24', '2022-01-25', '2022-01-27', '2022-01-29']),
  });

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const daysInMonth = new Date(year, month + 1, 0).getDate();
  // Adjusting so Monday is the first day of the week (0 = Mon, 6 = Sun)
  const firstDayOfMonth = (new Date(year, month, 1).getDay() + 6) % 7; 

  const handlePrevMonth = () => setCurrentDate(new Date(year, month - 1, 1));
  const handleNextMonth = () => setCurrentDate(new Date(year, month + 1, 1));

  const toggleDate = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    
    setCompletedDates(prev => {
      const goalDates = new Set(prev[selectedGoal] || []);
      if (goalDates.has(dateStr)) {
        goalDates.delete(dateStr);
      } else {
        goalDates.add(dateStr);
      }
      return { ...prev, [selectedGoal]: goalDates };
    });
  };

  const isCompleted = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    return completedDates[selectedGoal]?.has(dateStr);
  };

  const monthName = currentDate.toLocaleString('default', { month: 'short' }).toUpperCase();

  // Generate grid items
  const blanks = Array.from({ length: firstDayOfMonth }, (_, i) => <div key={`blank-${i}`} className="h-10 w-10" />);
  
  const days = Array.from({ length: daysInMonth }, (_, i) => {
    const day = i + 1;
    const completed = isCompleted(day);
    const prevCompleted = isCompleted(day - 1);
    const nextCompleted = isCompleted(day + 1);

    // Logic to determine if we need the connecting "pill" background
    const isStartOfStreak = completed && !prevCompleted && nextCompleted;
    const isEndOfStreak = completed && prevCompleted && !nextCompleted;
    const isMiddleOfStreak = completed && prevCompleted && nextCompleted;
    const isIsolated = completed && !prevCompleted && !nextCompleted;

    // Tailwind classes for the pill background connections
    let wrapperClass = "relative flex h-10 items-center justify-center";
    if (isStartOfStreak) wrapperClass += " bg-orange-100 rounded-l-full ml-1 w-[calc(100%-4px)]";
    else if (isEndOfStreak) wrapperClass += " bg-orange-100 rounded-r-full mr-1 w-[calc(100%-4px)]";
    else if (isMiddleOfStreak) wrapperClass += " bg-orange-100 w-full";
    else if (isIsolated) wrapperClass += " bg-transparent";

    return (
      <div key={`day-${day}`} className={wrapperClass}>
        <button
          onClick={() => toggleDate(day)}
          className={`h-8 w-8 rounded-full flex items-center justify-center transition-all duration-200 z-10 ${
            completed 
              ? 'bg-amber-400 shadow-sm' 
              : 'bg-zinc-100 hover:bg-zinc-200'
          }`}
        >
          {completed && <Flame className="h-4 w-4 text-orange-600 fill-orange-500" />}
        </button>
      </div>
    );
  });

  return (
    <div className="w-full max-w-md mx-auto bg-white rounded-3xl shadow-sm border border-zinc-100 p-6 font-sans">
      
      {/* Header / Month Navigation */}
      <div className="flex items-center justify-between mb-6 px-2">
        <button onClick={handlePrevMonth} className="p-2 text-zinc-400 hover:text-zinc-700 transition-colors">
          <ChevronLeft className="w-5 h-5" />
        </button>
        <h2 className="text-lg font-semibold tracking-wide text-slate-800">
          {monthName} {year}
        </h2>
        <button onClick={handleNextMonth} className="p-2 text-zinc-400 hover:text-zinc-700 transition-colors">
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>

      <div className="w-full h-px bg-zinc-100 mb-6" />

      {/* Days of Week Header */}
      <div className="grid grid-cols-7 gap-y-4 mb-4">
        {['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'].map((day) => (
          <div key={day} className="text-center text-xs font-semibold text-slate-800 tracking-wider">
            {day}
          </div>
        ))}

        {/* Calendar Grid */}
        {blanks}
        {days}
      </div>

    </div>
  );
}