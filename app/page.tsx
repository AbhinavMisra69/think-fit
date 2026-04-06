'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';

export default function Home() {
  const [bio, setBio] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    setLoading(true);
    
    const response = await fetch('/api/onboarding', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bio }),
    });
    
    const data = await response.json();
    
    if (data.success) {
      setResult(data.user);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-zinc-50 flex items-center justify-center p-4 text-zinc-900">
      <Card className="w-full max-w-xl shadow-lg border-zinc-200">
        <CardHeader>
          <CardTitle className="text-2xl font-semibold tracking-tight">Think Fit: Brain Dump</CardTitle>
          <CardDescription className="text-zinc-500">
            Tell us about your current lifestyle, what you want to achieve, any nagging injuries, and your daily routine.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea 
            placeholder="I sleep 6 hours a day, want to lose 10kg, my knees hurt when I run, and I'm a vegetarian..." 
            className="min-h-[150px] resize-none focus-visible:ring-zinc-400"
            value={bio}
            onChange={(e) => setBio(e.target.value)}
          />
          <Button 
            className="w-full bg-zinc-900 text-white hover:bg-zinc-800" 
            onClick={handleSubmit}
            disabled={loading || !bio}
          >
            {loading ? 'Analyzing Profile...' : 'Process Profile'}
          </Button>
          
          {result && (
            <div className="mt-6 p-4 bg-zinc-100 rounded-md text-sm font-mono overflow-x-auto">
              <pre>{JSON.stringify(result, null, 2)}</pre>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}