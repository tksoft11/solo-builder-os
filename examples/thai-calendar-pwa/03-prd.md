# PRD Writer Output (World-Class Edition)

## 1. The Amazon PR/FAQ (Working Backwards)

**Press Release (Target Date: Jan 2027)**
**BANGKOK** — Today, a solo developer launched "Thai Holiday Hacker," a blazingly fast web app designed to save Thai office workers from burnout. Unlike traditional calendars that simply list dates, Thai Holiday Hacker acts as a strategic vacation planner. Upon opening the app, users are greeted with a massive countdown to their next day off. More importantly, its proprietary "Leave Maximizer" engine instantly scans the year's public holidays and highlights strategic "bridge days"—showing users exactly when to use their limited 6 days of annual leave to unlock over 20 days of continuous long weekends. It requires no login, no download, and is completely free. 

**FAQ for the User**
- *Q: Do I need to create an account?* A: No. The app works instantly in your browser and saves your preferences locally on your device.
- *Q: What if the government adds a special holiday?* A: The database is updated over-the-air within 24 hours of any official cabinet resolution.

**FAQ for the Internal Team (Solo Founder)**
- *Q: How do we handle different holiday rules (e.g., Bank holidays vs Government holidays)?* A: The MVP will focus solely on Bank Holidays (BOT schedule) as it covers the vast majority of private-sector office workers, our primary demographic.

## 2. Success Metrics (The North Star)
- **North Star Metric:** "Maximized Weekends Saved" (Count of users who click the "Add Long Weekend to Calendar" button).
- **Secondary Metric (Performance):** Largest Contentful Paint (LCP) must be under 1.2 seconds on a 3G mobile network.
- **Retention Metric:** Percentage of users who return to the site within 30 days.

## 3. MECE User Stories & Acceptance Criteria

We use the Mutually Exclusive, Collectively Exhaustive (MECE) principle to ensure all edge cases of holiday calculations are covered.

### Epic 1: The Relief Engine (Next Holiday Countdown)
- **Story:** As an exhausted worker, I want to see a countdown to the next holiday immediately, so I feel relief.
- **Acceptance Criteria 1.1:** The system must detect the user's current local time (Asia/Bangkok).
- **Acceptance Criteria 1.2:** The system must filter out holidays that have already passed in the current calendar year.
- **Acceptance Criteria 1.3:** The Top Fold displays the Name of the next holiday, the Date, and a live countdown (Days, Hours, Minutes, Seconds).

### Epic 2: The Leave Maximizer (Strategic Planning)
- **Story:** As a planner, I want the system to tell me which specific working days to take off to bridge public holidays into long weekends.
- **Acceptance Criteria 2.1 (Tuesday Rule):** IF a holiday falls on a Tuesday, the system MUST flag the preceding Monday (1 day leave) as yielding a 4-day weekend (Sat-Tue).
- **Acceptance Criteria 2.2 (Thursday Rule):** IF a holiday falls on a Thursday, the system MUST flag the succeeding Friday (1 day leave) as yielding a 4-day weekend (Thu-Sun).
- **Acceptance Criteria 2.3 (Wednesday Rule):** IF a holiday falls on a Wednesday, the system flags Thu/Fri OR Mon/Tue as yielding a 5-day weekend for 2 days leave.

## 4. Edge Case Matrix

| Scenario | System Behavior |
| :--- | :--- |
| User opens app ON a public holiday. | Countdown targets the *next* holiday. Hero text changes to "Enjoy your day off! Your next break is in X days." |
| User opens app on Dec 31st after all holidays are over. | System seamlessly loads next year's JSON data. Countdown targets New Year's Day or the next applicable holiday. |
| User's device time is set to a different timezone (e.g., traveling abroad). | App strictly forces `Asia/Bangkok` timezone for all calculations to prevent holiday shifting. |

## 5. The Iron Triangle (Out of Scope for V1)
- **NO Push Notifications.** We will not manage a database of device tokens or handle user permissions.
- **NO Custom Holidays.** Users cannot add their own company-specific holidays.
- **NO Native App.** This is strictly a Progressive Web App (PWA) accessed via URL to eliminate app-store friction.
