# UX & Code Planner Output (World-Class Edition)

## Part 1: UX Planner (Behavioral Design)

### 1. The Fogg Behavior Model Application
Behavior = Motivation (M) x Ability (A) x Prompt (P)
- **Motivation:** Extremely High (User is burned out and wants a vacation).
- **Ability:** Must be extremely easy (Zero clicks required to see the next holiday).
- **Prompt:** The URL/Bookmark or the organic Google search.

### 2. Information Architecture (IA)
A strict, single-page downward-scrolling hierarchy. No hamburger menus. No navigation bars.
1. **The Hero (Top 100vh):** 
   - Massive typography. 
   - H1: Name of the Holiday. 
   - Dynamic Countdown (Live seconds ticking creates urgency/excitement).
2. **The "Hacker" Section (Next 50vh):**
   - The immediate next "Long Weekend" opportunity.
   - Example: "Take April 12th off to get a 5-day weekend for Songkran."
   - Button: `[Add to Calendar]`
3. **The Ledger (Bottom):**
   - A minimalist, greyed-out list of the remaining holidays this year. Passed holidays are hidden or heavily dimmed to reduce cognitive load.

### 3. Cognitive Load Reduction
- We do not use traditional grid calendars. Grids force the brain to parse rows and columns to find the red number. We use a **chronological timeline feed**, which requires zero parsing effort.

---

## Part 2: Code Planner (Staff-Level Architecture)

### 1. System Architecture (The "Zero-Ops" Monolith)
To achieve sub-second load times and zero server costs for the solo developer, we utilize a statically generated Jamstack architecture.

- **Framework:** Next.js (App Router).
- **Rendering:** Static Site Generation (SSG). The HTML is pre-rendered at build time.
- **Client-Side:** Lightweight React hydration only for the countdown timer.
- **Styling:** Tailwind CSS.
- **Hosting:** Vercel Edge Network.
- **Database:** None. We use a static JSON schema (`data/holidays-th.json`).

### 2. The Data Dictionary (Schema)
```json
// Example object in holidays-th.json
{
  "id": "songkran-2026",
  "name_th": "วันสงกรานต์",
  "name_en": "Songkran Festival",
  "date": "2026-04-13T00:00:00+07:00",
  "is_bank_holiday": true,
  "leave_maximizer_recommendation": {
    "recommended_leave_dates": ["2026-04-16", "2026-04-17"],
    "total_weekend_days": 9
  }
}
```

### 3. SOLID Principles in Practice
- **Single Responsibility Principle (SRP):** The `CountdownTimer` component *only* handles the UI tick. The `TimeEngine` utility class handles the timezone math (`date-fns-tz`) keeping UI and logic decoupled.
- **Open-Closed Principle (OCP):** The holiday data is injected via JSON. When 2027 arrives, we add a new JSON file without touching the core rendering logic.

### 4. Implementation Phases (GitHub Issues)

**Phase 1: Foundation (Day 1)**
- [ ] Init Next.js + Tailwind project. Configure strict ESLint.
- [ ] Create `holidays-th-2026.json` based on BOT data.
- [ ] Build the `TimeEngine` utility to strictly enforce `Asia/Bangkok` timezone regardless of the user's browser location.

**Phase 2: The Core JTBD (Day 2)**
- [ ] Build `HeroCountdown` component. Use `requestAnimationFrame` or simple `setInterval` for the tick.
- [ ] Build `HolidayFeed` component to list remaining dates.

**Phase 3: The Hacker Engine (Day 3)**
- [ ] Write the logic to parse `leave_maximizer_recommendation` and render the "Take Leave Here" badges.
- [ ] Implement `.ics` file generation on the client-side so users can add the "Hacked Weekend" to their Apple/Google calendar.

**Phase 4: Polish & PWA (Day 4)**
- [ ] Generate standard PWA icons and `manifest.json`.
- [ ] Implement Workbox/Service Worker to cache the JSON and static assets so the app works offline in the Bangkok BTS underground.
- [ ] Deploy to Vercel and run Lighthouse audits (Target: 100/100/100/100).
