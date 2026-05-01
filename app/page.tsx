"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Activity,
  Target,
  Apple,
  Dumbbell,
  CheckCircle2,
} from "lucide-react";

// Assuming you have this correctly installed from Aceternity UI
import { Boxes } from "@/components/ui/background-boxes"; 

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 overflow-x-hidden selection:bg-cyan-500/30 selection:text-cyan-100 font-sans">
      
      {/* ================= HERO SECTION ================= */}
      <section className="relative w-full min-h-screen flex items-center justify-center overflow-hidden border-b border-white/5">
        
        {/* Full-Screen Background Boxes */}
        {/* Full-Screen Background Boxes (Increased opacity to 60) */}
        <div className="absolute inset-0 w-full h-full z-0 overflow-hidden opacity-60">
          <Boxes />
        </div>

        {/* Lighter mask with a wider transparent center so boxes show clearly */}
        <div className="absolute inset-0 w-full h-full bg-slate-950/40 z-10 [mask-image:radial-gradient(ellipse_at_center,transparent_40%,black_100%)] pointer-events-none" />

        {/* GLOWING ORBS (The Neon Backlight) */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-cyan-600/20 rounded-full blur-[120px] pointer-events-none z-10" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[300px] bg-blue-600/20 rounded-full blur-[100px] pointer-events-none z-10" />

        {/* Hero Content */}
        <div className="relative z-20 max-w-4xl mx-auto px-6 text-center flex flex-col items-center">
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, ease: "easeOut" }}
            className="text-5xl md:text-7xl font-extrabold tracking-tight text-white drop-shadow-lg"
          >
            Think-<span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500 drop-shadow-[0_0_15px_rgba(34,211,238,0.5)]">Fit</span>
            <span className="block mt-4 text-2xl md:text-4xl font-semibold text-slate-400">
              Your AI-Powered Protocol
            </span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15, duration: 0.6 }}
            className="mt-8 max-w-2xl mx-auto text-base md:text-xl text-slate-400 leading-relaxed font-medium"
          >
            Eliminate the guesswork. Our advanced AI engine analyzes your unique biomechanics, 
            goals, and lifestyle to generate the ultimate, science-backed training strategy.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.6 }}
            className="mt-12 flex flex-col sm:flex-row justify-center gap-6 w-full sm:w-auto"
          >
            <Link href="/signup" className="w-full sm:w-auto">
              <Button
                size="lg"
                // GLOWING PRIMARY BUTTON
                className="w-full sm:w-auto h-14 px-8 rounded-full bg-cyan-500 text-slate-950 text-lg font-extrabold hover:bg-cyan-400 shadow-[0_0_30px_rgba(6,182,212,0.4)] hover:shadow-[0_0_40px_rgba(6,182,212,0.6)] transition-all duration-300 hover:-translate-y-1 border border-cyan-300/50"
              >
                Start Assessment
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>

            <Link href="/login" className="w-full sm:w-auto">
              <Button
                size="lg"
                variant="outline"
                // GLOWING OUTLINE BUTTON
                className="w-full sm:w-auto h-14 px-8 rounded-full border-cyan-500/30 bg-slate-900/50 backdrop-blur-md text-cyan-50 text-lg font-bold hover:bg-cyan-500/10 hover:text-cyan-300 hover:border-cyan-400/50 transition-all shadow-[0_0_15px_rgba(6,182,212,0.0)] hover:shadow-[0_0_20px_rgba(6,182,212,0.2)]"
              >
                Log In
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* ================= FEATURES SECTION ================= */}
      <section className="py-28 relative z-10 border-b border-white/5 bg-slate-950">
        
        {/* Subtle background glow for features */}
        <div className="absolute top-1/4 left-0 w-96 h-96 bg-blue-600/10 rounded-full blur-[120px] pointer-events-none" />
        <div className="absolute bottom-1/4 right-0 w-96 h-96 bg-cyan-600/10 rounded-full blur-[120px] pointer-events-none" />

        <div className="max-w-7xl mx-auto px-6 relative z-10">
          <div className="text-center max-w-3xl mx-auto mb-20">
            <h2 className="text-4xl md:text-5xl font-extrabold text-white mb-6 tracking-tight">
              Why Choose Think-Fit?
            </h2>
            <p className="text-slate-400 text-lg md:text-xl font-medium">
              We replace generic templates with precision algorithms designed for maximum hypertrophy and sustainable progress.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              { title: "Smart Progression", desc: "Dynamic volume and intensity scaling based on your daily recovery metrics.", icon: Activity, color: "text-cyan-400", bg: "bg-cyan-500/10" },
              { title: "Targeted Hypertrophy", desc: "Precision exercise selection mapped exactly to your weak points and goals.", icon: Target, color: "text-red-400", bg: "bg-red-500/10" },
              { title: "Biomechanic Matching", desc: "Exercises tailored to your available equipment and specific joint health.", icon: Dumbbell, color: "text-sky-400", bg: "bg-sky-500/10" },
              { title: "AI powered Nutrition Tracking", desc: "Track your daily nutrition conviniently by clicking a photo of your meal.", icon: Apple, color: "text-green-400", bg: "bg-green-500/10" },
            ].map((f, i) => (
              <div
                key={i}
                // DARK GLASSMORPHISM WITH HOVER GLOW
                className="group relative p-8 rounded-3xl border border-slate-800 bg-slate-900/40 backdrop-blur-xl shadow-lg hover:shadow-[0_0_30px_rgba(34,211,238,0.15)] hover:border-cyan-500/50 transition-all duration-300"
              >
                <div className={`mb-6 h-16 w-16 flex items-center justify-center rounded-2xl ${f.bg} border border-white/5 group-hover:scale-110 group-hover:shadow-[0_0_15px_rgba(34,211,238,0.3)] transition-all duration-300`}>
                  <f.icon className={`w-8 h-8 ${f.color}`} />
                </div>
                <h3 className="text-xl font-bold text-slate-100 mb-3">
                  {f.title}
                </h3>
                <p className="text-slate-400 leading-relaxed font-medium">
                  {f.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ================= CTA / FOOTER ================= */}
      <footer className="relative bg-slate-950 overflow-hidden">
        <div className="max-w-7xl mx-auto px-6 py-24">
          
          {/* NEON CTA CARD */}
          <div className="mb-24 p-12 rounded-[2.5rem] bg-slate-900 border border-slate-800 shadow-2xl grid md:grid-cols-2 gap-12 items-center relative overflow-hidden group hover:border-cyan-500/30 transition-colors duration-500">
            
            {/* Massive Glowing Orbs inside the CTA Card */}
            <div className="absolute top-0 right-0 -mr-20 -mt-20 w-96 h-96 rounded-full bg-cyan-500/20 blur-[100px] group-hover:bg-cyan-500/30 transition-colors duration-700" />
            <div className="absolute bottom-0 left-0 -ml-20 -mb-20 w-96 h-96 rounded-full bg-blue-600/20 blur-[100px] group-hover:bg-blue-600/30 transition-colors duration-700" />

            <div className="relative z-10">
              <h3 className="text-3xl md:text-4xl font-extrabold text-white mb-4 tracking-tight drop-shadow-md">
                Ready to optimize your physique?
              </h3>
              <p className="text-cyan-100/70 text-lg max-w-md font-medium">
                Make objective, data-driven decisions regarding your health with Think-Fit today.
              </p>
              <div className="flex items-center gap-2 mt-6 text-cyan-400 font-bold tracking-wide">
                <CheckCircle2 className="w-5 h-5" />
                Science-Based & Measurable
              </div>
            </div>

            <div className="flex md:justify-end relative z-10">
              <Link href="/signup">
                <Button
                  size="lg"
                  className="h-16 px-10 rounded-full bg-cyan-500 text-slate-950 text-lg font-extrabold hover:bg-cyan-400 shadow-[0_0_30px_rgba(34,211,238,0.4)] hover:shadow-[0_0_50px_rgba(34,211,238,0.6)] hover:scale-105 transition-all duration-300 border border-cyan-300/50"
                >
                  Start Your Journey
                </Button>
              </Link>
            </div>
          </div>

          <div className="border-t border-slate-800/50 pt-10 flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center shadow-[0_0_15px_rgba(34,211,238,0.4)] border border-cyan-300/50">
                <span className="text-slate-950 font-extrabold text-xl">T</span>
              </div>
              <span className="text-xl font-extrabold tracking-tight text-white drop-shadow-sm">Think-Fit</span>
            </div>
            <p className="text-slate-500 text-sm font-medium">
              © 2026 Think-Fit AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}