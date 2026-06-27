# Workflow: Idea to PRD

## Objective
Help a solo founder transform a rough, unstructured idea into a decision-quality Product Requirements Document (PRD).

## Inputs
- Product idea
- Intended user/audience
- Problem statement
- Time/resource constraints

## Recommended Agents
You will act as the orchestrator. Copy the prompts below and feed them to the respective AI agents (in separate chats or one continuous context) to progress through the workflow.
1. **Product Strategist**
2. **Market Researcher**
3. **PRD Writer**

## Steps

### Step 1: Clarify Product Idea (Product Strategist)
**Prompt to AI:**
> "Act as the Product Strategist. I have an idea for [Insert Idea]. The intended audience is [Insert Audience] and the problem they face is [Insert Problem]. I want to build this in [Insert Time/Resource Constraints]. Please help me clarify this idea, define the exact problem, recommend an MVP scope, and list success hypotheses."

**Feedback Control:**
- **Review:** Does the MVP scope sound achievable? Is the problem statement clear?
- **Iterate:** If it's too broad, ask the AI to narrow it down before moving to Step 2.

### Step 2: Assess Assumptions and Market Alternatives (Market Researcher)
**Prompt to AI:**
> "Act as the Market Researcher. Based on the product summary and problem definition above, analyze the competitive landscape. Provide a competitor table of 3-5 alternatives, identify positioning gaps, validate user pain assumptions, and suggest specific differentiation opportunities for this MVP."

**Feedback Control:**
- **Review:** Are the differentiation opportunities realistic for a solo founder?
- **Iterate:** If the competitors are wrong, provide specific competitors for the AI to analyze again.

### Step 3: Draft PRD (PRD Writer)
**Prompt to AI:**
> "Act as the PRD Writer. Using the outputs from the Product Strategist and the Market Researcher, draft a comprehensive PRD using our standard template. Ensure the user stories, flows, and MVP requirements are specific and actionable for a solo developer."

**Feedback Control:**
- **Review:** Read through the PRD. Is anything ambiguous? Are non-goals explicitly listed?
- **Iterate:** Ask the AI to rewrite specific sections that lack clarity before finalizing.

### Step 4: Review with PRD Checklist (Human + AI)
Review the generated PRD against the evaluation checklist. If anything is vague, ask the PRD Writer to refine it.
**Prompt to AI (if refinement is needed):**
> "The user stories in section X are too vague. Please rewrite them to be more specific and include acceptance criteria."

## Outputs
- Completed PRD
- Top risks and assumptions
- Open questions
- Clear MVP boundary

## Done Criteria
- PRD is specific enough to generate implementation tasks.
- User and pain points are clearly defined.
- Explicit non-goals are included to prevent scope creep.
