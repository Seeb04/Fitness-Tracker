# Gemini Context: Fitness-Tracker

This document serves as the foundational context for Gemini CLI's interaction with the **Fitness-Tracker** project. It outlines the project's architecture, goals, and technical constraints.

## 🎯 Project Overview
The **Fitness-Tracker** is a cloud-native macro and exercise tracking application developed for a DBMS Laboratory course. It focuses on providing a minimalist, high-performance interface for logging nutritional intake and physical activity to calculate net daily energy deficits.

## 🛠️ Tech Stack
- **Frontend:** Single-page application (SPA) using vanilla HTML5, CSS3 (Modern dark/blue theme), and JavaScript (ES6+).
- **Backend:** Python 3.x serverless functions deployed via **Vercel Functions**.
- **Database:** **Aiven MySQL** (Cloud-hosted instance).
- **Deployment:** Vercel (Frontend & API orchestration).

## 🏗️ Core Architecture
- **API Layer (`/api`):** Modular Python scripts acting as serverless endpoints.
  - `add_meal.py`: Handles POST requests to log food items and calories.
  - `add_workout.py`: Handles POST requests to log activity types and calories burned.
- **Data Model:**
  - `Meals`: (LogDate, FoodItem, CaloriesIn)
  - `Workouts`: (LogDate, WorkoutType, CaloriesBurned)
  - *Planned:* `Users` (Biometrics), `Routines`, `Recipes`.

## 📈 Project Scope & Roadmap

### Phase 1: MVP (The Grade Saver) - **Current Focus**
- [ ] Complete `add_user.py` for biometric management.
- [ ] Enhance existing logging to include full macros (Protein, Carbs, Fats).
- [ ] Implement BMR Calculation (Mifflin-St Jeor) in the frontend.
- [ ] Establish a visual "Net Daily Deficit" KPI.

### Phase 2: SaaS Evolution (Backlog)
- [ ] **Routine Builder:** Custom workout plans (e.g., PPL, Upper/Lower).
- [ ] **Recipe Engine:** Component-based recipe macro calculations.
- [ ] **Progressive Overload Tracking:** Logging weights/reps per set.

## 🛡️ Development Mandates
1. **Security:** Never hardcode database credentials. Always use `os.environ.get()` to access Vercel environment variables.
2. **Database Integrity:** Use parameterized queries (`%s`) to prevent SQL injection.
3. **UI Consistency:** Adhere to the defined CSS variables (`--primary`, `--surface`, etc.) for all new components.
4. **Efficiency:** Prefer surgical updates to the single-page `index.html` to maintain its "clean" architecture.

---
*Note: This project is part of a University DBMS Lab. Prioritize database schema normalization and query efficiency in all recommendations.*
