from agent.agent_runner import run_agent

if __name__ == "__main__":
    print("🧠 Productivity Agent is ready.")
    
    try:
        while True:
            query = input("\nAsk something (or type 'exit' to quit): ")
            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye! 👋")
                break
                
            # Consume the iterator to display all responses
            for _ in run_agent(query):
                pass
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")