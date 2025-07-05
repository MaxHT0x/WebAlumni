#!/usr/bin/env python3
"""
Create test Excel file for 2016-2017 with exact known graduate and status counts
Total: 320 graduates (200 male, 120 female)
Status distribution: 224 Employed, 64 Unemployed, 32 Studying
"""

import pandas as pd
import random

def create_test_data_2016_2017():
    """Create controlled test dataset for 2016-2017 validation"""
    
    # Define exact distribution to match expected results
    college_distribution = {
        "College of Engineering & Advan": {"Male": 65, "Female": 35},  # 100 total
        "College of Business": {"Male": 55, "Female": 45},            # 100 total  
        "College of Science & General S": {"Male": 45, "Female": 30}, # 75 total
        "College of Medicine": {"Male": 25, "Female": 7},             # 32 total
        "College of Pharmacy": {"Male": 10, "Female": 3}              # 13 total
    }
    
    # Verify totals
    total_male = sum(college["Male"] for college in college_distribution.values())
    total_female = sum(college["Female"] for college in college_distribution.values()) 
    total_graduates = total_male + total_female
    
    print(f"Planned distribution:")
    print(f"Total Male: {total_male}")
    print(f"Total Female: {total_female}")
    print(f"Total Graduates: {total_graduates}")
    
    assert total_male == 200, f"Male count should be 200, got {total_male}"
    assert total_female == 120, f"Female count should be 120, got {total_female}"
    assert total_graduates == 320, f"Total should be 320, got {total_graduates}"
    
    # Create graduation terms for 2016-2017
    graduation_terms = [
        "2016-2017 FALL",
        "2016-2017 Spring", 
        "2016-2017 Summer"
    ]
    
    # Majors by college for realistic data
    majors_by_college = {
        "College of Engineering & Advan": ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering"],
        "College of Business": ["Finance", "Marketing", "Management", "Accounting"],
        "College of Science & General S": ["Mathematics", "Chemistry", "Physics", "Biology"],
        "College of Medicine": ["Medicine", "Surgery", "Pediatrics"],
        "College of Pharmacy": ["Clinical Pharmacy", "Pharmaceutical Sciences"]
    }
    
    # Employment statuses with specific distribution for testing
    # Need to create exactly: 224 Employed, 64 Unemployed, 32 Studying
    
    # Employment status mapping for detailed mode testing
    employed_statuses = [
        "Employed", "Employed - Add to List", "Business Owner", "Training", 
        "New graduate", "Others", "Do Not Contact", "Left The Country", "Passed Away"
    ]
    
    # Add variations for data quality testing
    employed_statuses_with_variations = employed_statuses + [
        # Whitespace variations
        "Employed ", " Employed", "  Employed  ", "Business Owner ", " Business Owner",
        "New graduate ", " New graduate", "Training ", " Training",
        # Case variations
        "employed", "EMPLOYED", "business owner", "BUSINESS OWNER", "new graduate", "NEW GRADUATE",
        "training", "TRAINING", "others", "OTHERS", "do not contact", "DO NOT CONTACT",
        # Mixed case variations
        "eMpLoYeD", "Business OWNER", "New Graduate", "Do Not CONTACT"
    ]
    
    unemployed_statuses = ["Unemployed", "Unemployed ", " Unemployed", "unemployed", "UNEMPLOYED", "UnEmPlOyEd"]
    studying_statuses = ["Studying", "Studying ", " Studying", "studying", "STUDYING", "StUdYiNg"]
    
    # Create status distribution list
    status_distribution = []
    # Add 224 employed statuses
    for i in range(224):
        status_distribution.append(random.choice(employed_statuses_with_variations))
    # Add 64 unemployed statuses  
    for i in range(64):
        status_distribution.append(random.choice(unemployed_statuses))
    # Add 32 studying statuses
    for i in range(32):
        status_distribution.append(random.choice(studying_statuses))
    
    # Shuffle the distribution to randomize assignment
    random.shuffle(status_distribution)
    
    records = []
    student_id_counter = 201600000  # Starting with 2016 year prefix
    status_index = 0
    
    for college, gender_counts in college_distribution.items():
        for gender, count in gender_counts.items():
            for i in range(count):
                # Distribute across terms roughly evenly
                term_index = i % len(graduation_terms)
                graduation_term = graduation_terms[term_index]
                
                # 20% chance of being graduate student
                is_graduate = random.random() < 0.2
                
                # Create student ID
                if is_graduate:
                    student_id = f"G{student_id_counter}"
                else:
                    student_id = str(student_id_counter)
                
                student_id_counter += 1
                
                # Generate record with controlled status distribution
                record = {
                    "Student ID": student_id,
                    "Student Name": f"Test Student {student_id}",
                    "College": college,
                    "Year/Semester of Graduation": graduation_term,
                    "Major": random.choice(majors_by_college[college]),
                    "Gender": gender,
                    "Current Status": status_distribution[status_index],
                    "Current Workplace": f"Test Company {random.randint(1, 100)}",
                    "Current Position": f"Test Position {random.randint(1, 50)}",
                    "Nationality": "Saudi Arabia" if random.random() < 0.7 else "Non-Saudi"
                }
                
                records.append(record)
                status_index += 1
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Verify final counts
    print(f"\nActual generated data:")
    gender_counts = df["Gender"].value_counts()
    print(f"Male: {gender_counts.get('Male', 0)}")
    print(f"Female: {gender_counts.get('Female', 0)}")
    print(f"Total: {len(df)}")
    
    college_counts = df["College"].value_counts()
    for college in college_distribution.keys():
        print(f"{college}: {college_counts.get(college, 0)}")
    
    # Verify gender distribution by college
    print(f"\nGender distribution by college:")
    for college in college_distribution.keys():
        college_df = df[df["College"] == college]
        college_gender_counts = college_df["Gender"].value_counts()
        male_count = college_gender_counts.get("Male", 0)
        female_count = college_gender_counts.get("Female", 0)
        print(f"{college}: {male_count}M + {female_count}F = {male_count + female_count}")
    
    # Verify status distribution (for testing purposes)
    print(f"\nStatus distribution verification:")
    status_counts = df["Current Status"].value_counts()
    employed_count = sum(status_counts.get(status, 0) for status in employed_statuses_with_variations)
    unemployed_count = sum(status_counts.get(status, 0) for status in unemployed_statuses)
    studying_count = sum(status_counts.get(status, 0) for status in studying_statuses)
    print(f"Employed variations: {employed_count}")
    print(f"Unemployed variations: {unemployed_count}")
    print(f"Studying variations: {studying_count}")
    
    # Sort by graduation term and college for consistency
    df_sorted = df.sort_values(['Year/Semester of Graduation', 'College', 'Gender'])
    
    # Save to Excel file
    output_file = "/home/rakanlinux/coolProjects/WebAlumni/tests/data/test_data_2016_2017.xlsx"
    df_sorted.to_excel(output_file, index=False, sheet_name="Alumni_Data")
    
    print(f"\nCreated test file: {output_file}")
    print(f"This file should produce exactly:")
    print(f"- Total graduates: 320")
    print(f"- Male graduates: 200")  
    print(f"- Female graduates: 120")
    print(f"- Employed: 224")
    print(f"- Unemployed: 64")
    print(f"- Studying: 32")
    
    return output_file

if __name__ == "__main__":
    create_test_data_2016_2017()