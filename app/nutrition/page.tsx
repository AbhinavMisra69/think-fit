'use client';

import React, { useState, useEffect } from 'react';
import { ChevronDown, Flame, MoreHorizontal } from 'lucide-react';
import MealSection from "@/components/MealSection"; 

// --- Types & Interfaces ---
type MacroData = {
  current: number;
  target: number;
  unit: string;
  colorClass: string;
  bgClass: string;
};

interface NutritionPayload {
  calories: {
    current: number;
    target: number;
  };
  macros: {
    carbs: MacroData;
    protein: MacroData;
    satFat: MacroData;
  };
}

interface WeeklyProgressDay {
  day: string;
  date: number;
  progress: number;
  isSelected?: boolean;
}

const defaultDescriptions = {
  calories: 'Total Consumed',
  carbs: 'Energy Source',
  protein: 'Muscle Recovery',
  satFat: 'Daily Maximum Limit',
};

export default function NutritionPage({ descriptions = defaultDescriptions }) {
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [nutritionData, setNutritionData] = useState<NutritionPayload | null>(null);
  
  // NEW: State to hold the weekly progress dictionary from the DB
  const [weeklyData, setWeeklyData] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);

  // UPDATED: Fetch both Daily and Weekly data
  useEffect(() => {
    async function fetchData() {
      try {
        const dailyRes = await fetch('/api/nutrition/today');
        const weeklyRes = await fetch('/api/nutrition/weekly');
  
        // If Flask sends a 500 error, this text() check will show you the HTML error
        if (!dailyRes.ok) {
          const errorText = await dailyRes.text();
          console.error("Flask Daily Error:", errorText);
          return;
        }
  
        setNutritionData(await dailyRes.json());
        setWeeklyData(await weeklyRes.json());
      } catch (error) {
        console.error("Network or JSON Error:", error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  // UPDATED: Dynamic Week Generator wired to the Database
  const generateWeek = (baseDate: Date): WeeklyProgressDay[] => {
    const current = new Date(baseDate);
    const dayOfWeek = current.getDay(); 
    const distanceToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1; 
    current.setDate(current.getDate() - distanceToMonday);
    
    const dayNames = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'];
    const week: WeeklyProgressDay[] = [];
    
    for (let i = 0; i < 7; i++) {
      const dayDate = new Date(current);
      dayDate.setDate(current.getDate() + i);
      
      // Format to YYYY-MM-DD perfectly to match the backend dictionary
      const yyyy = dayDate.getFullYear();
      const mm = String(dayDate.getMonth() + 1).padStart(2, '0');
      const dd = String(dayDate.getDate()).padStart(2, '0');
      const formattedDate = `${yyyy}-${mm}-${dd}`;
      
      week.push({
        day: dayNames[i],
        date: dayDate.getDate(),
        isSelected: dayDate.toDateString() === baseDate.toDateString(),
        // Check the database dictionary for this date. If empty, default to 0.
        progress: weeklyData[formattedDate] || 0, 
      });
    }
    return week;
  };

  // Run the generator
  const weeklyProgress = generateWeek(selectedDate);
  if (isLoading || !nutritionData) {
    return (
      <div className="flex w-full h-screen bg-[#f8fafc]">
        <div className="fixed top-0 left-0 w-full md:w-1/2 h-screen bg-[#fafbfc] flex items-center justify-center border-r border-slate-200/60 z-10">
          <p className="text-slate-500 font-medium animate-pulse">Loading Summary...</p>
        </div>
        <div className="ml-[50%] w-1/2 min-h-screen">
           <MealSection />
        </div>
      </div>
    );
  }

  const { calories, macros } = nutritionData;

  const radius = 90;
  const circumference = Math.PI * radius; 
  const caloriePercent = Math.min((calories.current / calories.target) * 100, 100);
  const displayCalories = Math.round(calories.current);

  return (
    <div className="flex w-full min-h-screen bg-[#f8fafc]">
      
      {/* --- RIGHT SIDE: Meal Section (Scrollable) --- */}
      <div className="hidden md:block md:ml-[50%] md:w-1/2 min-h-screen bg-[#f8fafc]">
        <MealSection />
      </div>

      {/* --- LEFT SIDE: Nutrition Sidebar (Fixed/Sticky) --- */}
      <div className="fixed top-0 left-0 w-full md:w-1/2 h-screen bg-[#fafbfc] font-sans border-r border-slate-200/60 flex flex-col z-10">
        <div className="p-8 md:p-12 flex-1 overflow-y-auto hide-scrollbar">
          
          {/* Top Weekly Tracker */}
          <div className="mb-12">
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-xl font-bold text-slate-900 tracking-tight flex items-center gap-2 cursor-pointer hover:text-slate-600 transition-colors">
                Today, {selectedDate.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}
                <ChevronDown className="w-5 h-5 text-slate-400 mt-0.5" />
              </h2>
            </div>

            <div className="flex justify-between gap-3 overflow-x-auto pb-4 select-none hide-scrollbar">
              {weeklyProgress.map((day, idx) => {
                const isSelected = day.isSelected;
                
                // Color Logic based on ranges
                let bgColor = "bg-white";
                let borderColor = "border-slate-100";
                let dayTextColor = "text-slate-400";
                let dateTextColor = "text-slate-800";
                let shadowClass = "shadow-sm group-hover:shadow-md";

                if (day.progress > 0) {
                  if (day.progress < 85) {
                    // Under eaten - Blue
                    bgColor = isSelected ? "bg-blue-500" : "bg-blue-50";
                    borderColor = isSelected ? "border-blue-500" : "border-blue-200";
                    dayTextColor = isSelected ? "text-blue-100" : "text-blue-500";
                    dateTextColor = isSelected ? "text-white" : "text-blue-900";
                    shadowClass = isSelected ? "shadow-[0_8px_16px_-6px_rgba(59,130,246,0.5)]" : "shadow-sm";
                  } else if (day.progress > 115) {
                    // Over eaten - Red
                    bgColor = isSelected ? "bg-red-500" : "bg-red-50";
                    borderColor = isSelected ? "border-red-500" : "border-red-200";
                    dayTextColor = isSelected ? "text-red-100" : "text-red-500";
                    dateTextColor = isSelected ? "text-white" : "text-red-900";
                    shadowClass = isSelected ? "shadow-[0_8px_16px_-6px_rgba(239,68,68,0.5)]" : "shadow-sm";
                  } else {
                    // On Track - Green
                    bgColor = isSelected ? "bg-emerald-500" : "bg-emerald-50";
                    borderColor = isSelected ? "border-emerald-500" : "border-emerald-200";
                    dayTextColor = isSelected ? "text-emerald-100" : "text-emerald-500";
                    dateTextColor = isSelected ? "text-white" : "text-emerald-900";
                    shadowClass = isSelected ? "shadow-[0_8px_16px_-6px_rgba(16,185,129,0.5)]" : "shadow-sm";
                  }
                } else if (isSelected) {
                  // Selected but no progress yet (e.g. today before any meals)
                  bgColor = "bg-slate-800";
                  borderColor = "border-slate-800";
                  dayTextColor = "text-slate-300";
                  dateTextColor = "text-white";
                  shadowClass = "shadow-[0_8px_16px_-6px_rgba(15,23,42,0.5)]";
                }
                
                return (
                  <div key={idx} className="relative w-[52px] h-[90px] shrink-0 flex flex-col items-center justify-center cursor-pointer group">
                    
                    {/* Solid Background Fill */}
                    <div className={`absolute inset-0 rounded-[26px] transition-all duration-300 border ${bgColor} ${borderColor} ${shadowClass}`} />
                    
                    <div className="relative z-10 flex flex-col items-center justify-between h-full py-4">
                      <span className={`text-[10px] font-bold tracking-widest uppercase transition-colors ${dayTextColor}`}>
                        {day.day}
                      </span>
                      <div className={`w-8 h-8 flex items-center justify-center rounded-full font-bold text-[15px] transition-colors ${dateTextColor} ${isSelected && day.progress > 0 ? 'bg-white/20' : ''}`}>
                        {day.date}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Nutrition Summary Section */}
          <div className="flex items-center justify-between mb-4 px-1">
            <h3 className="text-[22px] font-bold text-slate-900 tracking-tight">Summary</h3>
            <button className="text-[15px] font-semibold text-indigo-700 hover:text-indigo-800 transition-colors">Details</button>
          </div>

          {/* Main Calorie Card */}
          <div className="bg-[#f4f5f7] rounded-[32px] p-10 mb-6 flex flex-col items-center justify-center relative shadow-sm border border-slate-200/50">
            <div className="relative w-[280px] h-[150px] flex items-end justify-center overflow-visible">
              
              <svg className="absolute top-0 left-0 w-full h-full overflow-visible" viewBox="0 0 200 100">
                <path d="M 10 100 A 90 90 0 0 1 190 100" fill="none" stroke="#e2e8f0" strokeWidth="18" strokeLinecap="round" />
                <path 
                  d="M 10 100 A 90 90 0 0 1 190 100" 
                  fill="none" stroke="#7c3aed" strokeWidth="18" strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={circumference} 
                  style={{ strokeDashoffset: circumference - (circumference * caloriePercent) / 100 }}
                  className="transition-all duration-1000 ease-out"
                />
              </svg>

              <div className="flex flex-col items-center translate-y-3">
                <Flame className="w-6 h-6 text-orange-500 fill-orange-500 mb-1" />
                <span className="text-[52px] leading-none font-bold text-slate-900 tracking-[-0.04em]">
                  {displayCalories}
                </span>
                <span className="text-slate-500 font-medium mt-2 text-base">kcal</span>
              </div>
            </div>

            <p className="mt-10 text-[15px] text-slate-500 font-medium">
              {descriptions.calories}
            </p>
          </div>

          {/* Granular Macros Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <MacroCard title="Carbs" data={macros.carbs} description={descriptions.carbs} />
            <MacroCard title="Protein" data={macros.protein} description={descriptions.protein} />
            <MacroCard title="Sat Fat" data={macros.satFat} description={descriptions.satFat} isLimit={true} />
          </div>
          
        </div>
      </div>

    </div>
  );
}

// --- Sub-component for individual Macro Cards ---
function MacroCard({ title, data, description, isLimit = false }: { title: string, data: MacroData, description: string, isLimit?: boolean }) {
  const percent = Math.min((data.current / data.target) * 100, 100);
  const activeColor = isLimit && percent > 90 ? 'bg-red-500' : data.colorClass;

  const displayCurrent = Math.round(data.current);
  const displayTarget = Math.round(data.target);

  return (
    <div className="bg-white rounded-[28px] p-6 flex flex-col justify-between shadow-[0_2px_12px_rgba(0,0,0,0.03)] border border-slate-100">
      <div className="flex items-center justify-between mb-5">
        <span className="font-semibold text-slate-900 text-[15px] tracking-tight">{title}</span>
        <MoreHorizontal className="w-5 h-5 text-slate-400 cursor-pointer" />
      </div>

      <div>
        <div className="flex items-baseline gap-1.5 mb-4">
          <span className="font-bold text-slate-900 text-2xl tracking-tight">{displayCurrent}</span>
          <span className="text-slate-500 text-sm font-medium">/ {displayTarget}{data.unit}</span>
        </div>

        <div className={`h-3.5 w-full rounded-full ${data.bgClass} overflow-hidden mb-5`}>
          <div 
            className={`h-full rounded-full transition-all duration-700 ease-out ${activeColor}`} 
            style={{ width: `${percent}%` }}
          />
        </div>

        <p className="text-xs text-slate-400 font-medium truncate">
          {description}
        </p>
      </div>
    </div>
  );
}