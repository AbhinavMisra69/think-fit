"use client";

import React, { useState, useEffect } from "react";
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area 
} from 'recharts';
import { Activity, ArrowUpRight, ArrowDownRight, Scale, Dumbbell, Target, Loader2 } from "lucide-react";
import { toast } from "sonner";

interface MeasurementLog {
  log_date: string;
  weight_kg: number;
  body_fat_pct: number;
  waist_cm: number;
  chest_cm: number;
  arm_cm: number;
  thigh_cm: number;
  lean_mass?: number; 
  short_date?: string;
}

// Temporary Mock Data for Strength UI until we build the workout backend
const mockStrengthHistory = [
  { short_date: "1 Apr", bench: 80, squat: 100, deadlift: 120, ohp: 50 },
  { short_date: "8 Apr", bench: 82.5, squat: 105, deadlift: 125, ohp: 52.5 },
  { short_date: "15 Apr", bench: 85, squat: 107.5, deadlift: 130, ohp: 52.5 },
  { short_date: "22 Apr", bench: 87.5, squat: 112.5, deadlift: 135, ohp: 55 },
];

export default function ProgressDashboard() {
  const [history, setHistory] = useState<MeasurementLog[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const [formData, setFormData] = useState({
    weight: "", waist: "", chest: "", arm: "", thigh: ""
  });

  const fetchHistory = async () => {
    try {
      const res = await fetch("/api/progress");
      if (!res.ok) throw new Error("Failed to fetch");
      const data = await res.json();
      
      const processedHistory = data.history.map((entry: MeasurementLog) => ({
        ...entry,
        lean_mass: Number((entry.weight_kg * (1 - (entry.body_fat_pct / 100))).toFixed(1)),
        short_date: new Date(entry.log_date).toLocaleDateString('en-GB', { month: 'short', day: 'numeric' })
      }));
      
      setHistory(processedHistory);
    } catch (error) {
      console.error("Failed to fetch history", error);
      toast.error("Failed to load dashboard data.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleUpdateProgress = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    const payload = {
      weight: parseFloat(formData.weight),
      waist: parseFloat(formData.waist),
      chest: parseFloat(formData.chest),
      arm: parseFloat(formData.arm),
      thigh: parseFloat(formData.thigh),
    };

    try {
      const res = await fetch("/api/progress/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Update failed on server");
      }
      
      toast.success("Progress logged! ML Engine updated your Body Fat %.");
      setFormData({ weight: "", waist: "", chest: "", arm: "", thigh: "" }); 
      fetchHistory(); 
    } catch (error: any) {
      toast.error(`Save failed: ${error.message}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#f8fafc]">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
          <p className="text-slate-500 font-medium animate-pulse">Loading Analytics Engine...</p>
        </div>
      </div>
    );
  }

  const latest = history[history.length - 1] || null;
  const previous = history.length > 1 ? history[history.length - 2] : null;

  const getTrend = (current: number, past: number) => {
    const diff = current - past;
    return diff > 0 ? `+${diff.toFixed(1)}` : diff.toFixed(1);
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] p-6 md:p-12 font-sans text-slate-900">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-slate-900">Physique Analytics</h1>
          <p className="text-slate-500 mt-1">Track your body recomposition and strength metrics over time.</p>
        </div>

        {/* --- 1. FULL WIDTH UPDATE CARD --- */}
        <div className="bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-slate-200/60">
          <div className="flex items-center gap-3 mb-6">
            <Target className="w-6 h-6 text-indigo-500" />
            <h2 className="text-xl font-bold">Log New Measurements</h2>
          </div>
          
          <form onSubmit={handleUpdateProgress} className="flex flex-wrap md:flex-nowrap gap-4 items-end">
            <div className="flex-1 min-w-[120px]">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Weight (kg)</label>
              <input required type="number" step="0.1" value={formData.weight} onChange={(e) => setFormData({...formData, weight: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="0.0" />
            </div>
            <div className="flex-1 min-w-[120px]">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Waist (cm)</label>
              <input required type="number" step="0.1" value={formData.waist} onChange={(e) => setFormData({...formData, waist: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="0.0" />
            </div>
            <div className="flex-1 min-w-[120px]">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Chest (cm)</label>
              <input required type="number" step="0.1" value={formData.chest} onChange={(e) => setFormData({...formData, chest: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="0.0" />
            </div>
            <div className="flex-1 min-w-[120px]">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Arm (cm)</label>
              <input required type="number" step="0.1" value={formData.arm} onChange={(e) => setFormData({...formData, arm: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="0.0" />
            </div>
            <div className="flex-1 min-w-[120px]">
              <label className="block text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Thigh (cm)</label>
              <input required type="number" step="0.1" value={formData.thigh} onChange={(e) => setFormData({...formData, thigh: e.target.value})} className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500" placeholder="0.0" />
            </div>
            
            <button type="submit" disabled={isSubmitting} className="w-full md:w-auto px-8 py-3 bg-slate-900 hover:bg-slate-800 text-white font-semibold rounded-xl transition-colors flex items-center justify-center">
              {isSubmitting ? <Loader2 className="w-5 h-5 animate-spin" /> : "Save Metrics"}
            </button>
          </form>
        </div>

        {/* --- 2. SUMMARY METRICS --- */}
        {latest && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
             <MetricCard 
                title="Current Weight" value={`${latest.weight_kg} kg`} icon={Scale} 
                trend={previous ? `${getTrend(latest.weight_kg, previous.weight_kg)}kg` : null} 
                isGood={previous ? latest.weight_kg < previous.weight_kg : true} 
              />
             <MetricCard 
                title="Body Fat (ML Est.)" value={`${latest.body_fat_pct}%`} icon={Activity} 
                trend={previous ? `${getTrend(latest.body_fat_pct, previous.body_fat_pct)}%` : null} 
                isGood={previous ? latest.body_fat_pct < previous.body_fat_pct : true} 
              />
             <MetricCard 
                title="Lean Muscle Mass" value={`${latest.lean_mass} kg`} icon={Dumbbell} 
                trend={previous && latest.lean_mass && previous.lean_mass ? `${getTrend(latest.lean_mass, previous.lean_mass)}kg` : null} 
                isGood={previous && latest.lean_mass && previous.lean_mass ? latest.lean_mass >= previous.lean_mass : true} 
              />
             <MetricCard 
                title="Relative Strength" value={`1.8x BW`} icon={ArrowUpRight} subtitle="Est. from workouts" 
              />
          </div>
        )}

        {/* --- 3. DUAL HERO CHARTS --- */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-slate-200/60">
            <div className="mb-6">
              <h2 className="text-xl font-bold text-slate-900">Composition Timeline</h2>
              <p className="text-sm text-slate-500">Total Weight vs. Lean Mass (kg)</p>
            </div>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={history} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorWeight" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#f43f5e" stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="colorMuscle" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="short_date" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} dy={10} />
                  <YAxis domain={['dataMin - 5', 'auto']} axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                  <Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }} labelStyle={{ fontWeight: 'bold', color: '#1e293b', marginBottom: '4px' }} />
                  <Area type="monotone" name="Total Weight" dataKey="weight_kg" stroke="#f43f5e" strokeWidth={3} fillOpacity={1} fill="url(#colorWeight)" />
                  <Area type="monotone" name="Lean Mass" dataKey="lean_mass" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorMuscle)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="bg-white rounded-3xl p-6 md:p-8 shadow-sm border border-slate-200/60">
            <div className="mb-6">
              <h2 className="text-xl font-bold text-slate-900">Body Fat Percentage</h2>
              <p className="text-sm text-slate-500">ML Engine Estimations over time</p>
            </div>
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={history} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorBF" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                  <XAxis dataKey="short_date" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} dy={10} />
                  <YAxis domain={['dataMin - 1', 'auto']} axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12}} />
                  <Tooltip contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.08)' }} labelStyle={{ fontWeight: 'bold', color: '#1e293b', marginBottom: '4px' }} />
                  <Area type="monotone" name="Body Fat %" dataKey="body_fat_pct" stroke="#8b5cf6" strokeWidth={3} fillOpacity={1} fill="url(#colorBF)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* --- 4. TAPE MEASUREMENT GRAPHS (Magnified with Gradients) --- */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 mb-4 px-1">Body Circumference</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <MiniChart title="Waist (cm)" dataKey="waist_cm" color="#10b981" data={history} />
            <MiniChart title="Chest (cm)" dataKey="chest_cm" color="#f59e0b" data={history} />
            <MiniChart title="Arm (cm)" dataKey="arm_cm" color="#ef4444" data={history} />
            <MiniChart title="Thigh (cm)" dataKey="thigh_cm" color="#0ea5e9" data={history} />
          </div>
        </div>

        {/* --- 5. STRENGTH GRAPHS (Lines with Dots) --- */}
        <div>
          <h2 className="text-lg font-bold text-slate-900 mb-4 px-1 mt-4">Estimated 1RM Strength Progression</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StrengthChart title="Bench Press (kg)" dataKey="bench" color="#3b82f6" data={mockStrengthHistory} />
            <StrengthChart title="Squat (kg)" dataKey="squat" color="#8b5cf6" data={mockStrengthHistory} />
            <StrengthChart title="Deadlift (kg)" dataKey="deadlift" color="#ec4899" data={mockStrengthHistory} />
            <StrengthChart title="Overhead Press (kg)" dataKey="ohp" color="#f97316" data={mockStrengthHistory} />
          </div>
        </div>

      </div>
    </div>
  );
}

// --- Sub-components ---

function MetricCard({ title, value, icon: Icon, trend, isGood, subtitle }: any) {
  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200/60 shadow-sm flex flex-col justify-between">
      <div className="flex justify-between items-start mb-4">
        <span className="text-sm font-semibold text-slate-500">{title}</span>
        <div className="p-2 bg-slate-50 rounded-lg"><Icon className="w-5 h-5 text-slate-600" /></div>
      </div>
      <div className="flex items-end justify-between">
        <span className="text-2xl font-bold text-slate-900">{value}</span>
        {trend && (
          <span className={`text-xs font-bold px-2 py-1 rounded-full flex items-center ${isGood ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}`}>
            {isGood ? <ArrowDownRight className="w-3 h-3 mr-1" /> : <ArrowUpRight className="w-3 h-3 mr-1" />}
            {trend}
          </span>
        )}
        {subtitle && <span className="text-xs font-medium text-slate-400 mt-1">{subtitle}</span>}
      </div>
    </div>
  );
}

function MiniChart({ title, dataKey, color, data }: any) {
  const gradientId = `gradient-${dataKey}`;
  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200/60 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-600 mb-4">{title}</h3>
      <div className="h-[120px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={color} stopOpacity={0.4}/>
                <stop offset="95%" stopColor={color} stopOpacity={0}/>
              </linearGradient>
            </defs>
            {/* Magnification Fix: YAxis domain zooms in closely on the data variation */}
            <YAxis domain={['dataMin - 1', 'dataMax + 1']} hide />
            <Area 
              type="monotone" 
              dataKey={dataKey} 
              stroke={color} 
              strokeWidth={3} 
              fillOpacity={1} 
              fill={`url(#${gradientId})`} 
            />
            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.05)', padding: '4px 8px' }}
              itemStyle={{ color: color, fontWeight: 'bold' }}
              labelStyle={{ display: 'none' }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function StrengthChart({ title, dataKey, color, data }: any) {
  return (
    <div className="bg-white p-5 rounded-2xl border border-slate-200/60 shadow-sm">
      <h3 className="text-sm font-semibold text-slate-600 mb-4">{title}</h3>
      <div className="h-[120px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            {/* Magnification applied here as well */}
            <YAxis domain={['dataMin - 5', 'dataMax + 5']} hide />
            <Line 
              type="monotone" 
              dataKey={dataKey} 
              stroke={color} 
              strokeWidth={3} 
              dot={{ r: 4, strokeWidth: 2, fill: '#fff' }} 
              activeDot={{ r: 6, strokeWidth: 0 }}
            />
            <Tooltip 
              contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.05)', padding: '4px 8px' }}
              itemStyle={{ color: color, fontWeight: 'bold' }}
              labelStyle={{ display: 'none' }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}