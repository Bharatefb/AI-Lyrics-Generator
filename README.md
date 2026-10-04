# AI-Lyrics-Generator

What I Built

I built AI Lyrics Generator, a local AI-powered web application that helps a friend turn an idea, topic, or feeling into an original song.

The goal was simple: instead of struggling with a blank page or needing access to a paid AI service, my friend can enter a few details such as:

🎵 Song name or topic

🎸 Genre

😊 Mood

🌍 Language

📝 Number of verses

The application then generates an original song structure with sections such as verses, chorus, bridge, and final chorus.

The project runs locally using Qwen2.5-Coder 3B through Ollama, with a FastAPI backend and a lightweight HTML/CSS/JavaScript frontend.

The main problem I'm solving is making AI-assisted songwriting simple, accessible, and local.

Demo

🎥 Demo Video: Coming soon

🌐 Live Demo: Coming soon

The application can be run locally with Ollama, so users don't need a cloud AI API to generate lyrics.

Code GitHub Repository

AI-Lyrics-Generator

https://github.com/Bharatefb/AI-Lyrics-Generator

The repository contains the complete frontend, FastAPI backend, prompt logic, and setup instructions.

Project Architecture ┌─────────────────────┐ │ Browser │ │ │ │ Song / Topic │ │ Genre │ │ Mood │ │ Language │ │ Verse Count │ └──────────┬──────────┘ │ HTTP POST │ ▼ ┌─────────────────────┐ │ FastAPI │ │ │ │ /generate │ └──────────┬──────────┘ │ ▼ ┌─────────────────────┐ │ Ollama │ │ │ │ qwen2.5-coder:3b │ └──────────┬──────────┘ │ ▼ ┌─────────────────────┐ │ Generated Lyrics │ └──────────┬──────────┘ │ ▼ ┌─────────────────────┐ │ Browser │ │ │ │ [Verse 1] │ │ [Chorus] │ │ [Verse 2] │ │ [Bridge] │ │ [Final Chorus] │ └─────────────────────┘

How I Built It

The project is built around open-weight AI and local inference.

AI Model

I use:

Qwen2.5-Coder 3B

through:

Ollama

The model runs locally on the user's machine rather than requiring a remote AI API.

Backend

The backend is written in:

Python

FastAPI

Pydantic

Requests

Uvicorn

The frontend sends the user's song requirements to the FastAPI /generate endpoint.

FastAPI then builds a structured prompt and sends it to the local Ollama API.

Browser ↓ POST /generate ↓ FastAPI ↓ Ollama ↓ qwen2.5-coder:3b ↓ Generated lyrics ↓ Browser

Frontend

The frontend uses standard web technologies:

HTML

CSS

JavaScript

No large frontend framework is required, keeping the project simple and easy to understand.

Prompt Design

Instead of simply asking the model:

Write a song about summer.

the application provides structured information:

Song/topic: Summer Love Genre: Pop Mood: Happy Language: English Number of verses: 3

The model is instructed to create completely original lyrics and organize them into a recognizable song structure.

For example:

[Verse 1]

...

[Pre-Chorus]

...

[Chorus]

...

[Verse 2]

...

[Bridge]

...

[Final Chorus]

...

Local AI

One of the key parts of the project is that the AI inference happens locally.

After installing Ollama and the model:

ollama pull qwen2.5-coder:3b

the application can communicate with the local Ollama API.

This means the basic application does not require an OpenAI, Anthropic, Gemini, or other paid cloud AI API.