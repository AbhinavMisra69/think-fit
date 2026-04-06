'use client';

import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Checkbox } from '@/components/ui/checkbox';

// 1. Updated Zod Schema with better validation strings
const formSchema = z.object({
  goals: z.string().min(1, "Please enter your goals."),
  injuries: z.string().optional(),
  activityLevel: z.string().min(1, "Please select an activity level."),
  dietAlignment: z.string().min(1, "Please select a diet."),
  medicalExclusions: z.string().optional(),
  dislikes: z.string().optional(),
  availableEquipment: z.array(z.string()).min(1, "Select at least one item."),
  sleepAverage: z.string().min(1, "Please select average sleep."),
});

const equipmentList = [
  { id: "dumbbells", label: "Dumbbells" },
  { id: "resistance_bands", label: "Resistance Bands" },
  { id: "pull_up_bar", label: "Pull-up Bar" },
  { id: "bench", label: "Weight Bench" },
  { id: "none", label: "Bodyweight Only" },
];

export default function ManualOnboarding() {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      goals: "",
      injuries: "",
      medicalExclusions: "",
      dislikes: "",
      availableEquipment: [],
      activityLevel: "",
      dietAlignment: "",
      sleepAverage: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsSubmitting(true);
    
    const formattedData = {
      ...values,
      goals: values.goals.split(',').map(s => s.trim()),
      injuries: values.injuries ? values.injuries.split(',').map(s => s.trim()) : [],
      medicalExclusions: values.medicalExclusions ? values.medicalExclusions.split(',').map(s => s.trim()) : [],
      dislikes: values.dislikes ? values.dislikes.split(',').map(s => s.trim()) : [],
    };

    console.log("Data ready for Prisma:", formattedData);
    // Future: fetch('/api/user/update', { method: 'POST', body: JSON.stringify(formattedData) })
    
    setTimeout(() => setIsSubmitting(false), 1000);
  }

  return (
    <div className="min-h-screen bg-zinc-50 py-12 px-4 flex justify-center text-zinc-900">
      <Card className="w-full max-w-2xl shadow-lg border-zinc-200">
        <CardHeader>
          <CardTitle className="text-2xl font-semibold tracking-tight">Complete Your Profile</CardTitle>
          <CardDescription className="text-zinc-500">
            Verify your physical metrics and lifestyle parameters.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              
              <div className="space-y-4">
                <h3 className="text-lg font-medium border-b pb-2">Objectives</h3>
                
                <FormField
                  control={form.control}
                  name="goals"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Primary Goals (Comma separated)</FormLabel>
                      <FormControl>
                        <Input placeholder="Lose 10kg, build muscle" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="activityLevel"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Daily Activity Level</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select activity" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="sedentary">Sedentary</SelectItem>
                          <SelectItem value="light">Lightly Active</SelectItem>
                          <SelectItem value="moderate">Moderately Active</SelectItem>
                          <SelectItem value="very">Very Active</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="sleepAverage"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Average Sleep</FormLabel>
                      <Select onValueChange={field.onChange} defaultValue={field.value}>
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select sleep" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="under_5">&lt; 5h</SelectItem>
                          <SelectItem value="5_to_6">5-6h</SelectItem>
                          <SelectItem value="7_to_8">7-8h</SelectItem>
                          <SelectItem value="over_8">8h+</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="space-y-4">
                <h3 className="text-lg font-medium border-b pb-2">Available Equipment</h3>
                <FormField
                  control={form.control}
                  name="availableEquipment"
                  render={() => (
                    <FormItem>
                      <div className="grid grid-cols-2 gap-4">
                        {equipmentList.map((item) => (
                          <FormField
                            key={item.id}
                            control={form.control}
                            name="availableEquipment"
                            render={({ field }) => (
                              <FormItem className="flex flex-row items-start space-x-3 space-y-0">
                                <FormControl>
                                  <Checkbox
                                    checked={field.value?.includes(item.id)}
                                    onCheckedChange={(checked) => {
                                      return checked
                                        ? field.onChange([...field.value, item.id])
                                        : field.onChange(field.value?.filter((val: string) => val !== item.id))
                                    }}
                                  />
                                </FormControl>
                                <FormLabel className="font-normal">{item.label}</FormLabel>
                              </FormItem>
                            )}
                          />
                        ))}
                      </div>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <Button type="submit" className="w-full bg-zinc-900 text-white" disabled={isSubmitting}>
                {isSubmitting ? 'Saving...' : 'Finalize Protocol'}
              </Button>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}