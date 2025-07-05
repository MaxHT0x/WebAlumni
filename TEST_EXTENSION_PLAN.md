# Test System Extension Plan
## Adding Multiple Years + Detailed Mode Status Testing

### Overview
This plan extends the current test system from testing only 2014-2015 to supporting multiple academic years and adds comprehensive status breakdown testing for detailed mode reports.

### Current Test Coverage (What we have)
- **Years**: 2014-2015 only
- **Simple Mode**: ✅ Total graduates, gentlemen, ladies
- **Detailed Mode**: ✅ Total graduates only
- **Status Testing**: ❌ None

### Target Test Coverage (What we want)
- **Years**: 2014-2015, 2015-2016, 2016-2017 (expandable to more)
- **Simple Mode**: ✅ Total graduates, gentlemen, ladies (per year)
- **Detailed Mode**: ✅ Total graduates + ✅ Status breakdown (Employed/Unemployed/Studying)
- **Status Testing**: ✅ Full employment status validation

---

## PHASE 1: Create Multi-Year Test Data

### 1.1 Create Test Data Generation Scripts

**New Files to Create:**
- `create_test_data_2015_2016.py`
- `create_test_data_2016_2017.py`
- `create_test_data_multi_year.py` (generates all years at once)

**Template Structure (based on existing `create_test_data_2014_2015.py`):**

```python
#!/usr/bin/env python3
"""
Create test Excel file for [YEAR] with exact known graduate and status counts
"""

def create_test_data_YYYY_YYYY():
    # Define exact distribution with KNOWN status breakdowns
    college_distribution = {
        "College of Engineering & Advan": {
            "Male": {"Employed": 30, "Unemployed": 8, "Studying": 7},    # 45 total
            "Female": {"Employed": 15, "Unemployed": 6, "Studying": 4}   # 25 total
        },
        # ... similar for other colleges
    }
    
    # Employment status mapping for detailed mode testing
    status_mapping = {
        "Employed": ["Employed", "Business owner", "Training", "New graduate", "Others"],
        "Unemployed": ["Unemployed"],
        "Studying": ["Studying"]
    }
```

### 1.2 Test Data Requirements

**Each year should have:**
- **Known total graduates** (different per year for variety)
- **Known gender breakdown** (gentlemen/ladies)
- **Known status breakdown** (Employed/Unemployed/Studying counts)
- **Realistic data distribution** across colleges and terms

**Suggested Year Distribution:**
```
2014-2015: 251 graduates (162M, 89F) - [EXISTING]
2015-2016: 285 graduates (180M, 105F) - [NEW]
2016-2017: 320 graduates (200M, 120F) - [NEW]
```

**Status Distribution Strategy:**
- ~70% Employed (various employed statuses)
- ~20% Unemployed  
- ~10% Studying
- Include data quality variations (whitespace, case) like current system

---

## PHASE 2: Update Test Expectations

### 2.1 Expand `test_expectations.json`

**Add new year sections:**

```json
{
  "detailed_mode": {
    "2014-2015": {
      "total_graduates": 251,
      "employed_count": 176,
      "unemployed_count": 50, 
      "studying_count": 25
    },
    "2015-2016": {
      "total_graduates": 285,
      "employed_count": 200,
      "unemployed_count": 57,
      "studying_count": 28
    },
    "2016-2017": {
      "total_graduates": 320,
      "employed_count": 224,
      "unemployed_count": 64,
      "studying_count": 32
    }
  },
  "simple_mode": {
    "2014-2015": { /* existing */ },
    "2015-2016": {
      "total_graduates": 285,
      "gentlemen": 180,
      "ladies": 105
    },
    "2016-2017": {
      "total_graduates": 320,
      "gentlemen": 200,
      "ladies": 120
    }
  }
}
```

### 2.2 Add Status Validation Configuration

**New section in `test_expectations.json`:**

```json
{
  "status_categories": {
    "employed_statuses": [
      "Employed", "Employed - add to list", "Business owner", 
      "Training", "Do not contact", "Others", 
      "Left the country", "Passed away", "New graduate"
    ],
    "unemployed_statuses": ["Unemployed"],
    "studying_statuses": ["Studying"]
  }
}
```

---

## PHASE 3: Enhance Test Validator

### 3.1 Update `test_validator.py`

**Add Status Validation to Detailed Mode:**

