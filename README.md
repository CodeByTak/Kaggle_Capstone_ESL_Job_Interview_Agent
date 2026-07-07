# Kaggle_Capstone_ESL_Job_Interview_Multi_Agent
 Practice Makes Confident: A Multi-Agent ESL Interview Coach.  Helping English-language learners rehearse high-stakes conversations — with silent correction, honest guardrails, and zero real-world advice given by mistake.

ESL Interview Coach — A Multi-Agent Practice System

Kaggle Capstone Submission — AI Agents: Intensive Vibe Coding Course with Google
Track: Agents for Good

Helping English-language learners rehearse high-stakes conversations — with silent correction, honest guardrails, and zero real-world advice given by mistake.




The Problem

Millions of people navigate life-changing conversations in a language they're still learning — most urgently, a job interview. Traditional language apps teach vocabulary and grammar in isolation, but rarely let learners practice holding a real conversation under real pressure. Correcting a learner mid-sentence during practice breaks their fluency and confidence exactly when they need to build both.

This project builds a mock job-interview practice partner that corrects silently, stays encouraging, and — critically — knows the difference between a practice scenario and a real question.

Why Agents

This task is naturally split across several different jobs that need to happen at different times, sharing memory of the same conversation:


Something has to stay in character as an interviewer, holding a natural conversation.
Something has to silently notice language errors without interrupting the flow — a different task running in the background.
Something has to step out of the roleplay entirely afterward and turn errors into useful feedback.
Something has to recognize when the practice frame breaks — when a learner accidentally asks a real question — and respond honestly instead of staying in character.


A single prompt trying to do all of this at once is fragile. Splitting it into cooperating agents, with tool logic running independently of the agents, is what makes each piece simple and reliable.

Architecture

A root orchestrator agent, built with Google's Agent Development Kit (ADK), delegates to two specialized sub-agents:


InterviewCoach — plays a hiring manager conducting a mock interview. Asks one question at a time, waits for the answer, and silently logs any grammar, word-choice, or register errors without ever breaking character.
ProgressCoach — activated when the learner asks for feedback. Retrieves everything logged during the interview, groups errors into patterns, and delivers 2–3 prioritized, encouraging corrections with real examples.


Both agents connect to a standalone MCP server (interview_mcp_server.py) that exposes two tools — log_error and get_error_summary — over the Model Context Protocol, via ADK's MCPToolset. This decouples the tool logic from the agent logic entirely: the same server could be reused by a different agent framework, swapped for a database-backed version, or hosted remotely, without touching the agent code.

A safety guardrail (before_model_callback) intercepts every message before it reaches the model, detecting when a learner has stepped out of practice and asked something real ("is this a real job offer?"). It breaks character honestly rather than relying on the model's judgment in the moment.

Concepts demonstrated

ConceptWhereMulti-agent system (ADK)root_agent with sub_agents=[interview_agent, progress_agent]MCP Serverinterview_mcp_server.py, connected via MCPToolsetSecurity / guardrailbreakout_guardrail, a before_model_callback

Project Structure

├── esl_interview_agent.ipynb     # Main notebook: agents, orchestration, demo
├── interview_mcp_server.py       # Standalone MCP server (log_error, get_error_summary)
├── esl_coach_architecture.svg    # Architecture diagram
├── demo_transcript.md            # Full annotated demo transcript
└── README.md

Setup Instructions

Prerequisites:


Python 3.10+
A free Gemini API key from Google AI Studio


1. Install dependencies:

bashpip install google-adk

2. Set your API key:

pythonimport os
os.environ["GOOGLE_API_KEY"] = "your-key-here"

(If running in Kaggle, use Kaggle Secrets instead of hardcoding the key.)

3. Run the notebook cells in order. The notebook is structured as a linear sequence:


Tool functions / MCP server file
Guardrail callback
MCP toolset connection
InterviewCoach agent
ProgressCoach agent
Root orchestrator
Runner setup
Demo conversation


4. Run the MCP server standalone (optional, for testing):

bashpython interview_mcp_server.py

Note on rate limits: the Gemini free tier enforces both per-minute and per-day request caps. The demo includes a retry-with-backoff wrapper (send_with_retry) to handle per-minute limits gracefully during a live run.

Demo

See demo_transcript.md for a full annotated walkthrough of a practice session, showing:


Natural interview flow with silently-logged grammar errors
The safety guardrail catching a real-world question mid-roleplay
The final grouped, encouraging feedback report


What I'd Add With More Time


Cross-session memory to track recurring errors across multiple sessions
Additional scenario skills (parent-teacher conference, doctor visit, investor pitch) reusing the same architecture
A richer, database-backed MCP server with real interview question banks
A formal ADK evaluation suite with adversarial test cases
Deployment to Cloud Run using ADK's built-in deployment tooling


Why This Matters

Confidence in a second language isn't just linguistic — it's economic and civic. A learner who can practice a real job interview without fear of judgment, and who can trust the system will never quietly slip real advice into a fictional scene, gets something closer to what a human tutor offers: honest correction, without the anxiety of being corrected in the moment it counts.


Built for Kaggle's AI Agents: Intensive Vibe Coding Capstone using Google's Agent Development Kit (ADK), the Gemini API, and the Model Context Protocol (MCP).
