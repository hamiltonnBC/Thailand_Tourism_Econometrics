# Dashboard Architecture

## Overview

This is a static React dashboard built for displaying econometrics project data and analysis for Thailand Tourism. The application is built with modern web technologies and follows atomic component design principles.

## Tech Stack

- **React 18** - UI library for building component-based interfaces
- **TypeScript** - Type-safe JavaScript for better developer experience and fewer runtime errors
- **Vite** - Fast build tool and dev server with hot module replacement
- **Chakra UI v3** - Component library for consistent, accessible UI design
- **Emotion** - CSS-in-JS library used by Chakra UI

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.tsx      # Top header with project title
│   └── Navigation.tsx  # Left sidebar navigation
├── pages/              # Page-level components with sub-navigation
│   ├── Overview.tsx    # Overview page with Synopsis, Our Journey, Literature Review tabs
│   └── DataExploration.tsx  # Data page with Visualizations, Data Notes tabs
├── App.tsx             # Main app component with routing logic
├── main.tsx            # Entry point with Chakra Provider
└── index.css           # Global CSS reset

```

## Architecture Principles

### Component Reusability

The application follows atomic design principles:

1. **Atomic Components** (`components/`)
   - `Header.tsx` - Displays project title and subtitle, used once at the top
   - `Navigation.tsx` - Sidebar navigation, receives active tab state and change handler as props

2. **Page Components** (`pages/`)
   - Each major section (Overview, Data Exploration, etc.) is a separate page component
   - Pages implement their own sub-navigation tabs using the same pattern
   - Sub-tabs follow consistent styling and interaction patterns

### State Management

- **Main Navigation State**: Managed in `App.tsx` using `useState`
- **Sub-Navigation State**: Each page component manages its own sub-tab state independently
- Props are passed down for communication between parent and child components

### Styling Approach

- Uses Chakra UI's Box component system for layout
- Consistent color palette:
  - Dark slate (`#1e293b`) for primary text and active states
  - Gray (`#64748b`) for secondary text
  - Light backgrounds (`#f8fafc`, `white`)
- Hex colors used directly for precise control
- Consistent spacing and transitions across all interactive elements

### Layout Structure

```
┌─────────────────────────────────────────┐
│           Header (fixed)                │
├──────────┬──────────────────────────────┤
│          │                              │
│  Sidebar │     Main Content Area        │
│   Nav    │   ┌──────────────────────┐   │
│ (fixed)  │   │  Page Component      │   │
│          │   │  - Sub-tabs          │   │
│          │   │  - Content           │   │
│          │   └──────────────────────┘   │
│          │                              │
└──────────┴──────────────────────────────┘
```

- **Header**: Fixed at top, spans full width
- **Sidebar**: Fixed left sidebar (250px wide)
- **Content**: Scrollable main area with left margin to accommodate sidebar

## Navigation Structure

### Main Navigation (Sidebar)
1. Overview
2. Data Exploration
3. The Model
4. Results
5. Conclusions
6. Team
7. References

### Sub-Navigation

**Overview Page:**
- Synopsis
- Our Journey
- Literature Review

**Data Exploration Page:**
- Visualizations
- Data Notes

## Component Communication Pattern

```typescript
// Parent (App.tsx)
const [activeTab, setActiveTab] = useState<TabId>('overview')

<Navigation 
  activeTab={activeTab} 
  onTabChange={setActiveTab} 
/>

// Child (Navigation.tsx)
interface NavigationProps {
  activeTab: TabId
  onTabChange: (tab: TabId) => void
}
```

This pattern is reused in page components for sub-navigation, maintaining consistency throughout the app.

## Type Safety

TypeScript is used throughout for type safety:
- `TabId` type defines valid main navigation tabs
- Each page defines its own sub-tab types (e.g., `OverviewTab`, `DataExplorationTab`)
- Props interfaces ensure correct data flow between components

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Future Extensibility

The architecture makes it easy to:
- Add new main navigation tabs by updating `Navigation.tsx` and `App.tsx`
- Add new sub-tabs within existing pages by updating the respective page component
- Create new page components following the established pattern
- Maintain consistent styling by reusing the same Chakra UI patterns
