import { generateObject } from 'ai';
import { google } from '@ai-sdk/google';
import { z } from 'zod';
import { NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';
import { Pool } from 'pg';
import { PrismaPg } from '@prisma/adapter-pg';

const connectionString = `${process.env.DATABASE_URL}`;
const pool = new Pool({ connectionString });
const adapter = new PrismaPg(pool);
const prisma = new PrismaClient({ adapter });

export async function POST(req: Request) {
  try {
    const { bio } = await req.json();

    const result = await generateObject({
      model: google('gemini-2.0-flash'), 
      schema: z.object({
        goals: z.array(z.string()).describe('Fitness goals extracted from the text'),
        injuries: z.array(z.string()).describe('Any physical injuries or joint pain'),
        activityLevel: z.string().nullable().describe('Current lifestyle activity level'),
        dietAlignment: z.string().nullable().describe('Vegetarian, Vegan, Non-Vegetarian, etc.'),
        medicalExclusions: z.array(z.string()).describe('Conditions like diabetes, celiac, allergies'),
        dislikes: z.array(z.string()).describe('Specific foods the user refuses to eat'),
        sleepAverage: z.string().nullable().describe('Average hours of sleep per night')
      }),
      prompt: `You are a fitness data extraction engine. Analyze the following user bio and extract the structured data. Return null for unmentioned parameters.\n\nUser Bio: "${bio}"`,
    });

    const extractedData = result.object;

    const user = await prisma.user.create({
      data: {
        goals: extractedData.goals,
        injuries: extractedData.injuries,
        activityLevel: extractedData.activityLevel,
        dietAlignment: extractedData.dietAlignment,
        medicalExclusions: extractedData.medicalExclusions,
        dislikes: extractedData.dislikes,
        sleepAverage: extractedData.sleepAverage,
      }
    });

    return NextResponse.json({ success: true, user });

  } catch (error) {
    console.error("Gemini Extraction Error:", error);
    return NextResponse.json({ error: 'Failed to process brain dump' }, { status: 500 });
  }
}