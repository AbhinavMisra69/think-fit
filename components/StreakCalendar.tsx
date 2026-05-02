'use client';

import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, Flame } from 'lucide-react';

export default function StreakCalendar({ history = {} }: { history: any }) {
  // Default to today's date instead of Jan 2022
  const [currentDate, setCurrentDate] = useState(new Date());
  
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  const year = currentDate.getFullYear();
  const month = currentDate.getMonth();

  const daysInMonth = new Date(year, month + 1, 0).getDate();
  const firstDayOfMonth = (new Date(year, month, 1).getDay() + 6) % 7; 

  const handlePrevMonth = () => setCurrentDate(new Date(year, month - 1, 1));
  const handleNextMonth = () => setCurrentDate(new Date(year, month + 1, 1));

  const getStatus = (day: number) => {
    const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const dayData = history[dateStr];
    const checkDate = new Date(year, month, day);
    
    // Logic: 80% or 100% completion (Rest days are auto-100)
    const isFulfilled = dayData && dayData.progress >= 80;
    const isPast = checkDate < today;
    const isToday = checkDate.getTime() === today.getTime();

    return { isFulfilled, isPast, isToday };
  };

  const monthName = currentDate.toLocaleString('default', { month: 'short' }).toUpperCase();

  const blanks = Array.from({ length: firstDayOfMonth }, (_, i) => <div key={`blank-${i}`} className="h-10 w-10" />);
  
  const days = Array.from({ length: daysInMonth }, (_, i) => {
    const dayNum = i + 1;
    const { isFulfilled, isPast, isToday } = getStatus(dayNum);
    
    const prev = getStatus(dayNum - 1);
    const next = getStatus(dayNum + 1);

    // Pill background logic only for streaks of Fire
    const isStartOfStreak = isFulfilled && !prev.isFulfilled && next.isFulfilled;
    const isEndOfStreak = isFulfilled && prev.isFulfilled && !next.isFulfilled;
    const isMiddleOfStreak = isFulfilled && prev.isFulfilled && next.isFulfilled;

    let wrapperClass = "relative flex h-12 items-center justify-center";
    if (isStartOfStreak) wrapperClass += " bg-orange-100 rounded-l-full ml-1 w-[calc(100%-4px)]";
    else if (isEndOfStreak) wrapperClass += " bg-orange-100 rounded-r-full mr-1 w-[calc(100%-4px)]";
    else if (isMiddleOfStreak) wrapperClass += " bg-orange-100 w-full";

    return (
      <div key={`day-${dayNum}`} className={wrapperClass}>
        <div
          className={`h-9 w-9 rounded-full flex items-center justify-center transition-all duration-200 z-10 ${
            isFulfilled 
              ? 'bg-amber-400 shadow-sm' 
              : isToday 
                ? 'bg-blue-50 border-2 border-blue-200' 
                : 'bg-zinc-50'
          }`}
        >
          {isFulfilled ? (
            <Flame className="h-5 w-5 text-orange-600 fill-orange-500 animate-in zoom-in duration-300" />
          ) : isPast ? (
            <span className="text-lg grayscale opacity-60">😢</span>
          ) : (
            <span className={`text-[10px] font-bold ${isToday ? 'text-blue-600' : 'text-zinc-400'}`}>
              {dayNum}
            </span>
          )}
        </div>
        {isToday && !isFulfilled && (
          <div className="absolute bottom-1 w-1 h-1 bg-blue-500 rounded-full" />
        )}
      </div>
    );
  });

  return (
    <div className="w-full max-w-md mx-auto bg-white rounded-3xl shadow-sm border border-zinc-100 p-6 font-sans">
      
      <div className="flex items-center justify-between mb-6 px-2">
        <button onClick={handlePrevMonth} className="p-2 text-zinc-400 hover:text-zinc-700">
          <ChevronLeft className="w-5 h-5" />
        </button>
        <h2 className="text-sm font-bold tracking-widest text-slate-800">
          {monthName} {year}
        </h2>
        <button onClick={handleNextMonth} className="p-2 text-zinc-400 hover:text-zinc-700">
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>

      <div className="grid grid-cols-7 gap-y-4">
        {['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'].map((day) => (
          <div key={day} className="text-center text-[10px] font-bold text-zinc-400 tracking-wider">
            {day}
          </div>
        ))}

        {blanks}
        {days}
      </div>

    </div>
  );
}