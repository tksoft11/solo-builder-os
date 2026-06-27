# UX & Code Planner Output (World-Class Edition)

## Part 1: UX Planner (Behavioral Design)

### 1. The Fogg Behavior Model Application (B = MAP)
- **Motivation:** User wants to make money / find a profitable niche (High).
- **Ability:** We must eliminate the friction of "Data Analysis" (High ability = zero thinking required).
- **Prompt:** A weekly email digest: "Your 10 Coffee Trends for the Week are Ready."

### 2. Information Architecture (IA)
The dashboard is an anti-analytics tool. No graphs. No charts. 

1. **The Header:** "Top 10 Emerging Trends for [Niche]" + "Updated: Monday 08:00 AM".
2. **The Trend Feed (The Core):** A clean masonry grid or vertical list of exactly 10 cards.
3. **The Anatomy of a Trend Card:**
   - **Visual:** Clean product image (white background).
   - **The Signal (Top Left):** `+340% Surge` (in a bright green, adrenaline-inducing badge).
   - **The Keyword:** "Cold Brew Nitro Keg"
   - **The Friction-Killer:** A single massive button `[Copy Keyword & Product Link]`.

### 3. Cognitive Load Reduction
By hard-limiting the list to exactly 10 items, we defeat **Analysis Paralysis** (Hick's Law). If we give them 100 items, they will analyze. If we give them 10, they will act. We hide the raw search volume numbers; we only show the *Growth Velocity* (percentage), which is the only metric that matters for being "early."

---

## Part 2: Code Planner (Staff-Level Architecture)

### 1. System Architecture (The "Cron & Cache" Monolith)
This is a read-heavy application where data only changes once a week. We do not need a real-time database connection for the frontend.

- **Frontend:** Next.js (App Router).
- **Rendering:** Incremental Static Regeneration (ISR) with a 7-day cache. The site is physically rebuilt every Sunday night. Load times will be < 0.5s.
- **Backend (The Data Engine):** Node.js script triggered by GitHub Actions (Cron Job).
- **Data Storage:** SQLite (Turso) or simply static JSON files deployed to AWS S3 / Vercel Blob.
- **Authentication:** Supabase Auth (for the Freemium model).

### 2. The Data Pipeline (The "Brain")
1. **Source:** We maintain a seed list of 500 keywords per niche (e.g., `coffee-keywords.csv`).
2. **Fetch:** Cron job runs. Hits DataForSEO API for search volume. Hits Amazon Product Advertising API for top product ASINs.
3. **Process:** Calculate `(Current Month Vol - Last Month Vol) / Last Month Vol * 100`. Sort descending. Slice top 10.
4. **Publish:** Overwrite `trends.json`. Trigger Vercel webhook to rebuild the Next.js site.

### 3. SOLID Principles in Practice
- **Dependency Inversion Principle (DIP):** The `TrendAnalyzer` class does not depend directly on the `DataForSEOApi`. It depends on an interface `ISearchVolumeProvider`. If DataForSEO gets too expensive, we swap it for the `SemrushApi` class without breaking the analyzer logic.

### 4. Implementation Phases (GitHub Issues)

**Phase 1: The Pipeline (Backend First)**
- [ ] Write Python/Node script to read CSV of seed keywords.
- [ ] Integrate mock API for Search Volume to test the `(M2-M1)/M1` sorting logic.
- [ ] Export output to `curated-trends.json`.

**Phase 2: The Dashboard (Frontend)**
- [ ] Init Next.js App Router.
- [ ] Build the `TrendCard` component strictly adhering to the UX Planner's anatomy.
- [ ] Build the ISR page that maps over `curated-trends.json`.

**Phase 3: The Paywall (Supabase)**
- [ ] Integrate Supabase Auth.
- [ ] Logic: Unauthenticated users see Items #1 to #3. Items #4 to #10 are blurred out with a "Log in to see all 10" CTA.
