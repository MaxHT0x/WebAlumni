# QAA Report Test System

## Overview

This test system provides **fully automated testing** for the WebAlumni QAA report functionality. No manual file uploads required - test files are automatically loaded and results are displayed in a dedicated page.

## Key Features

✅ **Automatic File Loading** - Test files are pre-included in the project  
✅ **Real User Workflow Testing** - Tests the exact same process users follow  
✅ **True Integration Testing** - Validates complete pipeline from upload to Excel generation  
✅ **Multi-Year Testing** - Test multiple academic years simultaneously  
✅ **Employment Status Validation** - Validates detailed employment breakdowns (Employed/Unemployed/Studying)  
✅ **Separate Validation Logic** - Test verification code is completely separate from report generation  
✅ **Dedicated Results Page** - Results open in a new tab for better visibility  
✅ **Easy to Expand** - Designed for adding new test scenarios

## How It Works

### 1. **Navigate to Test Results Tab**
- Open the web application
- Click on the "Test Results" tab (5th tab in navigation)
- No file uploads needed - test files are automatically loaded from project root:
  - `test_data_2014_2015.xlsx` (251 graduates: 162M, 89F)
  - `test_data_2015_2016.xlsx` (285 graduates: 180M, 105F)
  - `test_data_2016_2017.xlsx` (320 graduates: 200M, 120F)

### 2. **Configure Tests** 
- Select test years: 2014-2015, 2015-2016, 2016-2017
- Toggle "Include Status Testing" for employment breakdown validation
- All test files are automatically available

### 3. **Run Tests** 
- Click **"Run Automatic Tests"** button
- New tab opens immediately with a dedicated test results page
- System automatically:
  - Loads test files for selected years
  - Generates Simple mode report(s) for selected years
  - Generates Detailed mode report(s) (with "combine all")
  - Parses the actual Excel files
  - Compares results with expected values including status breakdowns

### 4. **View Results**
- Results appear in real-time in the dedicated test page
- Each year gets its own result card with clear formatting
- ✅ **PASS**: Green indicators with detailed breakdown
- ❌ **FAIL**: Error messages with specific issues found
- Results show expected vs actual counts for all tested years

## Test Coverage

### Simple Mode Tests
- ✅ Total graduates per year
- ✅ Gender breakdown (Gentlemen/Ladies)  
- ✅ Academic year grouping
- ✅ Multi-year testing

### Detailed Mode Tests  
- ✅ Total graduates (with "combine all" option)
- ✅ Employment status breakdown (Employed/Unemployed/Studying)
- ✅ Excel structure parsing
- ✅ Employment stats validation

### Multi-Year Testing
- ✅ 2014-2015: 251 graduates (162M, 89F) - Basic validation
- ✅ 2015-2016: 285 graduates (180M, 105F) - With status breakdown: 200 Employed, 57 Unemployed, 28 Studying
- ✅ 2016-2017: 320 graduates (200M, 120F) - With status breakdown: 224 Employed, 64 Unemployed, 32 Studying

### Data Quality Testing
The test data includes comprehensive status value variations to validate the system's data cleaning and normalization capabilities:

**✅ Standard Status Values (11 total):**
- "Employed", "New graduate", "Unemployed", "Business Owner", "Studying", "Training"
- "Others", "Do Not Contact", "Left The Country", "Passed Away", "Employed - Add to List"

**✅ Whitespace Variations (13 variations):**
- Leading spaces: `" Employed"`, `" Unemployed"`, `" Business Owner"`
- Trailing spaces: `"Employed "`, `"New graduate "`, `"Training "`
- Multiple spaces: `"  Employed  "`

**✅ Case Variations (15 variations):**
- Lowercase: `"employed"`, `"unemployed"`, `"business owner"`, `"new graduate"`
- Uppercase: `"EMPLOYED"`, `"UNEMPLOYED"`, `"BUSINESS OWNER"`, `"NEW GRADUATE"`
- Mixed case: `"eMpLoYeD"`, `"UnEmPlOyEd"`, `"Business OWNER"`, `"Do Not CONTACT"`

**Total Status Variations: 39 different values**

This comprehensive test data validates:
- Status normalization (`clean_status()` function)
- Validation system's detection of problematic data
- Whitespace handling and case sensitivity
- Real-world data quality scenarios

## Files Created

1. **Test Data Files**:
   - `test_data_2014_2015.xlsx` - 251 graduates with status variations
   - `test_data_2015_2016.xlsx` - 285 graduates with controlled status distribution
   - `test_data_2016_2017.xlsx` - 320 graduates with controlled status distribution

2. **Test Infrastructure**:
   - `test_validator.py` - Excel validation logic (separate from app.py)
   - `test_expectations.json` - Expected results configuration with multi-year support
   
3. **Data Generation Scripts**:
   - `create_test_data_2014_2015.py`
   - `create_test_data_2015_2016.py` 
   - `create_test_data_2016_2017.py`

