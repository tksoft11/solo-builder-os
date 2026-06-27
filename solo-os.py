import os
import sys
import time
import json
try:
    import openai
except ImportError:
    print("Please install the openai library: pip install openai")
    sys.exit(1)

# Ensure API key is set
if not os.environ.get("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is not set.")
    print("Usage: export OPENAI_API_KEY='your-key-here'")
    sys.exit(1)

client = openai.OpenAI()

def load_agent_prompt(agent_filename):
    """Loads the system prompt for an agent from the markdown file."""
    filepath = os.path.join("agents", agent_filename)
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Could not find {filepath}. Ensure you are running this from the project root.")
        sys.exit(1)

def run_agent(agent_name, prompt_file, user_input, context=""):
    """Runs a specific agent via OpenAI API."""
    print(f"\n[{agent_name}] is thinking...")
    system_prompt = load_agent_prompt(prompt_file)
    
    full_prompt = f"{system_prompt}\n\n--- CURRENT CONTEXT ---\n{context}\n\n--- USER INPUT ---\n{user_input}"
    
    response = client.chat.completions.create(
        model="gpt-4o", # Use GPT-4o for complex reasoning
        messages=[
            {"role": "system", "content": "You are a World-Class AI Agent executing a specific role in the Solo Builder OS."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content

def main():
    print("=============================================")
    print("🚀 Welcome to Solo Builder OS CLI Automation 🚀")
    print("=============================================")
    
    idea = input("What is your raw product idea? \n> ")
    if not idea.strip():
        print("Idea cannot be empty. Exiting.")
        sys.exit(1)

    print("\nStarting the Idea-to-PRD Workflow...")
    
    # 1. Product Strategist
    strategy = run_agent("Product Strategist", "product-strategist.md", idea)
    print("\n" + "="*40)
    print("🎯 Product Strategist Output:")
    print("="*40)
    print(strategy)
    
    if input("\nDo you approve this strategy? (y/n): ").lower() != 'y':
        print("Workflow aborted by user. Please refine your idea and try again.")
        sys.exit(0)

    # 2. Market Researcher
    market = run_agent("Market Researcher", "market-researcher.md", "Please analyze the market based on this strategy.", context=strategy)
    print("\n" + "="*40)
    print("🕵️ Market Researcher Output:")
    print("="*40)
    print(market)
    
    if input("\nDo you approve this research? (y/n): ").lower() != 'y':
        print("Workflow aborted by user.")
        sys.exit(0)

    # 3. PRD Writer
    prd = run_agent("PRD Writer", "prd-writer.md", "Please write a comprehensive PRD.", context=f"{strategy}\n{market}")
    print("\n" + "="*40)
    print("📝 PRD Writer Output:")
    print("="*40)
    print(prd)
    
    # Save the final PRD
    with open("final-prd.md", "w", encoding="utf-8") as f:
        f.write(prd)
        
    print("\n✅ Workflow complete! Your World-Class PRD has been saved to 'final-prd.md'.")
    print("Next Step: Hand this PRD over to the Code Planner agent or your IDE (Cursor/Windsurf) to begin building!")

if __name__ == "__main__":
    main()
