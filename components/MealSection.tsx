'use client';

import React, { useState, useRef } from 'react';
import { Camera, ScanBarcode, Plus, Loader2, X, Utensils, ChevronLeft, Search, CheckCircle2 } from 'lucide-react';
import { toast } from 'sonner';
// IMPORT AUTHTOKEN TO PASS TO PYTHON BACKEND
import { useAuth } from "app/context/AuthContext"; 

type MealType = {
  id: string;
  title: string;
  recommendedCal: string;
  imagePos: 'left' | 'right';
  placeholderColor: string; 
  imageUrl: string; 
};

interface SearchResult {
  id: string;
  name: string;
}

export default function MealSection() {
  const { user } = useAuth(); // Grab the user context
  const [isScanning, setIsScanning] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [category, setCategory] = useState("Snack");
  
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  
  const [selectedFood, setSelectedFood] = useState<SearchResult | null>(null);
  const [servingQty, setServingQty] = useState("");
  const [servingUnit, setServingUnit] = useState("grams");
  
  const [isOcrLoading, setIsOcrLoading] = useState(false);
  const [isOcrModalOpen, setIsOcrModalOpen] = useState(false);
  const [detectedNutrition, setDetectedNutrition] = useState<any>(null);
  const [consumptionMode, setConsumptionMode] = useState<'percent' | 'servings'>('servings');
  const [amount, setAmount] = useState("1");
  const packagedFileInputRef = useRef<HTMLInputElement>(null);

  const [isThaliModalOpen, setIsThaliModalOpen] = useState(false);
  const [detectedThaliInfo, setDetectedThaliInfo] = useState<any>(null);

  const meals: MealType[] = [
    { 
      id: 'breakfast', 
      title: 'Breakfast', 
      recommendedCal: '400-550', 
      imagePos: 'right', 
      placeholderColor: 'bg-emerald-100/50',
      imageUrl: 'https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?auto=format&fit=crop&q=80&w=400' 
    },
    { 
      id: 'lunch', 
      title: 'Lunch', 
      recommendedCal: '600-750', 
      imagePos: 'left', 
      placeholderColor: 'bg-orange-100/50',
      imageUrl: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&q=80&w=400'
    },
    { 
      id: 'snack', 
      title: 'Snack', 
      recommendedCal: '150-250', 
      imagePos: 'right', 
      placeholderColor: 'bg-amber-100/50',
      imageUrl: 'https://images.unsplash.com/photo-1772766115216-adec7b88d399?auto=format&fit=crop&q=80&w=400'
    },
    { 
      id: 'dinner', 
      title: 'Dinner', 
      recommendedCal: '500-650', 
      imagePos: 'left', 
      placeholderColor: 'bg-blue-100/50',
      imageUrl: 'https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&q=80&w=400'
    },
  ];

  const openManualModal = (categoryTitle?: string) => {
    setCategory(categoryTitle || "Snack");
    setIsModalOpen(true);
    setSearchQuery("");
    setSearchResults([]);
    setSelectedFood(null);
    setServingQty("");
  };

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    if (query.trim().length > 1) {
      try {
        const res = await fetch(`http://127.0.0.1:5001/api/food/search?q=${encodeURIComponent(query)}`);
        if (res.ok) {
          const data = await res.json();
          setSearchResults(data);
        }
      } catch (error) { console.error(error); }
    } else {
      setSearchResults([]);
    }
  };

  // 1. FIXED MANUAL SUBMIT
  const handleManualSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFood || !servingQty) return;
    if (!user) { toast.error("Please log in first."); return; }

    let weight_g = parseFloat(servingQty);
    if (servingUnit === "bowls") weight_g = weight_g * 150; 
    if (servingUnit === "pieces") weight_g = weight_g * 50;  

    const payload = { 
      thinkfit_session: user, // Tells Python whose DB row to update
      scanned_items: [{ food_id: selectedFood.id, weight_g: weight_g }] 
    };

    try {
      const response = await fetch('http://127.0.0.1:5001/api/scan/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!response.ok) throw new Error("Failed to log");
      toast.success(`${selectedFood.name} added!`);
      setIsModalOpen(false);
      window.location.reload(); 
    } catch (error) { toast.error("Failed to save."); }
  };

  // 2. FIXED PACKAGED UPLOAD (OCR)
  const handlePackagedUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
  
    setIsOcrLoading(true);
    const formData = new FormData();
    formData.append('image', file);
  
    try {
      const res = await fetch('http://127.0.0.1:5001/api/scan/packaged', { method: 'POST', body: formData });
      const data = await res.json();
      if (data.success) {
        setDetectedNutrition(data.nutrition);
        setIsOcrModalOpen(true);
      } else {
        toast.error("Could not read label. Use a clearer photo.");
      }
    } catch (e) {
      toast.error("OCR Server Error.");
    } finally {
      setIsOcrLoading(false);
      if (packagedFileInputRef.current) packagedFileInputRef.current.value = '';
    }
  };
  
  // 3. FIXED OCR FINAL SUBMIT
  const submitOcrFinal = async () => {
    if (!user) { toast.error("Please log in first."); return; }
    const factor = consumptionMode === 'percent' ? parseFloat(amount) / 100 : parseFloat(amount);
    
    const payload = {
      thinkfit_session: user, // Tells Python whose DB row to update
      calories: (detectedNutrition.calories || 0) * factor,
      protein: (detectedNutrition.protein || 0) * factor,
      carbs: (detectedNutrition.carbs || 0) * factor,
      fat: (detectedNutrition.fat || 0) * factor,
    };
  
    try {
      await fetch('http://127.0.0.1:5001/api/manual/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      toast.success("Nutrition added!");
      setIsOcrModalOpen(false);
      window.location.reload();
    } catch (e) {
      toast.error("Failed to log.");
    }
  };

  const handleThaliUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setIsScanning(true);
    const loadingToast = toast.loading("AI is analyzing your plate...");

    try {
      const formData = new FormData();
      formData.append('image', file);

      // ⚠️ UPDATE THIS NGROK URL WITH YOUR ACTIVE ONE
      const colabUrl = 'https://trout-happiest-antennae.ngrok-free.dev/api/scan/thali';
      
      const colabRes = await fetch(colabUrl, {
        method: 'POST',
        body: formData
      });

      if (!colabRes.ok) throw new Error("Failed to connect to Colab API.");

      const colabData = await colabRes.json();
      if (!colabData.success) throw new Error(colabData.error || "AI could not identify food.");

      setDetectedThaliInfo(colabData);
      setIsThaliModalOpen(true);
      toast.dismiss(loadingToast);

    } catch (error: any) {
      toast.error(error.message || "An error occurred.", { id: loadingToast });
    } finally {
      setIsScanning(false);
      if (fileInputRef.current) fileInputRef.current.value = '';
    }
  };

  // 4. FIXED THALI FINAL SUBMIT
  const handleThaliConfirmAndSave = async () => {
    if (!detectedThaliInfo) return;
    if (!user) { toast.error("Please log in first."); return; }
    
    const loadingToast = toast.loading("Saving nutrition to your daily log...");

    try {
      const payload = {
        thinkfit_session: user, // Tells Python whose DB row to update
        scanned_items: detectedThaliInfo.scanned_items
      };

      const localRes = await fetch('http://127.0.0.1:5001/api/scan/log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload), 
      });

      if (!localRes.ok) throw new Error("Failed to save to local database.");

      toast.success(`Added ${detectedThaliInfo.totals.calories} kcal to your daily log!`, { id: loadingToast });
      setIsThaliModalOpen(false);
      setDetectedThaliInfo(null);
      
      setTimeout(() => window.location.reload(), 800);
    } catch (error: any) {
      toast.error(error.message || "Failed to save.", { id: loadingToast });
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto p-8 md:p-12 font-sans relative">
      <input type="file" accept="image/*" className="hidden" ref={fileInputRef} onChange={handleThaliUpload} />
      <input type="file" accept="image/*" className="hidden" ref={packagedFileInputRef} onChange={handlePackagedUpload} />

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-6 mb-12">
        <button onClick={() => fileInputRef.current?.click()} className="group relative flex flex-col items-center justify-center gap-4 bg-white aspect-square rounded-[32px] p-6 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.04)] border border-slate-100/80 hover:shadow-[0_8px_30px_-4px_rgba(0,0,0,0.08)] transition-all" disabled={isScanning}>
          <div className="w-16 h-16 rounded-2xl bg-indigo-50 flex items-center justify-center">
            {isScanning ? <Loader2 className="w-8 h-8 text-indigo-600 animate-spin" /> : <Camera className="w-8 h-8 text-indigo-600" />}
          </div>
          <span className="font-semibold text-slate-800 text-lg tracking-tight">
            {isScanning ? 'Analyzing...' : 'Click Photo'}
          </span>
        </button>

        <button 
          onClick={() => packagedFileInputRef.current?.click()}
          className="group relative flex flex-col items-center justify-center gap-4 bg-white aspect-square rounded-[32px] p-6 shadow-sm border border-slate-100 hover:shadow-md transition-all"
        >
          <div className="w-16 h-16 rounded-2xl bg-violet-50 flex items-center justify-center">
            {isOcrLoading ? <Loader2 className="w-8 h-8 text-violet-600 animate-spin" /> : <ScanBarcode className="w-8 h-8 text-violet-600" />}
          </div>
          <span className="font-semibold text-slate-800 text-lg tracking-tight">Scan Label</span>
        </button>
      </div>

      <h3 className="text-[22px] font-bold text-slate-900 mb-8">Today's Meals</h3>
      <div className="flex flex-col gap-6">
        {meals.map((meal) => (
          <MealCard key={meal.id} meal={meal} onAdd={() => openManualModal(meal.title)} />
        ))}
      </div>

      {/* THALI CONFIRMATION MODAL */}
      {isThaliModalOpen && detectedThaliInfo && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white rounded-[32px] shadow-2xl w-full max-w-md max-h-[90vh] flex flex-col overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="px-8 py-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
              <h3 className="text-xl font-bold text-slate-800">Review Your Meal</h3>
              <button onClick={() => { setIsThaliModalOpen(false); setDetectedThaliInfo(null); }}><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            <div className="flex-1 overflow-y-auto p-8">
              {/* Summary Header */}
              <div className="bg-indigo-50/50 rounded-2xl p-6 mb-8 text-center border border-indigo-100">
                <p className="text-sm font-bold text-indigo-500 uppercase tracking-wider mb-2">Total Estimated</p>
                <div className="flex items-baseline justify-center gap-1">
                  <span className="text-4xl font-black text-indigo-950">{detectedThaliInfo.totals.calories}</span>
                  <span className="text-lg font-bold text-indigo-600/80">kcal</span>
                </div>
                <div className="flex justify-center gap-4 mt-4 text-sm font-semibold text-slate-600">
                <span>🥩 {Math.round(detectedThaliInfo.totals.protein_g)}g Protein</span>
                <span>🍞 {Math.round(detectedThaliInfo.totals.carbs_g)}g Carb</span>
                <span>🧈 {Math.round(detectedThaliInfo.totals.fat_g)}g Fat</span>
                </div>
              </div>

              {/* Items List */}
              <h4 className="text-sm font-bold text-slate-400 uppercase tracking-wider mb-4">Detected Items</h4>
              <div className="space-y-3 mb-8">
                {detectedThaliInfo.scanned_items.map((item: any, i: number) => (
                  <div key={i} className="flex justify-between items-center p-4 rounded-xl border border-slate-100 bg-white shadow-sm">
                    <div>
                      <p className="font-bold text-slate-800 capitalize">{item.food_id.replace(/-/g, ' ')}</p>
                      <p className="text-sm text-slate-500 font-medium">{item.weight_g}g</p>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-indigo-600">{item.calories} kcal</p>
                    </div>
                  </div>
                ))}
              </div>

              <button onClick={handleThaliConfirmAndSave} className="w-full flex items-center justify-center gap-2 py-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-2xl shadow-lg transition-colors">
                <CheckCircle2 className="w-5 h-5" /> Confirm & Log Meal
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Manual Search Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white rounded-[32px] shadow-2xl w-full max-w-md max-h-[95vh] flex flex-col overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="px-8 py-6 border-b border-slate-100 flex justify-between items-center bg-white shrink-0">
              <div className="flex items-center gap-3">
                {selectedFood ? <button onClick={() => setSelectedFood(null)}><ChevronLeft className="w-5 h-5 text-slate-400" /></button> : <Utensils className="w-5 h-5 text-indigo-500" />}
                <h3 className="text-xl font-bold text-slate-800">{selectedFood ? "Add Serving" : "Log Meal"}</h3>
              </div>
              <button onClick={() => setIsModalOpen(false)}><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            <div className="flex-1 overflow-y-auto">
              {!selectedFood ? (
                <div className="p-8 space-y-6">
                  <div className="relative">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                    <input 
                      type="text" 
                      value={searchQuery}
                      onChange={(e) => handleSearch(e.target.value)}
                      className="w-full bg-slate-50 border border-slate-200 rounded-2xl pl-12 pr-5 py-4 focus:ring-2 focus:ring-indigo-500/20 outline-none" 
                      placeholder="Search Indian database..." 
                      autoFocus
                    />
                  </div>

                  <div className="space-y-2">
                    {searchResults.map((food) => (
                      <button 
                        key={food.id}
                        onClick={() => setSelectedFood(food)}
                        className="w-full flex items-center justify-between p-4 bg-white border border-slate-100 rounded-2xl hover:bg-indigo-50/30 text-left"
                      >
                        <span className="font-bold text-slate-700">{food.name}</span>
                        <Plus className="w-4 h-4 text-indigo-500" />
                      </button>
                    ))}
                  </div>
                </div>
              ) : (
                <form onSubmit={handleManualSubmit} className="p-8 space-y-8">
                  <div>
                    <h4 className="text-2xl font-bold text-slate-900">{selectedFood.name}</h4>
                    <p className="text-slate-500 text-sm mt-1">Logged as {category}</p>
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-[11px] font-bold text-slate-400 uppercase">Quantity</label>
                      <input required type="number" step="0.5" value={servingQty} onChange={(e) => setServingQty(e.target.value)} className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 text-lg font-bold" />
                    </div>
                    <div className="space-y-2">
                      <label className="text-[11px] font-bold text-slate-400 uppercase">Unit</label>
                      <select value={servingUnit} onChange={(e) => setServingUnit(e.target.value)} className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 font-medium outline-none">
                        <option value="grams">Grams</option>
                        <option value="bowls">Bowls</option>
                        <option value="pieces">Pieces</option>
                      </select>
                    </div>
                  </div>

                  <button type="submit" className="w-full py-4 bg-[#6366f1] text-white font-bold rounded-2xl shadow-lg">Add to Daily Log</button>
                </form>
              )}
            </div>
          </div>
        </div>
      )}

      {/* OCR Modal */}
      {isOcrModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm">
          <div className="bg-white rounded-[32px] shadow-2xl w-full max-w-md overflow-hidden animate-in zoom-in-95">
            <div className="px-8 py-6 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
              <h3 className="text-xl font-bold text-slate-800">Confirm Macros</h3>
              <button onClick={() => setIsOcrModalOpen(false)}><X className="w-5 h-5 text-slate-400" /></button>
            </div>

            <div className="p-8 space-y-6">
              <div className="grid grid-cols-2 gap-3">
                {Object.entries(detectedNutrition || {}).map(([key, val]: any) => (
                  <div key={key} className="bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <p className="text-[10px] font-bold text-slate-400 uppercase">{key}</p>
                    <p className="text-lg font-bold text-slate-700">{val}g</p>
                  </div>
                ))}
              </div>

              <div className="pt-4 border-t border-slate-100">
                <div className="flex gap-2 mb-4">
                  <button onClick={() => setConsumptionMode('servings')} className={`flex-1 py-2 rounded-lg text-xs font-bold ${consumptionMode === 'servings' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-500'}`}>Servings</button>
                  <button onClick={() => setConsumptionMode('percent')} className={`flex-1 py-2 rounded-lg text-xs font-bold ${consumptionMode === 'percent' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-500'}`}>% of Pack</button>
                </div>
                <input type="number" value={amount} onChange={(e) => setAmount(e.target.value)} className="w-full bg-slate-50 border border-slate-200 rounded-2xl px-5 py-4 font-bold text-xl outline-none" />
              </div>

              <button onClick={submitOcrFinal} className="w-full py-4 bg-indigo-600 text-white font-bold rounded-2xl shadow-lg">Apply to Daily Log</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function MealCard({ meal, onAdd }: { meal: MealType, onAdd: () => void }) {
  const isRight = meal.imagePos === 'right';

  return (
    <div className="relative bg-white rounded-[32px] h-[160px] flex items-center overflow-hidden shadow-[0_4px_20px_-4px_rgba(0,0,0,0.03)] border border-slate-100/80 group">
      
      <div 
        className={`absolute top-1/2 -translate-y-1/2 w-48 h-48 rounded-full ${meal.placeholderColor} flex items-center justify-center overflow-hidden
          ${isRight ? '-right-12' : '-left-12'}
        `}
      >
        <img 
          src={meal.imageUrl} 
          alt={meal.title} 
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" 
        />
      </div>

      <div className={`relative z-10 flex flex-col justify-center h-full w-full px-10 ${isRight ? 'items-start' : 'items-end'}`}>
        <div className={`flex flex-col ${isRight ? 'text-left' : 'text-right'}`}>
          <h4 className="text-[22px] font-bold text-slate-900 tracking-tight mb-1">{meal.title}</h4>
          <p className="text-[13px] font-medium text-slate-400 mb-5">Recommended {meal.recommendedCal} Cal</p>
        </div>

        <button onClick={onAdd} className="flex items-center gap-1.5 bg-[#6366f1] text-white px-6 py-2.5 rounded-2xl font-semibold text-[15px] shadow-md transition-transform active:scale-95">
          <Plus className="w-4 h-4" /> Add
        </button>
      </div>
    </div>
  );
}