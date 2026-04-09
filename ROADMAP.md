# 🗺️ Project Roadmap & Tracker

**Current Phase:** Phase 1 (MVP)
**Primary Goal:** Establish a functional, cloud-hosted macro and fitness tracker to secure the DBMS course grade.

## 🏗️ Phase 1: Minimum Viable Product (The Grade Saver)

### 1. Database Foundation (Aiven MySQL)
- [x] Provision cloud database instance.
- [x] Design MVP Schema (Users, Meals, Workouts).
- [x] Execute `CREATE TABLE` scripts for MVP schema.
- [X] Insert 1-2 rows of dummy data manually via Workbench to verify tables.

### 2. Backend API (Vercel Serverless Python)
- [X] Update `requirements.txt` with `mysql-connector-python`.
- [X] Create `/api/add_user.py` (Handles biometric creation/updates).
- [X] Update `/api/add_meal.py` (Include Protein, Carbs, Fats).
- [X] Update `/api/add_workout.py` (Include Category and Duration).
- [X] Securely add Aiven credentials to Vercel Environment Variables.

### 3. Frontend UI (HTML/JS)
- [ ] Build layout structure (Dark/Blue minimalist theme).
- [ ] **Overview Dashboard:**
  - [ ] Implement BMR Calculator (Mifflin-St Jeor equation) via JS.
  - [ ] Build Biometric input form (Age, Weight, Height, Goal).
  - [ ] Display Net Daily Deficit KPI.
- [ ] **Meal Logging:**
  - [ ] Build form (Food, Cals, Protein, Carbs, Fats).
  - [ ] Wire JS `fetch` to `/api/add_meal`.
- [ ] **Workout Logging:**
  - [ ] Build form (Category, Duration, Calories Burned).
  - [ ] Wire JS `fetch` to `/api/add_workout`.

### 4. Testing & Submission
- [ ] Verify End-to-End flow: Web UI -> Vercel API -> Aiven DB.
- [ ] Format DBMS Project Proposal document.
- [ ] Generate ER Diagram from Aiven database using Workbench.
- [ ] Final Vercel deployment check.

---

## 🚀 Phase 2: The SaaS Upgrades (Post-Submission / Extra Time)

### 1. Database Schema Expansion
- [ ] Create `Routines` and `Routine_Days` tables.
- [ ] Create `Exercises` library table.
- [ ] Create `Routine_Day_Exercises` junction table.

### 2. The Routine Builder
- [ ] UI to create a custom routine (e.g., "PPL Phase 1").
- [ ] Smart Dashboard Widget: Read yesterday's workout and suggest today's session based on the active routine.
- [ ] Progressive Overload Tracker (Log weights lifted per set).

### 3. The Recipe Engine
- [ ] Create `Recipes` table.
- [ ] UI to build custom recipes with macro calculations per serving.
- [ ] Dropdown on the Meal Logger to select pre-built recipes.

---

## 📝 Scratchpad / Dev Notes
*Use this space to drop quick SQL queries you need to remember, links to resources, or random ideas so they don't get lost.*

* **Vercel URL:** [https://fitness-tracker-bmpwhkhws-1haze.vercel.app/]
* **Aiven Host:** [mysql-16b13cdb-dbms-lab-fitness.j.aivencloud.com]