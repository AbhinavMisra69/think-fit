'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';

// Define the shape of our User object
type User = {
  id: string;
  email: string;
  name: string;
};

// Define the shape of our Context
type AuthContextType = {
  user: User | null;
  isLoading: boolean;
  login: (email: string, pass: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true); // Start true while we check for existing session
  const router = useRouter();
  const pathname = usePathname();

  // --- 1. Check for existing session on load ---
  useEffect(() => {
    const checkSession = () => {
      const storedSession = localStorage.getItem('thinkfit_session');
      if (storedSession) {
        setUser(JSON.parse(storedSession));
      }
      setIsLoading(false);
    };
    checkSession();
  }, []);

  // --- 2. Protect Routes ---
  // Define which paths require the user to be logged in
  const protectedRoutes = ['/dashboard', '/nutrition', '/workouts'];

  useEffect(() => {
    if (!isLoading) {
      const isProtectedRoute = protectedRoutes.some(route => pathname.startsWith(route));
      if (isProtectedRoute && !user) {
        router.push('/login'); // Redirect to login if unauthorized
      }
    }
  }, [user, isLoading, pathname, router]);

  // --- 3. Login Logic ---
 // Inside context/AuthContext.tsx
 const login = async (email: string, pass: string) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password: pass }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Failed to log in");
    }

    // Save the returned user data to state
    setUser(data.user);
    localStorage.setItem('thinkfit_session', JSON.stringify(data.user));
  };

  // --- 4. Logout Logic ---
  const logout = () => {
    setUser(null);
    localStorage.removeItem('thinkfit_session');
    router.push('/login');
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context easily
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
