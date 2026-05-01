"use client";

import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useRouter } from 'next/navigation';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Checkbox } from "@/components/ui/checkbox";
import { Loader2, ChevronLeft, ChevronRight, User, Target, Calendar, Activity, MapPin, Sparkles, Percent, Zap, Dumbbell } from "lucide-react";
import { toast } from "sonner";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { useAuth } from "app/context/AuthContext"; // (Adjust this path to match your project!)
 // Assuming your AuthContext exports the token!

const formSchema = z.object({
  gender: z.string().min(1, "Please select your gender"),
  weight: z.string().min(1, "Weight is required"),
  height: z.string().min(1, "Height is required"),
  neck: z.string().min(1, "Neck circumference is required"),
  waist: z.string().min(1, "Waist circumference is required"),
  chest: z.string().min(1, "Chest circumference is required"),
  arm: z.string().min(1, "Arm circumference is required"),
  hip: z.string().optional(),
  bodyType: z.string().min(1, "Please select a body shape"),
  primaryGoals: z.array(z.string()).min(1, "Please select at least one goal"), // Selection back
  activityLevel: z.string().min(1, "Please select your daily activity level"),
  experienceLevel: z.string().min(1, "Select your training experience"),
  workoutDays: z.string().min(1, "Select availability"),
  workoutTime: z.string().min(1, "Select preferred time"),
  soreness: z.string().min(1, "Select recovery speed"),
  medicalConditions: z.array(z.string()),
  workoutLocation: z.string().min(1, "Select a location"),
  availableEquipment: z.array(z.string()).optional(),
}).refine((data) => {
  if (data.gender === "female") {
    return !!data.hip && data.hip.length > 0;
  }
  return true;
}, {
  message: "Hip circumference is required for females",
  path: ["hip"],
});

type MultiFormSchema = z.infer<typeof formSchema>;

