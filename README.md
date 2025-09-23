# AI-Powered Code Review System

A full-stack application that leverages artificial intelligence to provide automated code reviews. The system consists of a FastAPI backend implementing Clean Architecture principles and a modern React frontend with a focus on user experience and accessibility.

## 🚀 Live Demo

**Frontend**: [https://reviewer.simv.site](https://reviewer.simv.site)  
**Backend API Docs**: [https://ai.simv.site/docs](https://ai.simv.site/docs)

## 📋 Table of Contents

- [Features](#-features)
- [Architecture Overview](#-architecture-overview)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Development Setup](#-development-setup)
- [API Documentation](#-api-documentation)
- [Architecture Decisions](#-architecture-decisions)
- [Future Enhancements](#-future-enhancements)
- [Contributing](#-contributing)

## ✨ Features

### Core Functionality

- **AI-Powered Code Reviews**: Automated code analysis using advanced language models
- **User Authentication**: Secure JWT-based authentication system
- **Code Submission**: Intuitive interface for submitting code for review
- **Review Dashboard**: Comprehensive view of all code reviews with filtering and search

### Technical Features

- **Clean Architecture**: Backend follows Clean Architecture and SOLID principles for maintainability
- **Type Safety**: Full TypeScript coverage across frontend and backend
- **Responsive Design**: Mobile-first approach with modern UI components
- **Database Flexibility**: Support for both any database
- **Rate Limiting**: Built-in protection against abuse
- **Comprehensive Testing**: Automated test suite

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐       ┌─────────────────┐
│  React Frontend │    │ FastAPI Backend │       │                 │
│                 │    │                 │       │                 │
│ • shadcn/ui     │◄──►│ • Clean Arch    │◄───►  │    Database     │
│ • TanStack Query│    │ • JWT Auth      │       │                 │
│ • Zustand       │    │ • Rate Limiting │       │                 │
└─────────────────┘    └─────────────────┘       └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   GitHub Pages  │    │  GitHubRegistry │
│   Deployment    │    │  Private VPS    │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
```

## 🛠️ Tech Stack

### Backend (AI Microservice)

- **Framework**: FastAPI 0.115.12
- **Architecture**: Clean Architecture with dependency injection
- **Database**: MongoDB (Beanie ODM) / PostgreSQL support
- **Authentication**: JWT with bcrypt password hashing
- **AI Integration**: PraisonAI library for agnostic integrations with LLMs
- **Testing**: pytest with async support
- **Development**: Docker Dev Containers
- **Deployment**: GitHub Registry and VPS

### Frontend (Code Reviewer)

- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 7.1.2
- **UI Library**: shadcn/ui (Radix UI primitives)
- **Styling**: Tailwind CSS 4
- **State Management**: Zustand + TanStack Query
- **Forms**: React Hook Form with Zod validation
- **Deployment**: GitHub Pages with automatic CI/CD

## 🚀 Quick Start

### Prerequisites

- **Backend**: Docker, Docker Compose, VS Code with Dev Containers extension
- **Frontend**: Node.js 18+, npm or pnpm

### 1. Clone the Repository

```bash
git clone <repository-url>
cd assignment
```

### 2. Backend Setup

```bash
cd AI
```

📖 **See**: [AI/README.md](./AI/README.md) for detailed backend setup instructions.

### 3. Frontend Setup

```bash
cd code_reviewer_frontend
```

📖 **See**: [code_reviewer_frontend/README.md](./code_reviewer_frontend/README.md) for detailed frontend setup instructions.

## 🏛️ Architecture Decisions

### Why Clean Architecture?

I chose Clean Architecture for the backend because it provides:

- **🔄 Technology Independence**: Swap frameworks/databases without touching business logic
- **🧪 Testability**: Test core functionality without external dependencies
- **🔧 Maintainability**: Changes in one layer don't cascade through the system
- **👥 Team Collaboration**: Different teams can work on different layers simultaneously
- **📈 Long-term Flexibility**: Adapt components without major rewrites

### Frontend Architecture

The frontend follows a feature-based architecture with:

- **Separation of Concerns**: Clear boundaries between UI, business logic, and data
- **Reusable Components**: shadcn/ui components for consistency
- **Type Safety**: Full TypeScript coverage
- **Modern Patterns**: React 19 features, custom hooks, and efficient state management

## 🔮 Future Enhancements

### 1. Analytics Dashboard

Complete the analytics dashboard implementation:

- **Backend**: Interface for Analyzer, concrete ReviewAnalyzer implementation
- **Use Case**: Trigger analysis when review status changes
- **Database**: Store analytics data for efficient retrieval
- **API**: Endpoint to expose analytics data
- **Frontend**: Connect to analytics API and visualize data

### 2. Background Task Processing

Upgrade from basic FastAPI background tasks to more robust solutions:

- **Celery + RabbitMQ**: For production-grade task processing
- **Inngest**: Modern alternative for event-driven workflows
- **Reliability**: Ensure tasks aren't lost on server crashes

### 3. Enhanced User Experience

Improve frontend polish and usability:

- **Dark Mode**: Theme switching capability
- **User Feedback**: Better error messages and success notifications
- **Navigation**: Improved routing and page transitions
