"use client";

import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useRouter } from 'next/navigation'; // Added for redirecting to dashboard
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Checkbox } from "@/components/ui/checkbox";
import { Loader2, ChevronLeft, ChevronRight, User, Target, Calendar, Activity, MapPin, Sparkles } from "lucide-react";
import { toast } from "sonner";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";

// 1. Master Zod Schema (Updated with Circumference Measurements)
const formSchema = z.object({
  // Step 1: Body & Measurements
  weight: z.string().min(1, "Weight is required"),
  height: z.string().min(1, "Height is required"),
  waist: z.string().min(1, "Waist is required"),
  chest: z.string().min(1, "Chest is required"),
  arm: z.string().min(1, "Arm is required"),
  thigh: z.string().min(1, "Thigh is required"),
  bodyType: z.string().min(1, "Please select a body shape"),
  
  // Step 2: Goals
  primaryGoals: z.array(z.string()),
  customGoal: z.string().optional(),
  
  // Step 3: Schedule & Recovery
  workoutDays: z.string().min(1, "Select availability"),
  workoutTime: z.string().min(1, "Select preferred time"),
  soreness: z.string().min(1, "Select recovery speed"),
  
  // Step 4: Medical
  medicalConditions: z.array(z.string()),
  
  // Step 5: Location & Equipment
  workoutLocation: z.string().min(1, "Select a location"),
  availableEquipment: z.array(z.string()).optional(),
}).refine((data) => data.primaryGoals.length > 0 || !!data.customGoal, {
  message: "Please select a goal or write a custom one",
  path: ["primaryGoals"],
});

type MultiFormSchema = z.infer<typeof formSchema>;

// 2. Data Arrays
const bodyTypes = [
  { id: "ectomorph", label: "Lean / Hard to gain weight" },
  { id: "mesomorph", label: "Athletic / Builds muscle easily" },
  { id: "endomorph", label: "Stocky / Hard to lose fat" },
  { id: "average", label: "Average / Balanced" },
];

const goalOptions = [
  { id: "muscle_gain", label: "Gain Muscle Mass" },
  { id: "fat_loss", label: "Lose Body Fat" },
  { id: "endurance", label: "Improve Stamina" },
  { id: "maintenance", label: "Maintain Current Weight" },
];

const daysOptions = [
  { id: "2_days", label: "1-2 Days / Week" },
  { id: "3_4_days", label: "3-4 Days / Week" },
  { id: "5_plus", label: "5+ Days / Week" },
];

const timeOptions = [
  { id: "morning", label: "Morning" },
  { id: "afternoon", label: "Afternoon" },
  { id: "evening", label: "Evening" },
];

const recoveryOptions = [
  { id: "fast", label: "Fast (Rarely sore)" },
  { id: "average", label: "Average (Sore for a day)" },
  { id: "slow", label: "Slow (Sore for days)" },
];

const medicalOptions = [
  { id: "none", label: "None / Perfectly Healthy" },
  { id: "lower_back", label: "Lower Back Pain" },
  { id: "joint_pain", label: "Knee / Joint Pain" },
  { id: "shoulder", label: "Shoulder Issues" },
  { id: "hypertension", label: "High Blood Pressure" },
  { id: "asthma", label: "Asthma / Breathing" },
];

const locationOptions = [
  { id: "home", label: "Home Workout" },
  { id: "basic_gym", label: "Basic Gym (Apartment/Hotel)" },
  { id: "pro_gym", label: "Professional Gym" },
  { id: "outdoor", label: "Outdoor / Park" },
];

const homeEquipment = [
  { id: "dumbbells", label: "Dumbbells" },
  { id: "bands", label: "Resistance Bands" },
  { id: "mat", label: "Yoga Mat" },
  { id: "pullup", label: "Pull-up Bar" },
];

const basicGymEquipment = [
  { id: "smith", label: "Smith Machine" },
  { id: "cables", label: "Cable Machine" },
  { id: "treadmill", label: "Cardio Machines" },
  { id: "kettlebells", label: "Kettlebells" },
];

