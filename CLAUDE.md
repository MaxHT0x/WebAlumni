# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

WebAlumni is a Flask-based web application for processing and analyzing alumni data from Excel files. It provides data cleaning, normalization, and report generation capabilities with a focus on employment statistics and workplace analysis.

## Development Commands

### Running the Application
```bash
python3 app.py
```
The application runs on `http://127.0.0.1:5000/` by default.

### Python Environment Setup
```bash
python3 -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux  
source .venv/bin/activate

pip install -r requirements.txt
```

### Dependencies
- Flask 3.0.0 - Web framework
- pandas 2.1.0 - Data processing
- openpyxl 3.1.2 - Excel file handling
- xlsxwriter 3.1.2 - Excel report generation

## Architecture

### Core Components

**Flask Application (`app.py`)**
- Single-file Flask application (~1600 lines)
- Session-based data storage using in-memory dictionary
- File upload handling with validation
- Multiple report generation endpoints

**Data Processing Pipeline**
1. **File Upload**: Excel files uploaded to `uploads/` directory
2. **Data Loading**: `load_excel_data()` validates and processes Excel files with comprehensive validation
3. **Data Normalization**: Company names, employment status, gender values, and position titles are normalized
4. **Report Generation**: Multiple report types generated as Excel files in `generated_files/`

**Supported File Types**
- Alumni List files: Contains graduate data with employment information
- Banner files: University system exports with graduation data

### Key Data Processing Functions

**Company Name Normalization (`normalize_company_name()`)**
- Handles empty/null values with categorization
- Standardizes company aliases (e.g., "SNB" → "SAUDI NATIONAL BANK")
- Removes common corporate suffixes
- Returns standardized company names for analysis

**High Position Detection (`is_high_position()`)**
- Identifies C-suite, director, VP, and founder positions
- Returns normalized position titles for leadership analysis
- Uses regex patterns for flexible matching

**Status Cleaning (`clean_status()`)**
- Normalizes employment status values
- Handles case sensitivity and whitespace

**Gender Cleaning (`clean_gender()`)**
- Normalizes gender values with common variation handling
- Maps variations (M/Man/Gentleman → Male, F/Woman/Lady → Female)
- Returns standardized gender values for consistent processing

### Data Validation System

**Excel File Validation (`load_excel_data()`)**
- **Required Column Validation**: Checks for missing required columns based on file type
- **Student ID Format**: Validates IDs match pattern `^[0-9G]\d*$`
- **College Validation**: Validates against predefined college list with ⚠️ ALERT for invalid entries
- **Graduation Year Validation**: Validates against extracted or default year ranges
- **Current Status Validation**: Checks against 11 expected status values with ⚠️ ALERT for invalid entries
- **Gender Validation**: Validates against expected gender values ["Male", "Female"] with ⚠️ ALERT for invalid entries
- **Empty Field Detection**: Identifies empty/null values in critical fields (Gender, Status, College) with row numbers
- **Comprehensive Warnings**: Returns detailed validation messages with row references for debugging

**Expected Values**
- **Current Status**: 11 standard values including "Employed", "Unemployed", "Business owner", "New graduate", and a few others. 
- **Gender**: "Male", "Female" with normalization for common variations
- **Colleges**: 5 predefined college options

### Report Types

1. **QAA Reports** - Employment statistics by college/major (supports both Detailed and Simple modes)
2. **Alumni Lists** - Filtered contact lists by criteria
3. **Workplace Reports** - Company and position analysis
4. **Banner Integration** - Merges new graduates with existing alumni data

### QAA Report Modes

**Detailed Mode (Default)**
- Full employment statistics with major breakdowns
- Includes employment status analysis (Employed, Unemployed, Studying, etc.)
- Respects all filter options (Degree, Gender, Nationality)
- Generates comprehensive reports with employment percentages
- Creates detailed worksheets by college/year or combined views

**Simple Mode**
- Basic graduate counts with gender breakdown only
- Ignores ALL filter options except colleges and years
- Groups data by academic year (e.g., "2013-2014") regardless of graduation terms
- Creates one Excel tab per academic year
- Shows total graduates per college with "Gentlemen" and "Ladies" counts
- Includes "All years summary" tab with comprehensive overview across all years
- Nationality breakdown with Saudi/Non-Saudi categorization in summary tab
- Excludes majors, employment status, and all status information
- Case-insensitive data processing for robust gender detection
- Only includes colleges that have graduates for each year

**Simple Mode Implementation (`process_simple_mode_report()`)**
- Uses intelligent academic year extraction from graduation terms
- Handles multiple formats: "2013-2014", "2013-14", "2013"
- Normalizes text data (Gender_Normalized, College_Normalized) for case-insensitive processing
- Creates clean Excel reports with proper formatting and totals
- Filters out years with no data automatically
- Generates summary tab (`create_all_years_summary_tab()`) with three-section layout: colleges, gender, and nationality

