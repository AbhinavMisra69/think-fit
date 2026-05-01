"use client";

import React from "react";
import { usePathname } from "next/navigation";
import { FloatingNav } from "@/components/ui/floating-navbar"; // Adjust this path if yours is different
import { LayoutDashboard, Apple, LineChart } from "lucide-react";

export function Navigation() {
  const pathname = usePathname();

  // 1. Define the pages where the navbar SHOULD NOT appear
  const hiddenRoutes = ["/", "/login", "/signup", "/manual-onboarding"];
  
  if (hiddenRoutes.includes(pathname)) {
    return null; // Hide the navbar entirely on auth/onboarding pages
  }

  // 2. Define your app routes and icons
  const navItems = [
    { 
      name: "Dashboard", 
      link: "/dashboard", 
      icon: <LayoutDashboard className="w-4 h-4" /> 
    },
    { 
      name: "Nutrition", 
      link: "/nutrition", 
      icon: <Apple className="w-4 h-4" /> 
    },
    { 
      name: "Progress", 
      link: "/progress", 
      icon: <LineChart className="w-4 h-4" /> 
    },
  ];

  return <FloatingNav navItems={navItems} />;
}