# Fitracker

Fitracker is a personal fitness and nutrition management application designed to track biometrics, log meals, and architect workout protocols.

## Features

- **Biometric Dashboard**: Automatically calculates Basal Metabolic Rate (BMR) using the Mifflin-St Jeor equation, Total Daily Energy Expenditure (TDEE), and Body Mass Index (BMI).
- **Nutrition Logging**: Track daily calorie intake and macros (Protein, Carbs, Fats).
- **Recipe System**: Save frequent meals as recipes for quick one-click logging.
- **Protocol Architect**: Create custom workout routines (splits) with specific exercises, sets, and reps.
- **Activity Tracking**: Log workouts and monitor calories burned.
- **Progress Visualization**: Interactive charts for weight timeline, daily calorie balance, and macro distribution using Chart.js.
- **User Profiles**: Support for multiple user accounts with passcode-protected access.

## Tech Stack

- **Frontend**: Vanilla HTML5, CSS3, and JavaScript.
- **Backend**: Python (Serverless Function architecture).
- **Database**: MySQL.
- **Visualization**: Chart.js.

## Database Configuration

The application requires a MySQL database. Connection settings are managed via environment variables:

- `DB_HOST`: Database host address.
- `DB_USER`: Database username.
- `DB_PASSWORD`: Database password.
- `DB_NAME`: Database name.
- `DB_PORT`: Database port (defaults to 15463).

## Installation

1. Clone the repository.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the required environment variables for the database connection.
4. Ensure a MySQL server is running with the appropriate schema.
