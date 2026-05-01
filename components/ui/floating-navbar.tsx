"use client";
import React, { useState } from "react";
import {
  motion,
  AnimatePresence,
  useScroll,
  useMotionValueEvent,
} from "framer-motion";
import { cn } from "@/lib/utils";
import { useRouter } from "next/navigation";

export const FloatingNav = ({
  navItems,
  className,
}: {
  navItems: {
    name: string;
    link: string;
    icon?: React.ReactNode;
  }[];
  className?: string;
}) => {
  const router = useRouter();
  
  // Changed from scrollYProgress to scrollY for accurate pixel-based tracking
  const { scrollY } = useScroll();
  
  // Default to true so it's visible on first load
  const [visible, setVisible] = useState(true);

  useMotionValueEvent(scrollY, "change", (current) => {
    if (typeof current === "number") {
      const direction = current - scrollY.getPrevious()!;

      // 1. If we are at the very top of the page (within 50px), ALWAYS show it.
      if (current < 50) {
        setVisible(true);
      } else {
        // 2. If scrolling UP, show it. If scrolling DOWN, hide it.
        if (direction < 0) {
          setVisible(true);
        } else {
          setVisible(false);
        }
      }
    }
  });

  const handleLogout = () => {
    console.log("Logging out...");
    router.push("/");
  };

  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial={{
          opacity: 1,
          y: -100,
        }}
        animate={{
          y: visible ? 0 : -100,
          opacity: visible ? 1 : 0,
        }}
        transition={{
          duration: 0.3,
          ease: "easeInOut"
        }}
        className={cn(
          "flex max-w-fit fixed top-6 inset-x-0 mx-auto z-[5000] items-center justify-center",
          className
        )}
      >
        {/* 
          UPDATED CONTAINER: 
          - White background with frosted glass (bg-white/90 + backdrop-blur)
          - Reduced padding (px-2 py-1.5) for a tighter, smaller profile
          - Beautiful soft glow (shadow-[0_0_20px_rgba(255,255,255,0.4)])
        */}
        <div className="flex items-center justify-center gap-2 rounded-full border border-white/40 bg-white/90 px-2 py-1.5 shadow-[0_0_20px_rgba(0,205,205,0.2)] backdrop-blur-md">
          
          {/* Nav items container */}
          <div className="flex items-center gap-1">
            {navItems.map((navItem, idx: number) => (
              <a
                key={`link-${idx}`}
                href={navItem.link}
                className={cn(
                  // Reduced text size to text-sm, slate text on white background
                  "relative flex items-center gap-1.5 rounded-full px-4 py-2 text-sm font-semibold text-slate-700 transition-colors hover:bg-slate-100 hover:text-cyan-600"
                )}
              >
                <span className="block sm:hidden">{navItem.icon}</span>
                <span className="hidden sm:block">{navItem.name}</span>
              </a>
            ))}
          </div>

          {/* Divider */}
          <div className="h-5 w-px bg-slate-200" />

          {/* LOGOUT BUTTON: Reduced size, high contrast */}
          <button 
            onClick={handleLogout}
            className="relative rounded-full bg-slate-900 px-5 py-2 text-sm font-bold text-white transition-all hover:bg-slate-800 hover:shadow-[0_0_15px_rgba(0,0,0,0.2)] active:scale-95"
          >
            <span>Logout</span>
          </button>
        </div>
      </motion.div>
    </AnimatePresence>
  );
};