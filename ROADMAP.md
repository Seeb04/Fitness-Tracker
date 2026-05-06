# 🗺️ Project Roadmap & Tracker

**Current Phase:** Phase 2 (SaaS Enhancements)
**Primary Goal:** Evolve the functional MVP into a multi-user platform with advanced tracking capabilities.

## ✅ Phase 1: Minimum Viable Product (Completed)
- [x] **Cloud Database:** Aiven MySQL instance provisioned and schema deployed.
- [x] **Multi-Profile Support:** Added `get_users` API and frontend profile switcher.
- [x] **Biometric Engine:** Mifflin-St Jeor BMR & Target calculation with manual override support.
- [x] **Unified Logging:** Expanded `Meals` and `Workouts` to include macros, duration, and categories.
- [x] **Real-time Dashboard:** Today's Net Status KPI and dynamic data fetching.

## 🏗️ Phase 2: SaaS Upgrades (In Progress)

### 1. Advanced Data Management
- [x] **Delete Operations:** Implement `/api/delete_entry.py` for removing logs.
- [x] **Historical Analytics:** View logs by date range (7-day / 30-day views).
- [x] **Weight Tracking:** Dedicated weight-log table to track progress over time.

### 2. The Routine Builder
- [X] Create `Routines` and `Routine_Days` tables.
- [X] UI to build custom routines (e.g., "PPL Phase 1").
- [X] Smart Widget: Suggest today's session based on the active routine.

### 3. The Recipe Engine
- [X] Create `Recipes` table for component-based macro tracking.
- [X] UI to build and select pre-saved recipes in the Meal Logger.

## 🚀 Phase 3: UX & Performance
- [ ] **Visualizations:** Charts for weight trends and macro distribution (Chart.js).
- [ ] **Mobile Optimization:** Refine responsive layout for mobile logging.
- [ ] **Auth Layer:** Simple password protection for profiles.
