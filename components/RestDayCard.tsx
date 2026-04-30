'use client';

import React from 'react';
import { BatteryCharging, ArrowRightLeft, Plus, Leaf } from 'lucide-react';

export default function RestDayCard() {
  return (
    <div className="w-full relative overflow-hidden bg-white border border-emerald-100 rounded-3xl shadow-sm font-sans mt-2">
      
      {/* Soft decorative background glow */}
      <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-emerald-50/80 to-transparent pointer-events-none" />

      <div className="relative p-8 md:p-10 flex flex-col items-center text-center z-10">
        
        {/* Serene Icon Array */}
        <div className="relative mb-6">
          <div className="w-20 h-20 bg-emerald-100/70 backdrop-blur-sm rounded-full flex items-center justify-center shadow-inner">
            <BatteryCharging className="w-10 h-10 text-emerald-600" />
          </div>
          {/* Small decorative leaf */}
          <div className="absolute -bottom-1 -right-1 bg-white p-1.5 rounded-full shadow-sm border border-emerald-50">
            <Leaf className="w-4 h-4 text-emerald-400" />
          </div>
        </div>

        {/* Text Content */}
        <h3 className="text-2xl md:text-3xl font-bold text-emerald-950 mb-3 tracking-tight">
          Active Recovery
        </h3>
        <p className="text-emerald-700/80 max-w-md mb-10 leading-relaxed text-base md:text-lg">
          Growth happens outside the gym. Take today to stretch, hydrate, and let your muscles repair. You've earned the rest.
        </p>
        
        {/* Action Buttons */}
        <div className="w-full max-w-md flex flex-col sm:flex-row gap-4 mt-auto">
          
          <button className="flex-1 py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 font-semibold text-emerald-700 bg-white border-2 border-emerald-100 hover:border-emerald-200 hover:bg-emerald-50 transition-all duration-200 shadow-sm active:scale-[0.98]">
            <ArrowRightLeft className="w-5 h-5 opacity-80" />
            Shift Workout
          </button>
          
          <button className="flex-1 py-3.5 px-4 rounded-xl flex items-center justify-center gap-2 font-semibold text-white bg-emerald-600 hover:bg-emerald-700 transition-all duration-200 shadow-sm shadow-emerald-200 active:scale-[0.98]">
            <Plus className="w-5 h-5" />
            Additional Workout
          </button>

        </div>
      </div>
    </div>
  );
}