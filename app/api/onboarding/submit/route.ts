import { NextResponse } from 'next/server';
import { neon } from '@neondatabase/serverless';
import jwt from 'jsonwebtoken';
import { cookies } from 'next/headers';

const sql = neon(process.env.DATABASE_URL!);
const JWT_SECRET = process.env.JWT_SECRET || 'fallback_secret_do_not_use_in_prod';

export async function POST(req: Request) {
  try {
    // 1. Authenticate the user securely via their HTTP-only cookie
    const cookieStore = await cookies();
    const token = cookieStore.get('auth_token')?.value;

    if (!token) {
      return NextResponse.json({ error: "Unauthorized. No session found." }, { status: 401 });
    }

    // Decode the token to reliably get their email/ID without trusting the frontend
    const decodedToken = jwt.verify(token, JWT_SECRET) as { email: string };
    const userEmail = decodedToken.email;

    // 2. Extract the payload from the onboarding form
    const body = await req.json();
    
    // 3. Execute the definitive UPDATE query
    // We use the email from the secure token to ensure users can only update their own row
    await sql`
      UPDATE users
      SET
        weight_kg = ${body.weight_kg},
        height_cm = ${body.height_cm},
        body_fat_pct = ${body.body_fat_pct},
        body_type = ${body.body_type},
        waist_cm = ${body.waist_cm},
        chest_cm = ${body.chest_cm},
        arm_cm = ${body.arm_cm},
        thigh_cm = ${body.thigh_cm},
        primary_goals = ${body.primary_goals},
        workout_days = ${body.workout_days},
        soreness_recovery = ${body.soreness_recovery},
        medical_conditions = ${body.medical_conditions},
        workout_location = ${body.workout_location},
        available_equipment = ${body.available_equipment},
        target_calories = ${body.target_calories},
        target_protein = ${body.target_protein},
        target_carbs = ${body.target_carbs},
        target_fat = ${body.target_fat},
        sat_fat_limit = ${body.sat_fat_limit}
      WHERE email = ${userEmail}
    `;

    return NextResponse.json({ message: "Onboarding profile saved successfully" }, { status: 200 });

  } catch (error) {
    console.error("Onboarding Update Error:", error);
    return NextResponse.json({ error: "Failed to save onboarding data" }, { status: 500 });
  }
}