### Frontend Architecture

**Single Page Application (~2700 lines)**
- Monolithic HTML template with embedded CSS (~950 lines) and JavaScript (~1100 lines)
- Modern responsive design using CSS custom properties (CSS variables)
- Tab-based navigation with dynamic content switching
- Real-time preview functionality with debounced API calls

**CSS Architecture**
- **Design System**: Custom CSS variables for colors, shadows, and border radius
- **Color Palette**: Primary blue (#4a6fff), secondary green (#0dbc95), comprehensive gray scale
- **Layout**: Flexbox and CSS Grid with sidebar + main content structure
- **Components**: Modular CSS classes for cards, buttons, forms, modals, and alerts
- **Responsive**: Breakpoints at 1200px, 992px, and 768px with mobile-first approach
- **Animations**: Fade-in animations, loading spinners, and smooth transitions

**JavaScript Functionality**
- **State Management**: Global variables for session management and file tracking
- **File Upload**: Drag-and-drop support with progress indicators and validation
- **API Integration**: RESTful endpoints for data processing and preview generation
- **Real-time Previews**: Debounced preview updates (300ms delay) for performance
- **Form Handling**: Custom radio/checkbox styling with active states
- **Modal System**: Reusable modal components for credits and notifications

**Key UI Components**
- **Sidebar**: Fixed 280px width with file upload area and credits
- **Tab System**: Four main tabs (QAA Report, Alumni List, Workplace Statistics, Banner Integration)
- **Form Controls**: Multi-select dropdowns, radio button groups, checkbox groups
- **Preview Cards**: Live data previews with monospace formatting
- **Download Panels**: Success states with direct download links
- **Alert System**: Success, warning, and error notifications with auto-fade

**API Endpoints Used**
- `/upload` - File upload with session creation
- `/get_constants` - Fetch colleges and graduation years
- `/{tab}_preview` - Real-time data previews for each report type
- `/generate_{report_type}` - Report generation endpoints
- `/download/{filename}` - File download endpoint

## File Structure

```
WebAlumni/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend SPA template
├── uploads/              # Temporary uploaded files (gitignored)
├── generated_files/      # Generated reports (gitignored)
├── requirements.txt      # Python dependencies
└── README.md            # Setup and usage documentation
```

## Data Models

### Expected Excel Columns

**Alumni List Files:**
- Student ID, Student Name, College, Year/Semester of Graduation
- Current Status, Current Workplace, Current Position
- Gender, Major, Nationality (optional)

**Banner Files:**
- Student ID, Student Name, College, Graduation Term
- Major, Gender, Degree

### Session Data Structure

```python
session_data[session_id] = {
    "data": pandas.DataFrame,
    "file_name": str,
    "timestamp": str,
    "is_banner": bool,
    "graduation_years": list
}
```

## Configuration Constants

**College Options**: Predefined list of 5 colleges
**Expected Employment Statuses**: 11 standard status values including "New graduate"
**Graduation Years**: Dynamically extracted from uploaded files or defaults to 2010-2025 range

## Security Considerations

- File upload validation (Excel files only, 16MB limit)
- Secure filename handling
- Session-based data isolation
- Automatic cleanup of old files and sessions (24 hour TTL)

## Frontend Development Patterns

**HTML Structure**
- Single template file with embedded styles and scripts
- Semantic HTML with accessibility considerations
- Consistent class naming following BEM-like conventions
- Grid-based layout system with responsive column spans

**CSS Patterns**
- Use CSS custom properties for consistent theming
- Utility classes for common spacing and layout patterns
- Component-based styling with clear separation of concerns
- Mobile-first responsive design approach

**JavaScript Patterns**
- Global state management with descriptive variable names
- Debounced API calls for performance optimization
- Event delegation for dynamic content
- Consistent error handling with user-friendly messages
- Session-based data management with cleanup

**Form Handling**
- Custom styling for form controls with active states
- Real-time validation and preview updates
- Accessibility-friendly form interactions
- Progressive enhancement approach

## Backend Development Patterns

- Use `safe_get_column()` when accessing potentially missing DataFrame columns
- All data processing functions return error dictionaries on failure
- Company name normalization is applied before workplace analysis
- High position detection is used for leadership statistics
- Gender and nationality filtering respects case sensitivity in Detailed mode
- Session-based data storage with automatic cleanup (24hr TTL)
- Simple mode uses case-insensitive text processing for robust data handling
- Academic year extraction handles multiple graduation term formats
- Mode-specific filtering logic: Simple mode ignores demographic filters, Detailed mode respects all filters