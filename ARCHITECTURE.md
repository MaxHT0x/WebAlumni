# WebAlumni Architecture Documentation

## Overview

WebAlumni is a Flask-based web application for processing and analyzing alumni data from Excel files. The application provides data cleaning, normalization, and report generation capabilities with a focus on employment statistics and workplace analysis.

## Core Architecture

### Single-File Design
- **Main Application**: `app.py` (2174 lines) - Complete Flask application with embedded business logic
- **Frontend**: `templates/index.html` - Single-page application with embedded CSS and JavaScript
- **Data Storage**: In-memory session-based storage with 24-hour TTL

### Key Components

## Configuration & Constants

### Application Setup (Lines 19-30)
```python
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload
app.config['GENERATED_FILES'] = 'generated_files'
session_data = {}  # Global session storage
```

### College Options (Lines 35-41)
Predefined list of 5 colleges:
- College of Engineering & Advan
- College of Business  
- College of Science & General S
- College of Medicine
- College of Pharmacy

### Expected Status Values (Lines 44-56)
11 standard employment status values including:
- Employed, Unemployed, Business owner, Training, Studying, New graduate, etc.

### Default Graduation Years (Lines 65-81)
Fallback years from 2010-2025 with FALL/Spring/Summer terms

## Data Processing Functions

### Data Cleaning & Normalization

#### `clean_status(status)` - Lines 89-92
Normalizes employment status values for consistent processing.

#### `clean_gender(gender)` - Lines 94-106
- Handles common gender variations (M/Man/Gentleman → Male)
- Maps F/Woman/Lady → Female
- Returns standardized gender values

#### `normalize_company_name(name)` - Lines 118-235
**Critical function for workplace analysis**
- Handles null/empty values with comprehensive categorization
- Maps company aliases (SNB → SAUDI NATIONAL BANK, BCG → BOSTON CONSULTING GROUP)
- Removes common corporate suffixes (LTD, CORPORATION, etc.)
- Categorizes empty patterns: COMPLETELY EMPTY, PLACEHOLDER, CONFIDENTIAL, etc.

#### `is_high_position(position)` - Lines 262-345
**Leadership position detection**
- Identifies C-suite positions (CEO, CFO, CTO, etc.)
- Detects director-level roles (Director, Managing Director, etc.)
- Recognizes VP positions and founder roles
- Returns normalized position names for analysis

### File Processing

#### `load_excel_data(file_path, session_id)` - Lines 439-630
**Main data loading and validation function**
- Detects file type (Alumni List vs Banner file)
- Validates required columns based on file type
- Performs comprehensive data validation:
  - Student ID format validation (lines 508-510)
  - College validation against predefined options (lines 561-564)
  - Current Status validation (lines 567-577)
  - Gender validation (lines 580-590)
  - Empty field detection with row numbers (lines 597-610)
- Creates normalized columns (`_College`, `_Year`, `_CurrentStatus`, `_Gender`)
- Returns detailed statistics and warnings

#### `extract_graduation_years(file_path)` - Lines 632-662
Extracts graduation years from Excel files, with fallback to defaults if extraction fails.

### Report Generation

#### `process_qaa_report(session_id, ...)` - Lines 825-1080
**Primary QAA report generation function**
- Supports both Detailed and Simple modes
- Handles filtering by college, year, degree, gender, nationality
- Creates employment statistics with percentage calculations
- Generates multiple sheet formats (Combined, by College, by Year)
- Adds gender/nationality breakdown sheets in separate writer

#### `process_simple_mode_report(filtered_df, ...)` - Lines 1083-1218
**Simple mode QAA report generation**
- Groups data by academic year (2013-2014 format)
- Shows basic graduate counts with gender breakdown only
- Ignores employment status and demographic filters
- Creates one sheet per academic year plus summary sheet

#### `create_all_years_summary_tab(filtered_df, ...)` - Lines 1221-1315
Creates comprehensive summary with college/gender/nationality breakdowns

### Workplace Analytics

#### `get_workplace_statistics(df, ...)` - Lines 347-434
**Comprehensive workplace analysis**
- Filters data by colleges, years, degree, gender, nationality
- Normalizes company names and separates empty/valid entries
- Calculates top employers, high positions, nationality distribution
- Returns statistics for JSON serialization

