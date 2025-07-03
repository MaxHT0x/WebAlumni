# QAA Report Test System

## Overview

This test system provides **integrated testing** for the WebAlumni QAA report functionality directly within the web interface. Instead of external test scripts, users can now validate report accuracy with a simple button click.

## Key Features

✅ **Real User Workflow Testing** - Tests the exact same process users follow  
✅ **True Integration Testing** - Validates complete pipeline from upload to Excel generation  
✅ **Separate Validation Logic** - Test verification code is completely separate from report generation  
✅ **Easy to Use** - Simple "Run Tests" button in the web interface  
✅ **Easy to Expand** - Designed for adding new test scenarios

## How It Works

### 1. **Upload Test Data**
- Use the provided `test_data_2014_2015.xlsx` file (251 graduates: 162 male, 89 female)
- Upload through the normal file upload interface

### 2. **Run Tests** 
- Click the **"Run Tests"** button next to "Generate QAA Report"
- System automatically:
  - Generates Simple mode report 
  - Generates Detailed mode report (with "combine all")
  - Parses the actual Excel files
  - Compares results with expected values

### 3. **View Results**
- ✅ **PASS**: Green success message with detailed breakdown
- ❌ **FAIL**: Orange warning with specific errors found
- Detailed results show expected vs actual counts

## Test Coverage

### Simple Mode Tests
- ✅ Total graduates: 251
- ✅ Gentlemen: 162  
- ✅ Ladies: 89
- ✅ Academic year grouping (2014-2015)

### Detailed Mode Tests  
- ✅ Total graduates: 251 (with "combine all" option)
- ✅ Excel structure parsing
- ✅ Total column validation

## Files Created

1. **`test_data_2014_2015.xlsx`** - Test data file with known graduate counts
2. **`test_validator.py`** - Excel validation logic (separate from app.py)
3. **`test_expectations.json`** - Expected results configuration
4. **`create_test_data_2014_2015.py`** - Script to regenerate test data if needed

## Using the Test System

### Step 1: Start the Application
```bash
source venv/bin/activate
python3 app.py
```

### Step 2: Upload Test File
1. Navigate to `http://127.0.0.1:5000/`
2. Upload `test_data_2014_2015.xlsx` using the file upload area

### Step 3: Run Tests
1. Go to the "QAA Report" tab
2. Click **"Run Tests"** button (🧪 icon)
3. Wait for test execution (generates 2 reports and validates them)
4. Review test results in the alert area

### Step 4: Interpret Results

**✅ Success Example:**
```
🧪 QAA Report Test Results for 2014-2015
==================================================

📊 SIMPLE MODE:
   ✅ Total graduates: 251 (expected: 251)
   ✅ Gentlemen: 162 (expected: 162)  
   ✅ Ladies: 89 (expected: 89)

📈 DETAILED MODE:
   ✅ Total graduates: 251 (expected: 251)

🎯 SUMMARY:
   ✅ Simple mode tests PASSED
   ✅ Detailed mode tests PASSED

🎉 ALL TESTS PASSED! 🎉
```

**❌ Failure Example:**
```
🧪 QAA Report Test Results for 2014-2015
==================================================

📊 SIMPLE MODE:
   ❌ Total graduates: 248 (expected: 251)
   ❌ Gentlemen: 160 (expected: 162)
   ✅ Ladies: 89 (expected: 89)

⚠️ SOME TESTS FAILED ⚠️
```

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
```javascript
// Modify runQaaTests() function to support multiple test years
test_year: '2015-2016'  // or make it selectable
```

## Troubleshooting

### Common Issues

**"No session available"**
- Upload the test Excel file first before running tests

**"Test year 2014-2015 not found"** 
- Verify the uploaded file contains 2014-2015 graduation terms
- Check that the file matches the expected structure

**"Could not find 'Total' column"**
- Detailed mode Excel structure might have changed
- Check if the app is using "combine all" option correctly

**"Could not find gender columns"**
- Simple mode Excel structure might have changed  
- Validator looks for "Gentlemen"/"Ladies" or "Male"/"Female" columns

### Validation Logic Details

The validator uses smart logic to find the correct totals in Excel files:

**Detailed Mode Validation:**
- Locates the "Total" column in the Excel header
- Searches for a row where the first column contains "Overall Total" (case-insensitive)
- Extracts the value from that specific row only
- **Why**: Prevents summing individual major totals + overall total (which would be wrong)

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
- **Button**: Added to QAA Report tab alongside "Generate QAA Report"
- **JavaScript**: `runQaaTests()` function handles UI and API calls
- **User Experience**: Same loading/alert patterns as normal report generation

### Backend Integration  
- **Endpoint**: `/run_tests` route in `app.py`
- **Process**: Uses existing `process_qaa_report()` function for actual report generation
- **Validation**: Separate `test_validator.py` module parses generated Excel files

### Separation of Concerns
- **Report Generation**: `app.py` (what we're testing)
- **Test Validation**: `test_validator.py` (the tester)
- **Never mixing the two ensures we test the real functionality**

## Benefits of This Approach

1. **User-Friendly**: Anyone can run tests, not just developers
2. **Real Environment**: Tests in actual browser/session environment  
3. **Integration Testing**: Catches bugs in the complete workflow
4. **Maintainable**: Easy to update expectations and add new scenarios
5. **Immediate Feedback**: Results show instantly in the web interface
6. **True Validation**: Tests actual Excel output, not parallel logic

This test system turns quality assurance into a **user feature** rather than a developer chore, while providing genuine validation of the application's core functionality.