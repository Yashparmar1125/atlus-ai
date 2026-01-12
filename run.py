from orchestrator.orchestrator import Orchestrator


orchestrator = Orchestrator()
response = orchestrator.run("I want to build a web application with a database and a user authentication system and a chatbot")
print(response)