#### `analyze_unknown_entries(df)` - Lines 237-260
Analyzes distribution of unknown/empty workplace entries with categorization.

### Banner Integration

#### `process_banner_integration(banner_session_id, alumni_session_id)` - Lines 1514-1683
**Banner file integration with Alumni List**
- Compares Banner graduates with existing Alumni List
- Identifies new graduates not in Alumni List
- Maps Banner fields to Alumni List structure
- Sets default status as "New graduate"
- Preserves original Excel formatting and table structure

## API Endpoints

### File Management
- **POST `/upload`** (Lines 1692-1720) - File upload with session creation
- **POST `/load_test_file`** (Lines 1722-1772) - Load predefined test data
- **GET `/get_constants`** (Lines 1774-1791) - Fetch colleges and graduation years

### Preview Endpoints
- **POST `/qaa_preview`** (Lines 1793-1857) - Real-time QAA report preview
- **POST `/alumni_list_preview`** (Lines 1859-1914) - Alumni list filtering preview  
- **POST `/workplace_preview`** (Lines 1916-1946) - Workplace statistics preview

### Report Generation
- **POST `/generate_qaa_report`** (Lines 1948-1966) - Generate QAA reports
- **POST `/generate_alumni_list`** (Lines 2086-2102) - Generate alumni contact lists
- **POST `/generate_workplace_report`** (Lines 2104-2119) - Generate workplace analysis
- **POST `/generate_banner_integration`** (Lines 2121-2129) - Process Banner integration

### Testing & Utilities
- **POST `/run_tests`** (Lines 1968-2084) - Execute QAA report validation tests
- **GET `/download/<filename>`** (Lines 2131-2133) - File download
- **POST `/cleanup`** (Lines 2136-2171) - Clean up old files and sessions

## Data Models

### Session Data Structure (Line 30)
```python
session_data[session_id] = {
    "data": pandas.DataFrame,
    "file_name": str,
    "timestamp": str,
    "is_banner": bool,
    "graduation_years": list
}
```

### Required Alumni List Columns (Lines 462-472)
- College, Year/Semester of Graduation, Current Status
- Student ID, Gender, Major, Current Workplace, Current Position

### Required Banner File Columns (Lines 452-460)
- Student ID, Student Name, College, Graduation Term, Major, Gender

## Key Processing Patterns

### Data Normalization Pipeline
1. **File Upload** → Excel validation and column mapping
2. **Data Loading** → Comprehensive validation with warnings  
3. **Normalization** → Company names, status, gender standardization
4. **Report Generation** → Filtered analysis with statistics

### Error Handling Strategy
- All processing functions return error dictionaries on failure
- Comprehensive validation with row-level error reporting
- Graceful degradation with warning messages
- Session-based error isolation

### Performance Considerations
- In-memory session storage (production would need database)
- 24-hour automatic cleanup of files and sessions
- Streaming Excel generation for large datasets
- Separate Excel writers for breakdown sheets to avoid conflicts

## File Structure Integration

```
WebAlumni/
├── app.py                    # Main application (2174 lines)
├── templates/index.html      # Frontend SPA (~2800 lines)
├── uploads/                  # Temporary uploaded files
├── generated_files/          # Generated reports
├── tests/                    # Test system
│   ├── data/                # Test data files
│   ├── validation/          # Test validation system
│   └── generators/          # Test data generators
└── requirements.txt         # Python dependencies
```

## Testing System Integration

The application includes a comprehensive testing framework accessed via `/run_tests`:

- **Multi-year testing** with validation across different academic years
- **Status validation** ensuring employment statistics accuracy  
- **Simple vs Detailed mode** comparison testing
- **Expected totals validation** against predefined test expectations

Test files are located in `tests/data/` with corresponding generators in `tests/generators/`.

## Security & Deployment Notes

- File upload validation (Excel only, 16MB limit)
- Secure filename handling with `secure_filename()`
- Session-based data isolation
- Automatic cleanup prevents data accumulation
- No database credentials or external dependencies for core functionality