## Using the Test System

### Step 1: Start the Application
```bash
source venv/bin/activate
python3 app.py
```

### Step 2: Navigate to Test Results
1. Navigate to `http://127.0.0.1:5000/`
2. Click on the **"Test Results"** tab (5th tab in navigation)

### Step 3: Configure Tests
1. Select which years to test (2014-2015, 2015-2016, 2016-2017)
2. Toggle "Include Status Testing" if desired
3. Test files are automatically available - no uploads needed

### Step 4: Run Tests
1. Click **"Run Automatic Tests"** button
2. New tab opens with dedicated test results page
3. Watch real-time progress as tests execute sequentially

### Step 5: Interpret Results

Results appear in the dedicated test results page as individual cards for each year:

**✅ Success Example:**
- Header shows "WebAlumni Test Results" with selected years and start time
- Each year appears as a separate card with clear formatting
- Test output shows detailed pass/fail for Simple and Detailed modes
- Real-time status updates during execution

**❌ Failure Example:**
- Error cards show specific issues found
- Clear indication of which tests passed vs failed
- Detailed error messages for debugging

## Adding New Test Scenarios

### 1. Create New Test Data
```python
# Modify create_test_data_2014_2015.py or create new script
# Add data for different years/scenarios
```

### 2. Update Expected Results
```json
// Add to test_expectations.json
"detailed_mode": {
  "2015-2016": {
    "total_graduates": 300,
    "description": "New test scenario"
  }
},
"simple_mode": {
  "2015-2016": {
    "total_graduates": 300,
    "gentlemen": 180,
    "ladies": 120
  }
}
```

### 3. Update Frontend (Optional)
- Test year selection is now built into the UI
- Multi-year testing is automatically supported

## Troubleshooting

### Common Issues

**"Please select at least one test year"**
- Select checkboxes for test years before clicking "Run Automatic Tests"

**"Failed to load test file for [year]"** 
- Verify the test data file exists in the project directory
- Check file permissions and accessibility

**"Could not find 'Total' column"**
- Detailed mode Excel structure might have changed
- Check if the app is using "combine all" option correctly

**"Could not find gender columns"**
- Simple mode Excel structure might have changed  
- Validator looks for "Gentlemen"/"Ladies" or "Male"/"Female" columns

### Validation Logic Details

The validator uses smart logic to find the correct totals in Excel files:

**Detailed Mode Validation:**
- Locates the "Total" column for graduate count validation
- For status validation, finds the Employment Stats section (after empty columns)
- Reads aggregated Employed/Unemployed/Studying columns, not individual status columns
- **Why**: The Employment Stats section contains properly calculated totals that match the app's employment logic

**Simple Mode Validation:**
- Locates "Gentlemen" and "Ladies" columns (or "Male"/"Female" as fallback)
- Searches for a row where the first column contains exactly "TOTAL" 
- Extracts gender values from that specific row only
- **Why**: Prevents summing individual college totals + grand total (which would be wrong)

This approach ensures the validator reads the **same final numbers** that users see in their reports.

### Debug Mode

To debug validation issues:

1. **Check Generated Files**: Test files are kept in `generated_files/` for inspection
2. **Examine Excel Structure**: Open generated Excel files manually to see column layout
3. **Update Validator Logic**: Modify `test_validator.py` if Excel structure changes

## Technical Architecture

### Frontend Integration
- **Dedicated Tab**: "Test Results" tab with clean configuration interface
- **Test Configuration**: UI for selecting test years and options without file uploads
- **JavaScript**: `runAutomaticTests()` function opens new tab for results
- **User Experience**: Real-time progress and dedicated results page

### Backend Integration  
- **Automatic Loading**: `/load_test_file` endpoint loads Excel files from project root directory
- **Enhanced Testing**: `/run_tests` route supports multi-year testing
- **Process**: Uses existing `process_qaa_report()` function for actual report generation
- **Validation**: Enhanced `test_validator.py` with employment status extraction
- **Multi-Year Support**: Sequential testing to avoid conflicts

### Separation of Concerns
- **Report Generation**: `app.py` (what we're testing)
- **Test Validation**: `test_validator.py` (the tester)
- **Never mixing the two ensures we test the real functionality**

## Benefits of This Approach

1. **Fully Automated**: No manual file uploads - everything is built-in
2. **User-Friendly**: Anyone can run tests with a single click
3. **Real Environment**: Tests in actual browser/session environment  
4. **Integration Testing**: Catches bugs in the complete workflow
5. **Multi-Year Capability**: Test multiple academic years simultaneously
6. **Employment Validation**: Validates complex employment status calculations
7. **Dedicated Results**: Clear, readable results in a separate page
8. **True Validation**: Tests actual Excel output, not parallel logic
9. **Maintainable**: Easy to update expectations and add new scenarios

This test system provides **one-click quality assurance** that validates the application's core functionality using the exact same code paths that real users experience.