```python
def validate_detailed_mode_excel(self, excel_file_path: str, test_year: str = "2014-2015") -> Dict:
    """Enhanced validation including status breakdown"""
    
    # ... existing total validation code ...
    
    # NEW: Status breakdown validation
    employed_count = self._extract_status_count(data_sheet, "Employed", total_column_index)
    unemployed_count = self._extract_status_count(data_sheet, "Unemployed", total_column_index)
    studying_count = self._extract_status_count(data_sheet, "Studying", total_column_index)
    
    # Validate against expectations
    expected = self.expectations.get("detailed_mode", {}).get(test_year, {})
    self._validate_status_counts(results, employed_count, unemployed_count, studying_count, expected)
    
    return results

def _extract_status_count(self, sheet, status_name: str, total_column_index: int) -> int:
    """Extract count for specific employment status from Excel sheet"""
    # Search for status name in first column, get corresponding total
    # Implementation details...

def _validate_status_counts(self, results: Dict, actual_employed: int, actual_unemployed: int, 
                          actual_studying: int, expected: Dict):
    """Validate status counts against expectations"""
    # Compare actual vs expected for each status category
    # Add to results["details"] with ✅/❌ indicators
```

### 3.2 Add Multi-Year Test Support

**New method in `QAATestValidator`:**

```python
def run_multi_year_test_suite(self, test_years: List[str], file_paths: Dict[str, Dict[str, str]]) -> Dict:
    """
    Run tests across multiple years
    
    Args:
        test_years: ["2014-2015", "2015-2016", "2016-2017"]
        file_paths: {
            "2014-2015": {"simple": "path1", "detailed": "path2"},
            "2015-2016": {"simple": "path3", "detailed": "path4"},
            # ...
        }
    """
    results = {
        "overall_passed": False,
        "years_tested": test_years,
        "year_results": {},
        "summary": []
    }
    
    all_passed = True
    for year in test_years:
        year_result = self.run_full_test_suite(
            file_paths[year]["simple"], 
            file_paths[year]["detailed"], 
            year
        )
        results["year_results"][year] = year_result
        if not year_result["overall_passed"]:
            all_passed = False
    
    results["overall_passed"] = all_passed
    return results
```

---

## PHASE 4: Backend Integration

### 4.1 Update `/run_tests` Route in `app.py`

**Enhanced route to support multiple years:**

```python
@app.route('/run_tests', methods=['POST'])
def run_tests():
    """Run QAA report tests for multiple years with status validation"""
    try:
        data = request.json
        session_id = data.get('session_id')
        test_years = data.get('test_years', ['2014-2015'])  # NEW: Support multiple years
        include_status_tests = data.get('include_status_tests', True)  # NEW: Status testing flag
        
        if not session_id or session_id not in session_data:
            return jsonify({"error": "No valid session found."})
        
        validator = QAATestValidator()
        all_results = {}
        
        for test_year in test_years:
            # Generate reports for this year
            simple_result = process_qaa_report(/* ... parameters for this year ... */)
            detailed_result = process_qaa_report(/* ... parameters for this year ... */)
            
            # Validate reports
            year_results = validator.run_full_test_suite(
                simple_file_path, detailed_file_path, test_year
            )
            all_results[test_year] = year_results
        
        # Combine results
        overall_passed = all(result["overall_passed"] for result in all_results.values())
        
        return jsonify({
            "status": "success",
            "overall_passed": overall_passed,
            "test_results": all_results,
            "years_tested": test_years
        })
        
    except Exception as e:
        return jsonify({"error": f"Test execution failed: {str(e)}"})
```

---

## PHASE 5: Frontend Enhancements

### 5.1 Update HTML Template (`templates/index.html`)

**Add Test Configuration Options:**

```html
<!-- NEW: Test year selection -->
<div class="form-group">
    <label>Test Years:</label>
    <div class="checkbox-group">
        <label><input type="checkbox" id="test-year-2014-2015" value="2014-2015" checked> 2014-2015</label>
        <label><input type="checkbox" id="test-year-2015-2016" value="2015-2016"> 2015-2016</label>
        <label><input type="checkbox" id="test-year-2016-2017" value="2016-2017"> 2016-2017</label>
    </div>
</div>

<!-- NEW: Test options -->
<div class="form-group">
    <label><input type="checkbox" id="include-status-tests" checked> Include Status Testing</label>
</div>
```

### 5.2 Update JavaScript (`templates/index.html` - script section)

**Enhanced `runQaaTests()` function:**

