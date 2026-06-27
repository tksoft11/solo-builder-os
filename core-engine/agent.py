import os
import sys
import json
import time
from colorama import init, Fore, Style
from openai import OpenAI
from tools import TOOLS_SCHEMA, execute_tool_call

init(autoreset=True)

class AutonomousAgent:
    def __init__(self, role_prompt: str, max_iterations: int = 15):
        if not os.environ.get("OPENAI_API_KEY"):
            print(Fore.RED + "Error: OPENAI_API_KEY is not set.")
            sys.exit(1)
        
        self.client = OpenAI()
        self.model = "gpt-4o"
        self.max_iterations = max_iterations
        self.messages = [
            {"role": "system", "content": f"{role_prompt}\n\nYou are an autonomous agent capable of using tools. Think step-by-step. If you encounter an error, observe it and self-correct."}
        ]

    def run(self, task: str):
        print(Fore.CYAN + Style.BRIGHT + f"\n🚀 Task Initialized: {task}\n")
        self.messages.append({"role": "user", "content": task})

        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            print(Fore.YELLOW + f"--- Iteration {iteration} ---")
            
            # Step 1: Brainstorming (Thought)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOLS_SCHEMA,
                tool_choice="auto",
                temperature=0.2
            )
            
            message = response.choices[0].message
            
            # Print Agent's thinking
            if message.content:
                print(Fore.MAGENTA + f"\n🧠 Thought:\n{message.content}")
                
            self.messages.append(message)

            # Step 2: Action (Tool Execution)
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    print(Fore.BLUE + f"🛠️  Action: {name}({json.dumps(args)})")
                    
                    # Execute tool
                    tool_result = execute_tool_call(name, args)
                    
                    print(Fore.GREEN + f"👁️  Observation:\n{tool_result[:500]}..." if len(tool_result) > 500 else Fore.GREEN + f"👁️  Observation:\n{tool_result}")
                    
                    # Append result back to messages
                    self.messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": tool_result
                    })
            else:
                # No more tools to call, task is complete
                print(Fore.CYAN + Style.BRIGHT + "\n✅ Task Complete!")
                return message.content
                
            time.sleep(1) # Rate limit protection

        print(Fore.RED + "\n❌ Max iterations reached without completing the task.")
        return "Failed to complete within iteration limit."

if __name__ == "__main__":
    print(Fore.CYAN + "=== Solo Builder OS: Autonomous Core Engine ===")
    
    with open("../agents/code-planner.md", "r", encoding="utf-8") as f:
        architect_prompt = f.read()

    agent = AutonomousAgent(role_prompt=architect_prompt)
    
    print("Welcome! The Autonomous Code Planner is ready.")
    user_task = input("What should I build? (e.g., 'Initialize a Next.js project in the ./demo folder')\n> ")
    
    agent.run(user_task)
