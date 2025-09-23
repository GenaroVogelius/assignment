# Code Reviewer Frontend

A modern React-based frontend application for code review functionality, built with a focus on clean architecture and user experience.

## Tech Stack

### Core Framework

- **React 19** - Modern React with latest features
- **TypeScript** - Type-safe development
- **Vite** - Fast build tool and development server

### UI & Styling

- **Tailwind CSS 4** - Utility-first CSS framework
- **shadcn/ui** - High-quality, accessible UI components built on Radix UI
- **Lucide React** - Beautiful & consistent icon toolkit

### State Management & Data Fetching

- **TanStack Query (React Query)** - Powerful data synchronization for React
- **Zustand** - Lightweight state management with persistence
- **Zod** - TypeScript-first schema validation

### Routing & Navigation

- **React Router DOM** - Declarative routing for React

### Development Tools

- **ESLint** - Code linting and formatting
- **TypeScript ESLint** - TypeScript-specific linting rules

## Project Structure

```
src/
├── api/                    # API layer and data fetching
│   ├── Auth/              # Authentication API calls
│   └── Reviews/           # Review-related API calls
├── components/            # Reusable UI components
│   ├── ui/               # shadcn/ui components
│   ├── CodeEditor/       # Code editor component
│   ├── Header/           # Application header
│   └── ...               # Other shared components
├── features/             # Feature-based modules
│   ├── AnalyticsDashboard/  # Analytics and reporting
│   ├── auth/             # Authentication features
│   ├── CodeSubmissionForm/ # Code submission functionality
│   └── ReviewDashboard/  # Main review dashboard
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions and configurations
├── pages/                # Page-level components
├── stores/               # Zustand state stores
└── styles/               # Global styles and CSS
```

## Architecture

### Feature-Based Architecture

The application follows a feature-based architecture where each major functionality is organized into its own module:

- **Authentication Module**: Handles user login, registration, and session management
- **Review Dashboard**: Main interface for viewing and managing code reviews
- **Code Submission**: Interface for submitting code for review
- **Analytics Dashboard**: Reporting and analytics features

### State Management Strategy

- **Zustand**: Global application state (authentication, user preferences)
- **TanStack Query**: Server state management and caching
- **React Hook Form**: Form state management
- **Local Component State**: Component-specific state using React hooks

### API Layer

- Centralized API calls organized by feature
- Type-safe API interfaces using TypeScript
- Automatic caching and synchronization with TanStack Query

## Getting Started

### Prerequisites

- Node.js (version 18 or higher)
- npm or pnpm (recommended)

### Installation

1. Navigate to the frontend directory:

```bash
cd code_reviewer_frontend
```

2. Install dependencies:

```bash
npm install
# or
pnpm install
```

### Development

Start the development server:

```bash
npm run dev
# or
pnpm dev
```

The application will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
# or
pnpm build
```

### Preview Production Build

```bash
npm run preview
# or
pnpm preview
```

## Key Features

- **Modern UI Components**: Built with shadcn/ui for consistent, accessible design
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Type Safety**: Full TypeScript coverage for better development experience
- **State Persistence**: User authentication state persists across sessions
- **Code Syntax Highlighting**: Built-in code editor with syntax highlighting
- **Real-time Updates**: Efficient data synchronization with TanStack Query
- **Form Validation**: Robust form handling with React Hook Form and Zod

## Development Guidelines

- Use TypeScript for all new components and functions
- Follow the feature-based folder structure
- Implement proper error handling and loading states
- Use TanStack Query for all API calls
- Maintain consistent styling with Tailwind CSS classes
- Write accessible components following shadcn/ui patterns

## Deployment

### GitHub Pages

The application is configured for deployment on GitHub Pages with automatic CI/CD:

- **Automatic deployment**: Pushes to the `main` branch trigger automatic deployment
- **GitHub Actions workflow**: Located in `.github/workflows/deploy.yml`
- **Production URL**: https://GenaroVogelius.github.io/assignment

#### Manual Deployment

You can also deploy manually using the included script:

```bash
npm run deploy
```

This will build the project and deploy it to the `gh-pages` branch.

#### Configuration

The deployment is configured with:

- **Base path**: `/assignment/` (configured in `vite.config.ts`)
- **Homepage**: `https://GenaroVogelius.github.io/assignment` (configured in `package.json`)
- **Build output**: `dist/` directory
- **Dependencies**: `gh-pages` package for manual deployment
