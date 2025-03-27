from agent.agent_runner import run_agent

if __name__ == "__main__":
    print("🧠 Productivity Agent is ready.")
    query = input("Ask something: ")
    run_agent(query)