```javascript
function runQaaTests() {
    // Get selected test years
    const testYears = Array.from(document.querySelectorAll('[id^="test-year-"]:checked'))
                           .map(cb => cb.value);
    
    const includeStatusTests = document.getElementById('include-status-tests').checked;
    
    if (testYears.length === 0) {
        showAlert('Please select at least one test year.', 'warning');
        return;
    }
    
    // Enhanced API call
    fetch('/run_tests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            session_id: currentSessionId,
            test_years: testYears,
            include_status_tests: includeStatusTests
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            displayMultiYearTestResults(data);
        } else {
            showAlert(`Test failed: ${data.error}`, 'error');
        }
    });
}

function displayMultiYearTestResults(data) {
    const results = [];
    
    for (const [year, yearResult] of Object.entries(data.test_results)) {
        results.push(`🗓️ ${year}:`);
        results.push(format_test_results_for_display(yearResult));
        results.push(''); // Empty line between years
    }
    
    const alertType = data.overall_passed ? 'success' : 'warning';
    showAlert(results.join('\n'), alertType);
}
```

---

## PHASE 6: Implementation Steps

### Step 1: Create Test Data Files
1. **Create `create_test_data_2015_2016.py`**
   - 285 graduates (180M, 105F)
   - Known status distribution: 200 Employed, 57 Unemployed, 28 Studying
   - Graduation terms: "2015-2016 FALL", "2015-2016 Spring", "2015-2016 Summer"

2. **Create `create_test_data_2016_2017.py`**
   - 320 graduates (200M, 120F)  
   - Known status distribution: 224 Employed, 64 Unemployed, 32 Studying
   - Graduation terms: "2016-2017 FALL", "2016-2017 Spring", "2016-2017 Summer"

3. **Run scripts to generate `test_data_2015_2016.xlsx` and `test_data_2016_2017.xlsx`**

### Step 2: Update Test Configuration
1. **Expand `test_expectations.json`** with new years and status expectations
2. **Add status category definitions** for validation

### Step 3: Enhance Validator
1. **Add status extraction logic** to `test_validator.py`
2. **Add status validation methods**
3. **Add multi-year test support**
4. **Update result formatting** for status breakdown display

### Step 4: Update Backend
1. **Modify `/run_tests` route** to support multiple years
2. **Add test year parameter validation**
3. **Update error handling** for multi-year scenarios

### Step 5: Update Frontend
1. **Add test year selection UI**
2. **Add status testing toggle**
3. **Update JavaScript** for multi-year testing
4. **Enhance results display** for multiple years

### Step 6: Testing & Validation
1. **Test each year individually** to ensure data integrity
2. **Test multi-year combinations**
3. **Verify status calculations** match expected employment breakdowns
4. **Test error scenarios** (missing files, invalid years, etc.)

---

## PHASE 7: Future Expansion Guide

### Adding New Test Years
1. **Create new test data script**: `create_test_data_YYYY_YYYY.py`
2. **Add expectations**: Update `test_expectations.json`
3. **Add frontend option**: New checkbox in HTML
4. **No backend changes needed** (automatically supported)

### Adding New Test Categories
1. **Define expectations** in `test_expectations.json`
2. **Add extraction logic** to `test_validator.py`
3. **Update result formatting** 
4. **Add frontend controls** if needed

### Test Data Quality Assurance
- **Always verify exact counts** before committing test data
- **Include status variations** (whitespace, case) to test normalization
- **Document expected results** clearly in JSON and scripts
- **Test cross-year consistency** to catch calculation bugs

---

## DELIVERABLES

### New Files to Create:
1. `create_test_data_2015_2016.py`
2. `create_test_data_2016_2017.py`
3. `test_data_2015_2016.xlsx`
4. `test_data_2016_2017.xlsx`

### Files to Modify:
1. `test_expectations.json` - Add new years and status expectations
2. `test_validator.py` - Add status validation and multi-year support
3. `app.py` - Update `/run_tests` route for multi-year support
4. `templates/index.html` - Add test configuration UI and enhanced JavaScript

### Validation Criteria:
- ✅ All three years test independently
- ✅ Multi-year testing works
- ✅ Status breakdown validation passes
- ✅ UI allows selecting years and test options
- ✅ Results display clearly shows year-by-year breakdown
- ✅ Error handling for missing/invalid test data

This plan provides a complete roadmap for extending the test system to support multiple years with comprehensive status testing while maintaining the existing robust architecture.