const genderOptions = [{ id: "male", label: "Male" }, { id: "female", label: "Female" }];
const bodyTypes = [{ id: "ectomorph", label: "Lean / Hard to gain weight" }, { id: "mesomorph", label: "Athletic / Builds muscle easily" }, { id: "endomorph", label: "Stocky / Hard to lose fat" }, { id: "average", label: "Average / Balanced" }];
const activityOptions = [
  { id: "sedentary", label: "Sedentary (Office job, mostly sitting)" }, 
  { id: "light", label: "Lightly Active (Walking, light chores)" }, 
  { id: "moderate", label: "Moderately Active (On feet often)" }, 
  { id: "heavy", label: "Very Active (Heavy manual labor)" }
];
const experienceOptions = [{ id: "beginner", label: "Beginner (0-1 year)" }, { id: "intermediate", label: "Intermediate (1-5 years)" }, { id: "advanced", label: "Advanced (5+ years)" }];
const daysOptions = [{ id: "2", label: "1-2 Days / Week" }, { id: "4", label: "3-4 Days / Week" }, { id: "6", label: "5+ Days / Week" }];
const timeOptions = [{ id: "morning", label: "Morning" }, { id: "afternoon", label: "Afternoon" }, { id: "evening", label: "Evening" }];
const recoveryOptions = [{ id: "fast", label: "Fast (Rarely sore)" }, { id: "average", label: "Average (Sore for a day)" }, { id: "slow", label: "Slow (Sore for days)" }];
const medicalOptions = [{ id: "none", label: "None / Perfectly Healthy" }, { id: "lower_back", label: "Lower Back Pain" }, { id: "joint_pain", label: "Knee / Joint Pain" }, { id: "shoulder", label: "Shoulder Issues" }, { id: "hypertension", label: "High Blood Pressure" }, { id: "asthma", label: "Asthma / Breathing" }];
const locationOptions = [{ id: "home", label: "Home Workout" }, { id: "basic_gym", label: "Basic Gym (Apartment/Hotel)" }, { id: "pro_gym", label: "Professional Gym" }, { id: "outdoor", label: "Outdoor / Park" }];
const homeEquipment = [{ id: "dumbbells", label: "Dumbbells" }, { id: "bands", label: "Resistance Bands" }, { id: "mat", label: "Yoga Mat" }, { id: "pullup", label: "Pull-up Bar" }];
const basicGymEquipment = [{ id: "smith", label: "Smith Machine" }, { id: "cables", label: "Cable Machine" }, { id: "treadmill", label: "Cardio Machines" }, { id: "kettlebells", label: "Kettlebells" }];
const goalOptions = [
  { id: "muscle_gain", label: "Gain Muscle Mass" },
  { id: "fat_loss", label: "Lose Body Fat" },
  { id: "recomposition", label: "Body Recomposition (Both)" },
  { id: "maintenance", label: "Maintain / Performance" }
];
export default function ThinkFitMasterForm() {
  const router = useRouter(); 
  const { user } = useAuth();
  const baseSteps = [
    { title: "Body Assessment", description: "Establish your current baseline metrics", icon: User },
    { title: "Lifestyle", description: "Determine your daily energy expenditure", icon: Target },
    { title: "Experience & Schedule", description: "Map out your week and background", icon: Calendar },
    { title: "Medical Health", description: "Ensure safety and longevity", icon: Activity },
    { title: "Logistics", description: "Where and how you will train", icon: MapPin },
    { title: "Your Protocol", description: "Review your algorithmic journey path", icon: Sparkles },
  ];

  const [currentStep, setCurrentStep] = useState(0);
  const [estimatedBF, setEstimatedBF] = useState<number | null>(null);
  const [isCalculating, setIsCalculating] = useState(false);
  
  const form = useForm<MultiFormSchema>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      gender: "", weight: "", height: "", neck: "", waist: "", chest: "", arm: "", hip: "", bodyType: "",
      activityLevel: "", experienceLevel: "", workoutDays: "", workoutTime: "", soreness: "",
      medicalConditions: [], workoutLocation: "", availableEquipment: [],
    },
    mode: "onChange",
  });

  const isLastStep = currentStep === baseSteps.length - 1;
  const progress = ((currentStep + 1) / baseSteps.length) * 100;
  
  const selectedLocation = form.watch("workoutLocation");
  const selectedGender = form.watch("gender");

  const handleNextButton = async () => {
    let fieldsToValidate: (keyof MultiFormSchema)[] = [];
    if (currentStep === 0) {
      fieldsToValidate = ["gender", "weight", "height", "neck", "waist", "chest", "arm", "bodyType"];
      if (selectedGender === "female") fieldsToValidate.push("hip");
    }
    if (currentStep === 1) fieldsToValidate = ["activityLevel"]; // CHANGED TO ACTIVITY LEVEL
    if (currentStep === 2) fieldsToValidate = ["experienceLevel", "workoutDays", "workoutTime", "soreness"];
    if (currentStep === 3) fieldsToValidate = ["medicalConditions"];
    if (currentStep === 4) fieldsToValidate = ["workoutLocation"];
    
    const isValid = await form.trigger(fieldsToValidate);
    
    if (isValid) {
      if (currentStep === 0) {
        setIsCalculating(true);
        try {
          const values = form.getValues();
          const response = await fetch("http://127.0.0.1:5001/api/calculate_bf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              gender: values.gender, height: values.height, weight: values.weight,
              waist: values.waist, neck: values.neck, chest: values.chest,
              arm: values.arm, hip: values.hip || "0"
            }),
          });
          const data = await response.json();
          if (data.body_fat_percentage) setEstimatedBF(data.body_fat_percentage);
        } catch (error) {
          console.error("Failed to calculate BF%", error);
        } finally {
          setIsCalculating(false);
        }
      }
      setCurrentStep((prev) => prev + 1);
    } else {
      toast.error("Please complete all required fields.");
    }
  };

  const handleBackButton = () => { if (currentStep > 0) setCurrentStep((prev) => prev - 1); };

  // Inside your ThinkFitMasterForm component...

  const handleFinalSubmit = async (values: MultiFormSchema) => {
    // 3. Guard Clause: Make sure they are actually logged in
    if (!user) {
      toast.error("Authentication Error: Please log in again.");
      router.push("/login");
      return;
    }

    toast.success("Profile Sent! Evaluating goals and generating protocol...");

    try {
      const payload = { 
        ...values, 
        userId: user.id, // 🔥 This dynamically attaches the real user's ID!
        estimatedBF: estimatedBF 
      };
      
      const response = await fetch("http://127.0.0.1:5001/api/onboarding", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        // We removed the "Authorization" header because we don't need a token anymore!
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Failed to save profile.");
      
      router.push("/dashboard"); 

    } catch (error) {
      toast.error("Failed to connect to database. Please try again.");
    }
  };

  const CurrentIcon = baseSteps[currentStep].icon;

  const theme = {
    bgMain: { backgroundColor: '#ffffff', color: '#0f172a', borderColor: '#e2e8f0' },
    bgCard: { backgroundColor: '#ffffff', border: '1px solid #cbd5e1', borderRadius: '20px' },
    input: { backgroundColor: '#f8fafc', border: '1px solid #e2e8f0', color: '#0f172a', height: '64px', borderRadius: '12px', fontSize: '18px', padding: '0 20px' },
    label: { color: '#64748b', textTransform: 'uppercase', fontSize: '13px', letterSpacing: '0.05em', marginBottom: '10px', display: 'block', fontWeight: '600' } as React.CSSProperties,
    textMuted: { color: '#64748b' },
  };

  const renderCheckboxGrid = (name: keyof MultiFormSchema, options: {id: string, label: string}[], label: string) => (
    <div className="space-y-4">
      <label style={theme.label}>{label}</label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {options.map((item) => (
          <FormField key={item.id} control={form.control} name={name} render={({ field }) => {
            const isSelected = (field.value as string[])?.includes(item.id);
            return (
              <FormItem style={{ ...theme.bgCard, padding: '20px 24px', cursor: 'pointer', borderColor: isSelected ? '#60a5fa' : '#e2e8f0', backgroundColor: isSelected ? '#eff6ff' : '#ffffff' }} className="flex flex-row items-center space-x-4 space-y-0 hover:shadow-md transition-all group">
                <FormControl>
                  <Checkbox checked={isSelected} onCheckedChange={(checked) => checked ? field.onChange([...(field.value as string[] || []), item.id]) : field.onChange((field.value as string[])?.filter((val) => val !== item.id))} className="scale-150 border-slate-300 data-[state=checked]:bg-blue-600 data-[state=checked]:border-blue-600"/>
                </FormControl>
                <FormLabel className="font-medium text-lg text-slate-800 cursor-pointer w-full !mt-0 group-hover:text-blue-900 transition-colors">{item.label}</FormLabel>
              </FormItem>
            );
          }} />
        ))}
      </div>
      {form.formState.errors[name] && <p className="text-sm text-red-500 font-medium">{form.formState.errors[name]?.message as string}</p>}
    </div>
  );

  const renderRadioGrid = (name: keyof MultiFormSchema, options: {id: string, label: string}[], label: string) => (
    <div className="space-y-4">
      <label style={theme.label}>{label}</label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {options.map((item) => (
          <FormField key={item.id} control={form.control} name={name} render={({ field }) => {
            const isSelected = field.value === item.id;
            return (
              <FormItem onClick={() => field.onChange(item.id)} style={{ ...theme.bgCard, padding: '20px 24px', cursor: 'pointer', borderColor: isSelected ? '#60a5fa' : '#e2e8f0', backgroundColor: isSelected ? '#eff6ff' : '#ffffff' }} className="hover:shadow-md transition-all group">
                <FormLabel className="font-medium text-lg text-slate-800 cursor-pointer w-full !mt-0 flex items-center justify-between group-hover:text-blue-900 transition-colors">
                  {item.label}
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${isSelected ? 'border-blue-600' : 'border-slate-300'}`}>
                    {isSelected && <div className="w-3 h-3 rounded-full bg-blue-600" />}
                  </div>
                </FormLabel>
              </FormItem>
            );
          }} />
        ))}
      </div>
      {form.formState.errors[name] && <p className="text-sm text-red-500 font-medium">{form.formState.errors[name]?.message as string}</p>}
    </div>
  );

  const renderCurrentStepContent = () => {
    switch (currentStep) {
      case 0: 
        return (
          <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4">
            {renderRadioGrid("gender", genderOptions, "Biological Sex (For accurate algorithmic calculations)")}
            <div className="grid grid-cols-2 gap-8">
              <FormField control={form.control} name="weight" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Weight (kg)</FormLabel><FormControl><Input type="number" placeholder="e.g. 75" style={theme.input} className="focus-visible:ring-blue-500 focus-visible:ring-offset-2" {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="height" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Height (cm)</FormLabel><FormControl><Input type="number" placeholder="e.g. 180" style={theme.input} className="focus-visible:ring-blue-500 focus-visible:ring-offset-2" {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="neck" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Neck (cm)</FormLabel><FormControl><Input type="number" placeholder="Below Adam's apple" style={theme.input} className="focus-visible:ring-blue-500 focus-visible:ring-offset-2" {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="waist" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Waist (cm)</FormLabel><FormControl><Input type="number" placeholder="Navel level" style={theme.input} className="focus-visible:ring-blue-500 focus-visible:ring-offset-2" {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="chest" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Chest (cm)</FormLabel><FormControl><Input type="number" placeholder="Widest point" style={theme.input} className="focus-visible:ring-blue-500 focus-visible:ring-offset-2" {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="arm" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Arm (cm)</FormLabel><FormControl><Input type="number" placeholder="Flexed bicep" style={theme.input} className="focus-visible:ring-blue-500 focus-visible:ring-offset-2" {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              {selectedGender === "female" && (
                <div className="col-span-2 animate-in fade-in zoom-in-95 duration-300">
                  <FormField control={form.control} name="hip" render={({ field }) => (
                    <FormItem><FormLabel style={theme.label}>Hip (cm)</FormLabel><FormControl><Input type="number" placeholder="Widest part of glutes" style={theme.input} className="focus-visible:ring-blue-500 focus-visible:ring-offset-2" {...field} /></FormControl><FormMessage /></FormItem>
                  )} />
                </div>
              )}
            </div>
            {renderRadioGrid("bodyType", bodyTypes, "Select Closest Body Type")}
          </div>
        );
        case 1:
          return (
            <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4">
              {/* GOAL SELECTION IS BACK */}
              {renderCheckboxGrid("primaryGoals", goalOptions, "Select Your Primary Objectives")}
              
              <div className="pt-6 border-t border-slate-100">
                {/* ACTIVITY LEVEL REPLACES TEXTBOX */}
                {renderRadioGrid("activityLevel", activityOptions, "Daily Activity Level (Non-Exercise)")}
              </div>
            </div>
          );
      case 2:
        return (
          <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4">
            {renderRadioGrid("experienceLevel", experienceOptions, "Training Experience")}
            {renderRadioGrid("workoutDays", daysOptions, "Workout Availability")}
            {renderRadioGrid("workoutTime", timeOptions, "Preferred Time of Day")}
            {renderRadioGrid("soreness", recoveryOptions, "How long does muscle soreness last?")}
          </div>
        );
      case 3:
        return (
          <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4">
            {renderCheckboxGrid("medicalConditions", medicalOptions, "Select Any Medical Conditions")}
          </div>
        );
      case 4:
        return (
          <div className="space-y-10 animate-in fade-in slide-in-from-bottom-4">
            {renderRadioGrid("workoutLocation", locationOptions, "Where will you train?")}
            {selectedLocation === "home" && <div className="pt-6 border-t border-slate-100 animate-in fade-in">{renderCheckboxGrid("availableEquipment", homeEquipment, "Available Home Equipment")}</div>}
            {selectedLocation === "basic_gym" && <div className="pt-6 border-t border-slate-100 animate-in fade-in">{renderCheckboxGrid("availableEquipment", basicGymEquipment, "Available Gym Machines")}</div>}
            {selectedLocation === "pro_gym" && <div className="p-6 bg-emerald-50 border border-emerald-100 rounded-2xl mt-6 animate-in fade-in"><p className="text-emerald-800 text-base font-semibold">Great! A professional gym gives us access to all standard equipment for maximum optimization.</p></div>}
          </div>
        );
      case 5:
        const bf = estimatedBF || 0;
        const isRecomp = (selectedGender === "male" && bf >= 20) || (selectedGender === "female" && bf >= 30);
        const assignedPhase = isRecomp ? "Body Recomp" : "Building Phase";
        
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
             <div className="text-center mb-8">
               <h3 className="text-3xl font-black text-slate-900 mb-2">Analysis Complete</h3>
               <p className="text-slate-500 text-lg">We have analyzed your metrics to generate your optimal starting block.</p>
             </div>

             <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-slate-900 p-8 rounded-3xl flex flex-col items-center justify-center text-center shadow-xl border border-slate-800">
                  <div className="w-16 h-16 rounded-full bg-slate-800 border-[4px] border-blue-500 flex items-center justify-center mb-4">
                    <Percent className="text-blue-500 w-6 h-6 stroke-[3px]" />
                  </div>
                  <p className="text-slate-400 text-sm font-bold uppercase tracking-widest mb-1">Estimated Baseline</p>
                  <div className="flex items-baseline gap-1">
                    <span className="text-6xl font-black text-white">{estimatedBF || "--"}</span>
                    <span className="text-2xl font-bold text-blue-400">%</span>
                  </div>
                </div>

                <div className={`p-8 rounded-3xl flex flex-col items-center justify-center text-center shadow-lg border-2 ${isRecomp ? 'bg-blue-50 border-blue-200' : 'bg-emerald-50 border-emerald-200'}`}>
                  <div className={`w-16 h-16 rounded-full flex items-center justify-center mb-4 ${isRecomp ? 'bg-blue-100 text-blue-600' : 'bg-emerald-100 text-emerald-600'}`}>
                    {isRecomp ? <Zap className="w-8 h-8" /> : <Dumbbell className="w-8 h-8" />}
                  </div>
                  <p className={`text-sm font-bold uppercase tracking-widest mb-1 ${isRecomp ? 'text-blue-500' : 'text-emerald-500'}`}>Recommended Path</p>
                  <span className={`text-3xl font-black ${isRecomp ? 'text-blue-950' : 'text-emerald-950'}`}>{assignedPhase}</span>
                  <p className={`text-sm font-medium mt-3 ${isRecomp ? 'text-blue-800/70' : 'text-emerald-800/70'}`}>
                    {isRecomp 
                      ? "Focusing on fat loss while leveraging newbie gains to build muscle in a calculated deficit." 
                      : "Focusing on maximizing lean muscle growth in a controlled calorie surplus."}
                  </p>
                </div>
             </div>

             <div className="p-6 bg-slate-50 border border-slate-200 rounded-2xl text-center">
                <p className="text-slate-600 font-medium">Click <strong>Generate Protocol</strong> below to finalize your profile and calculate your daily macro targets.</p>
             </div>
          </div>
        );
      default: return null;
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 py-16 px-4 flex justify-center items-center font-sans text-slate-900">
      <div className="w-full max-w-4xl mx-auto">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleFinalSubmit)}>
            <Card style={{ ...theme.bgMain, borderRadius: '28px', overflow: 'hidden', boxShadow: '0 20px 40px -15px rgba(0,0,0,0.05)' }}>
              <CardHeader style={{ padding: '48px 48px 32px 48px', borderBottom: '1px solid #f1f5f9', background: 'linear-gradient(to bottom, #ffffff, #f8fafc)' }}>
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-5">
                    <div className="p-4 bg-blue-50 rounded-2xl border border-blue-100"><CurrentIcon className="w-8 h-8 text-blue-600"/></div>
                    <div>
                      <CardTitle className="text-3xl font-extrabold text-slate-900 tracking-tight">{baseSteps[currentStep].title}</CardTitle>
                      <CardDescription style={theme.textMuted} className="text-base mt-1">{baseSteps[currentStep].description}</CardDescription>
                    </div>
                  </div>
                  <span className="text-blue-600 font-bold text-sm bg-blue-50 px-5 py-2.5 rounded-full border border-blue-100 tracking-wide">STEP {currentStep+1} / {baseSteps.length}</span>
                </div>
                <div style={{ height: '8px', backgroundColor: '#e2e8f0', marginTop: '32px', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${progress}%`, backgroundColor: '#3b82f6', transition: 'width 0.6s cubic-bezier(0.22, 1, 0.36, 1)' }} />
                </div>
              </CardHeader>
              <div>
                <CardContent style={{ padding: '48px', backgroundColor: '#ffffff', minHeight: '450px' }}>
                  {renderCurrentStepContent()}
                </CardContent>
                <CardFooter style={{ padding: '36px 48px', borderTop: '1px solid #f1f5f9', backgroundColor: '#f8fafc' }}>
                  <div className="flex w-full justify-between items-center">
                    <Button type="button" variant="ghost" onClick={handleBackButton} disabled={currentStep===0} className="text-slate-500 hover:bg-slate-200 hover:text-slate-800 text-base h-12 px-6 rounded-xl font-semibold transition-colors" style={{ visibility: currentStep===0 ? 'hidden' : 'visible' }}>
                      <ChevronLeft className="mr-2 h-5 w-5"/> Back
                    </Button>
                    {!isLastStep ? (
                        <Button type="button" onClick={handleNextButton} disabled={isCalculating} className="bg-blue-600 hover:bg-blue-700 text-white px-10 h-14 text-lg rounded-xl font-bold shadow-md hover:shadow-lg transition-all active:scale-[0.98]">
                          {isCalculating ? <Loader2 className="w-6 h-6 animate-spin" /> : <>Next Step <ChevronRight className="ml-2 h-6 w-6"/></>}
                        </Button>
                    ) : (
                        <Button type="submit" disabled={form.formState.isSubmitting} className="bg-slate-900 hover:bg-black text-white px-10 h-14 text-lg rounded-xl font-bold shadow-md hover:shadow-lg transition-all active:scale-[0.98]">
                            {form.formState.isSubmitting ? <Loader2 className="mr-2 animate-spin"/> : <Sparkles className="mr-2 h-5 w-5" />} Generate Protocol
                        </Button>
                    )}
                  </div>
                </CardFooter>
              </div>
            </Card>
          </form>
        </Form>
      </div>
    </div>
  );
}