export default function ThinkFitMasterForm() {
  const router = useRouter(); // Initialize router for redirect
  const baseSteps = [
    { title: "Body Assessment", description: "Establish your current baseline metrics", icon: User },
    { title: "Objective Selection", description: "Set your targets", icon: Target },
    { title: "Schedule & Recovery", description: "Map out your week", icon: Calendar },
    { title: "Medical Health", description: "Ensure safety and longevity", icon: Activity },
    { title: "Logistics", description: "Where and how you will train", icon: MapPin },
  ];

  const [currentStep, setCurrentStep] = useState(0);
  
  const form = useForm<MultiFormSchema>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      weight: "", height: "", waist: "", chest: "", arm: "", thigh: "", bodyType: "",
      primaryGoals: [], customGoal: "",
      workoutDays: "", workoutTime: "", soreness: "",
      medicalConditions: [],
      workoutLocation: "", availableEquipment: [],
    },
    mode: "onChange",
  });

  const isLastStep = currentStep === baseSteps.length - 1;
  const progress = ((currentStep + 1) / baseSteps.length) * 100;
  
  // Watch location to dynamically render equipment
  const selectedLocation = form.watch("workoutLocation");

  const handleNextButton = async () => {
    let fieldsToValidate: (keyof MultiFormSchema)[] = [];
    if (currentStep === 0) fieldsToValidate = ["weight", "height", "waist", "chest", "arm", "thigh", "bodyType"];
    if (currentStep === 1) fieldsToValidate = ["primaryGoals", "customGoal"];
    if (currentStep === 2) fieldsToValidate = ["workoutDays", "workoutTime", "soreness"];
    if (currentStep === 3) fieldsToValidate = ["medicalConditions"];
    if (currentStep === 4) fieldsToValidate = ["workoutLocation"];
    
    const isValid = await form.trigger(fieldsToValidate);
    
    if (isValid) {
      setCurrentStep((prev) => prev + 1);
    } else {
      toast.error("Please complete all required fields.");
    }
  };

  const handleBackButton = () => { if (currentStep > 0) setCurrentStep((prev) => prev - 1); };

  // --- NEW: CONNECTED SUBMISSION HANDLER ---
  const handleFinalSubmit = async (values: MultiFormSchema) => {
    toast.success("Profile Sent! Evaluating goals and generating protocol...");
    
    try {
      // 1. Package the payload with a static test user ID
      const payload = { ...values, userId: "user_123" };

      // 2. Send to Flask Backend to run ML and save to Neon
      const response = await fetch("http://localhost:5000/api/onboarding", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Failed to save profile to backend.");
      }

      const result = await response.json();
      console.log("✅ ML Calculation & Database Save Successful:", result);
      
      // 3. Redirect user to the active dashboard
      router.push("/nutrition"); 

    } catch (error) {
      console.error("❌ Onboarding Error:", error);
      toast.error("Failed to connect to AI engine. Please try again.");
    }
  };

  const CurrentIcon = baseSteps[currentStep].icon;

  const theme = {
    bgMain: { backgroundColor: '#ffffff', color: '#1c1917', borderColor: '#f0f0f0' },
    bgCard: { backgroundColor: '#fdfcf8', border: '1px solid #e5e5e0', borderRadius: '16px' },
    input: { backgroundColor: '#ffffff', border: '1px solid #e5e5e0', color: '#1c1917', height: '56px', borderRadius: '8px' },
    label: { color: '#78716c', textTransform: 'uppercase', fontSize: '12px', letterSpacing: '0.05em', marginBottom: '8px', display: 'block' } as React.CSSProperties,
    textMuted: { color: '#78716c' },
  };

  // MULTIPLE CHOICE GRID (Checkboxes)
  const renderCheckboxGrid = (name: keyof MultiFormSchema, options: {id: string, label: string}[], label: string) => (
    <div className="space-y-4">
      <label style={theme.label}>{label}</label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {options.map((item) => (
          <FormField key={item.id} control={form.control} name={name} render={({ field }) => {
            const isSelected = (field.value as string[])?.includes(item.id);
            return (
              <FormItem style={{ ...theme.bgCard, padding: '16px 20px', cursor: 'pointer', borderColor: isSelected ? '#93c5fd' : '#e5e5e0', backgroundColor: isSelected ? '#eff6ff' : '#ffffff' }} className="flex flex-row items-center space-x-4 space-y-0 hover:shadow-sm transition-all">
                <FormControl>
                  <Checkbox 
                    checked={isSelected}
                    onCheckedChange={(checked) => checked ? field.onChange([...(field.value as string[] || []), item.id]) : field.onChange((field.value as string[])?.filter((val) => val !== item.id))}
                    className="scale-125 border-stone-300 data-[state=checked]:bg-blue-500 data-[state=checked]:border-blue-500"
                  />
                </FormControl>
                <FormLabel className="font-medium text-stone-800 cursor-pointer w-full !mt-0">{item.label}</FormLabel>
              </FormItem>
            );
          }} />
        ))}
      </div>
      {form.formState.errors[name] && <p className="text-sm text-red-500">{form.formState.errors[name]?.message as string}</p>}
    </div>
  );

  // SINGLE CHOICE GRID (Radios acting as buttons)
  const renderRadioGrid = (name: keyof MultiFormSchema, options: {id: string, label: string}[], label: string) => (
    <div className="space-y-4">
      <label style={theme.label}>{label}</label>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {options.map((item) => (
          <FormField key={item.id} control={form.control} name={name} render={({ field }) => {
            const isSelected = field.value === item.id;
            return (
              <FormItem onClick={() => field.onChange(item.id)} style={{ ...theme.bgCard, padding: '16px 20px', cursor: 'pointer', borderColor: isSelected ? '#93c5fd' : '#e5e5e0', backgroundColor: isSelected ? '#eff6ff' : '#ffffff' }} className="hover:shadow-sm transition-all">
                <FormLabel className="font-medium text-stone-800 cursor-pointer w-full !mt-0 flex items-center justify-between">
                  {item.label}
                  <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${isSelected ? 'border-blue-500' : 'border-stone-300'}`}>
                    {isSelected && <div className="w-2.5 h-2.5 rounded-full bg-blue-500" />}
                  </div>
                </FormLabel>
              </FormItem>
            );
          }} />
        ))}
      </div>
      {form.formState.errors[name] && <p className="text-sm text-red-500">{form.formState.errors[name]?.message as string}</p>}
    </div>
  );

  const renderCurrentStepContent = () => {
    switch (currentStep) {
      case 0: 
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
            <div className="grid grid-cols-2 gap-6">
              <FormField control={form.control} name="weight" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Weight (kg)</FormLabel><FormControl><Input type="number" placeholder="e.g. 75" style={theme.input} {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="height" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Height (cm)</FormLabel><FormControl><Input type="number" placeholder="e.g. 180" style={theme.input} {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              
              {/* NEW: Tape Measurements */}
              <FormField control={form.control} name="waist" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Waist (cm)</FormLabel><FormControl><Input type="number" placeholder="Navel level" style={theme.input} {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="chest" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Chest (cm)</FormLabel><FormControl><Input type="number" placeholder="Widest point" style={theme.input} {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="arm" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Arm (cm)</FormLabel><FormControl><Input type="number" placeholder="Flexed bicep" style={theme.input} {...field} /></FormControl><FormMessage /></FormItem>
              )} />
              <FormField control={form.control} name="thigh" render={({ field }) => (
                <FormItem><FormLabel style={theme.label}>Thigh (cm)</FormLabel><FormControl><Input type="number" placeholder="Widest point" style={theme.input} {...field} /></FormControl><FormMessage /></FormItem>
              )} />
            </div>
            {renderRadioGrid("bodyType", bodyTypes, "Select Closest Body Type")}
          </div>
        );
      case 1:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
            <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 flex items-start gap-3">
              <Sparkles className="w-5 h-5 text-blue-500 mt-0.5 shrink-0" />
              <p className="text-sm text-blue-800 leading-relaxed">Our AI Engine will evaluate your goals against your body metrics in the next step to ensure they are safe, realistic, and optimal.</p>
            </div>
            {renderCheckboxGrid("primaryGoals", goalOptions, "Select Your Goals")}
            <div className="relative flex items-center py-2"><div className="flex-grow border-t border-stone-200"></div><span className="flex-shrink-0 mx-4 text-stone-400 text-sm font-medium">OR</span><div className="flex-grow border-t border-stone-200"></div></div>
            <FormField control={form.control} name="customGoal" render={({ field }) => (
              <FormItem>
                <FormLabel style={theme.label}>Describe your custom goal</FormLabel>
                <FormControl><Textarea placeholder="e.g. I want to lose belly fat quickly but keep my leg muscle..." className="resize-none" style={{...theme.input, height: '100px', paddingTop: '12px'}} {...field} /></FormControl>
                <FormMessage />
              </FormItem>
            )} />
          </div>
        );
      case 2:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
            {renderRadioGrid("workoutDays", daysOptions, "Workout Availability")}
            {renderRadioGrid("workoutTime", timeOptions, "Preferred Time of Day")}
            {renderRadioGrid("soreness", recoveryOptions, "How long does muscle soreness last?")}
          </div>
        );
      case 3:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
            {renderCheckboxGrid("medicalConditions", medicalOptions, "Select Any Medical Conditions")}
          </div>
        );
      case 4:
        return (
          <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
            {renderRadioGrid("workoutLocation", locationOptions, "Where will you train?")}
            
            {/* Conditional Rendering based on Location */}
            {selectedLocation === "home" && (
               <div className="pt-4 border-t border-stone-100 animate-in fade-in">{renderCheckboxGrid("availableEquipment", homeEquipment, "Available Home Equipment")}</div>
            )}
            {selectedLocation === "basic_gym" && (
               <div className="pt-4 border-t border-stone-100 animate-in fade-in">{renderCheckboxGrid("availableEquipment", basicGymEquipment, "Available Gym Machines")}</div>
            )}
            {selectedLocation === "pro_gym" && (
              <div className="p-4 bg-emerald-50 border border-emerald-100 rounded-xl mt-4 animate-in fade-in"><p className="text-emerald-800 text-sm font-medium">Great! A professional gym gives us access to all standard equipment for maximum optimization.</p></div>
            )}
          </div>
        );
      default: return null;
    }
  };

  return (
    <div className="min-h-screen bg-[#fdfcf8] py-12 px-4 flex justify-center items-center font-sans text-stone-900">
      <div className="w-full max-w-4xl mx-auto">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleFinalSubmit)}>
            <Card style={{ ...theme.bgMain, borderRadius: '24px', overflow: 'hidden', boxShadow: '0 10px 40px -10px rgba(0,0,0,0.08)' }}>
              <CardHeader style={{ padding: '40px', borderBottom: '1px solid #f0f0f0', background: 'linear-gradient(to bottom, #ffffff, #fdfcf8)' }}>
                <div className="flex justify-between items-center">
                  <div className="flex items-center gap-4">
                    <div className="p-3 bg-blue-50 rounded-xl border border-blue-100"><CurrentIcon className="w-6 h-6 text-blue-500"/></div>
                    <div>
                      <CardTitle className="text-2xl font-bold text-stone-800">{baseSteps[currentStep].title}</CardTitle>
                      <CardDescription style={theme.textMuted}>{baseSteps[currentStep].description}</CardDescription>
                    </div>
                  </div>
                  <span className="text-stone-500 font-bold text-sm bg-stone-100 px-4 py-2 rounded-full border border-stone-200">STEP {currentStep+1} / {baseSteps.length}</span>
                </div>
                <div style={{ height: '6px', backgroundColor: '#f0f0f0', marginTop: '24px', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${progress}%`, backgroundColor: '#60a5fa', transition: 'width 0.5s ease' }} />
                </div>
              </CardHeader>
              <div>
                <CardContent style={{ padding: '40px', backgroundColor: '#ffffff', minHeight: '400px' }}>
                  {renderCurrentStepContent()}
                </CardContent>
                <CardFooter style={{ padding: '32px 40px', borderTop: '1px solid #f0f0f0', backgroundColor: '#fdfcf8' }}>
                  <div className="flex w-full justify-between">
                    <Button type="button" variant="ghost" onClick={handleBackButton} disabled={currentStep===0} className="text-stone-500 hover:bg-stone-100 hover:text-stone-800" style={{ visibility: currentStep===0 ? 'hidden' : 'visible' }}>
                      <ChevronLeft className="mr-2 h-5 w-5"/> Back
                    </Button>
                    {!isLastStep ? (
                        <Button type="button" onClick={handleNextButton} className="bg-blue-500 hover:bg-blue-600 text-white px-8 h-12 text-base rounded-xl font-semibold shadow-sm transition-all">
                          Next Step <ChevronRight className="ml-2 h-5 w-5"/>
                        </Button>
                    ) : (
                        <Button type="submit" disabled={form.formState.isSubmitting} className="bg-stone-800 hover:bg-stone-900 text-white px-8 h-12 text-base rounded-xl font-semibold shadow-md transition-all">
                            {form.formState.isSubmitting && <Loader2 className="mr-2 animate-spin"/>} Evaluate Profile
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