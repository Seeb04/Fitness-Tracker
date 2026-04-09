# Gemini Context: Fitness-Tracker

## 🎯 Current Status
The project has successfully transitioned from an MVP to a **Multi-User SaaS Framework**. 

## 🛠️ Updated Tech Stack & Architecture
- **Frontend:** SPA with vanilla JS, featuring dynamic profile switching and real-time dashboard updates.
- **Backend:** Python serverless functions on Vercel, now fully parameterized to support dynamic `user_id` context.
- **Database:** Aiven MySQL with a normalized schema supporting `Users`, `Meals`, and `Workouts`.

## 🏗️ Core Multi-User Logic
- **Profile Switching:** The UI maintains a `currentUserId` in `localStorage` and a dropdown selector in the header.
- **Dynamic Fetching:** All GET/POST requests (`/api/get_meals`, `/api/add_workout`, etc.) include a `user_id` query param or payload field.
- **Biometric Engine:** Mifflin-St Jeor calculation with support for a **Manual Calorie Target Override**.

## 🛡️ Active Mandates
1. **Parameterization:** All SQL queries *must* include `WHERE UserID = %s` or use the payload `user_id` to prevent data leaking between profiles.
2. **Schema Integrity:** Adhere to the `dbschema.txt` definitions.
3. **UI Consistency:** All new features must use the established dark/blue theme variables.

---
*Last Updated: April 9, 2026 | Focus: Phase 2 SaaS Enhancements*
