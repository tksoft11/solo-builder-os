# PRD Writer Output (World-Class Edition)

## 1. The Amazon PR/FAQ

**Press Release (Target Date: August 2026)**
**AUSTIN, TX** — Today, a new intelligence tool called "NicheTrend Radar" launched, promising to save affiliate marketers 10 hours of research a week. Traditional SEO tools overwhelm users with millions of keywords, requiring deep expertise to find a profitable product. NicheTrend Radar flips the model. Instead of a search engine, it's a "Done-For-You" weekly dashboard. By tracking search velocity across Google and combining it with Amazon product APIs, the Radar algorithm isolates the Top 10 "Surge Products" in highly specific niches (starting with Specialty Coffee and Home Office). Marketers no longer have to hunt for trends; the exact product links, difficulty scores, and target keywords are handed to them on a silver platter every Monday morning.

**FAQ for the User**
- *Q: Can I track my own custom niche?* A: Not in V1. We manually curate the most profitable niches to ensure the data quality remains exceptionally high.
- *Q: How often is the Top 10 list updated?* A: Every Monday at 08:00 AM EST to align with your weekly campaign planning.
- *Q: How do you define a "Surge Product"?* A: A product showing >300% search volume growth over a 30-day period with an SEO difficulty score of less than 30.

## 2. Success Metrics (The North Star)
- **North Star Metric:** "Campaigns Launched" (Tracked via clicks on the "Copy Keyword & Amazon Link" button).
- **Monetization Metric:** Free-to-Paid Conversion Rate (Target > 5%).
- **Engagement Metric:** Weekly Active Users (WAU) reading the Monday report.

## 3. MECE User Stories & Acceptance Criteria

### Epic 1: The Weekly Intelligence Dashboard
- **Story:** As a niche marketer, I want to see the Top 10 emerging products immediately when I log in, so I can pick a winner in under 5 minutes.
- **Acceptance Criteria 1.1:** The dashboard must display exactly 10 product cards. No pagination. No endless scrolling.
- **Acceptance Criteria 1.2:** Each card MUST display: Product Name, Product Image, "Surge Score" (Growth %), and Target SEO Keyword.
- **Acceptance Criteria 1.3:** Each card MUST have a one-click button that copies the Amazon ASIN and Target Keyword to the clipboard.

### Epic 2: The Data Ingestion Engine (Admin/Backend)
- **Story:** As the system admin, I want the system to aggregate raw keyword data and output a curated JSON list, so I don't have to manually build the dashboard.
- **Acceptance Criteria 2.1:** The backend cron job runs every Sunday night.
- **Acceptance Criteria 2.2:** The script ingests a predefined list of 500 niche keywords, queries a search volume API (e.g., DataForSEO), and sorts by MoM (Month-over-Month) growth.
- **Acceptance Criteria 2.3:** The top 10 results are saved to a static `current-trends.json` file.

## 4. Edge Case Matrix

| Scenario | System Behavior |
| :--- | :--- |
| API Failure (Search Volume API goes down on Sunday). | System falls back to the previous week's `current-trends.json` and alerts the Admin via webhook. User sees a "Historical Data" tag. |
| Two products have the exact same Surge Score. | Tie-breaker goes to the product with the lower SEO difficulty (less competition). |
| A product goes out of stock on Amazon. | The ingestion script pings the Amazon API; if out of stock, it drops the item and pulls the #11 item into the Top 10. |

## 5. The Iron Triangle (Out of Scope for V1)
- **NO Real-time Dashboards.** Data is updated weekly. Real-time creates anxiety and requires expensive server compute.
- **NO Competitor Tracking.** We don't track what other affiliates are doing.
- **NO Complex Filtering.** Users get 10 items. They cannot filter by price, weight, or color. Curation is the product.
