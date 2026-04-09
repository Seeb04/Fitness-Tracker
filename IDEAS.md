# 🚀 Phase 2: The SaaS Vision (Feature Backlog)

This section outlines the advanced features required to evolve the MVP into a fully-fledged fitness and nutrition Software as a Service (SaaS) application.

## 1. Advanced User Profile & Biometrics
* **BMR & TDEE Integration:** Transition from simple BMI calculation to utilizing the Mifflin-St Jeor equation to calculate Basal Metabolic Rate (BMR) based on Age, Weight, Height, and Gender.
* **Goal-Oriented Calorie Targets:** Allow users to select a specific fitness goal (Cut, Bulk, Maintain). The system will automatically calculate their Total Daily Energy Expenditure (TDEE) and establish daily caloric targets.
* **Dynamic Weight Logging:** Implement a daily weight log that automatically recalculates the user's BMR and adjusts daily calorie targets in real-time.

## 2. The Overview Dashboard (Command Center)
* **Calorie & Macro Ring Chart:** A visual dashboard component showing total calories consumed versus the daily target, including distinct progress indicators for Protein, Carbs, and Fats.
* **Weight Trend Graph:** A line chart visualizing body weight fluctuations over customizable timeframes (e.g., 30 days, 6 months).
* **Smart Routine Widget:** * Reads the user's active workout routine (e.g., PPL).
  * Analyzes the previous day's logged session.
  * Automatically suggests the current day's workout (e.g., "Today is Pull Day").
  * Includes manual overrides (e.g., "Skip" or "Log Rest Day").
* **Quick-Add Modals:** Floating Action Buttons (FABs) to log meals or workouts instantly via modal windows without leaving the dashboard.

## 3. Nutrition & Recipe Engine (The Meal Page)
* **Macro-First Tracking:** Ensure every nutritional log explicitly tracks Protein (g), Carbs (g), and Fats (g) alongside total calories.
* **The Recipe Database:** A searchable library of pre-built meals. Users select an item, input their serving size, and the system auto-calculates the resulting macros.
* **Custom Recipe Builder:** A tool allowing users to input individual ingredients to create and save custom meals, defining total macros per serving for efficient future logging.
* **Weekly Analytics:** A bar graph displaying daily caloric intake over the current week to identify consistency patterns or the impact of cheat days.

## 4. Workout & Routine Engine (The Workout Page)
* **The Routine Builder:** * Enable users to create and name multi-week programs (e.g., "6-Week PPL Phase 1").
  * Allow users to define specific days (Push, Pull, Legs) and link exercises to those days.
  * Support defining target Sets, Reps, Rest Times, and estimated session duration.
* **Session Execution Mode:** A "Start Workout" interface that acts as a live checklist, displaying required exercises, target reps, and active resting timers for that specific day's routine.
* **Progressive Overload Tracker:** Require users to record the actual weight lifted for each set during a session. Provide historical charts for specific exercises (e.g., Barbell Bench Press) to visualize strength progression over time.
* **The Exercise Library:** A comprehensive database of common individual exercises to utilize within the Routine Builder, featuring the capability to add custom or niche exercises.