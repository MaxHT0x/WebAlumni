#!/usr/bin/env python3
"""
Create test Excel file for 2014-2015 with exact known graduate counts
Total: 251 graduates (162 male, 89 female)
"""

import pandas as pd
import random

def create_test_data_2014_2015():
    """Create controlled test dataset for 2014-2015 validation"""
    
    # Define exact distribution to match expected results
    college_distribution = {
        "College of Engineering & Advan": {"Male": 45, "Female": 25},  # 70 total
        "College of Business": {"Male": 40, "Female": 35},            # 75 total  
        "College of Science & General S": {"Male": 37, "Female": 23}, # 60 total
        "College of Medicine": {"Male": 25, "Female": 5},             # 30 total
        "College of Pharmacy": {"Male": 15, "Female": 1}              # 16 total
    }
    
    # Verify totals
    total_male = sum(college["Male"] for college in college_distribution.values())
    total_female = sum(college["Female"] for college in college_distribution.values()) 
    total_graduates = total_male + total_female
    
    print(f"Planned distribution:")
    print(f"Total Male: {total_male}")
    print(f"Total Female: {total_female}")
    print(f"Total Graduates: {total_graduates}")
    
    assert total_male == 162, f"Male count should be 162, got {total_male}"
    assert total_female == 89, f"Female count should be 89, got {total_female}"
    assert total_graduates == 251, f"Total should be 251, got {total_graduates}"
    
    # Create graduation terms for 2014-2015
    graduation_terms = [
        "2014-2015 FALL",
        "2014-2015 Spring", 
        "2014-2015 Summer"
    ]
    
    # Majors by college for realistic data
    majors_by_college = {
        "College of Engineering & Advan": ["Computer Science", "Electrical Engineering", "Mechanical Engineering", "Civil Engineering"],
        "College of Business": ["Finance", "Marketing", "Management", "Accounting"],
        "College of Science & General S": ["Mathematics", "Chemistry", "Physics", "Biology"],
        "College of Medicine": ["Medicine", "Surgery", "Pediatrics"],
        "College of Pharmacy": ["Clinical Pharmacy", "Pharmaceutical Sciences"]
    }
    
    # Employment statuses for realistic data
    employment_statuses = ["Employed", "Unemployed", "Business owner", "Training", "Studying", "New graduate"]
    
    records = []
    student_id_counter = 201400000  # Starting with 2014 year prefix
    
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
                
                # Generate record
                record = {
                    "Student ID": student_id,
                    "Student Name": f"Test Student {student_id}",
                    "College": college,
                    "Year/Semester of Graduation": graduation_term,
                    "Major": random.choice(majors_by_college[college]),
                    "Gender": gender,
                    "Current Status": random.choice(employment_statuses),
                    "Current Workplace": f"Test Company {random.randint(1, 100)}",
                    "Current Position": f"Test Position {random.randint(1, 50)}",
                    "Nationality": "Saudi Arabia" if random.random() < 0.7 else "Non-Saudi"
                }
                
                records.append(record)
    
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
    
    # Sort by graduation term and college for consistency
    df_sorted = df.sort_values(['Year/Semester of Graduation', 'College', 'Gender'])
    
    # Save to Excel file
    output_file = "/home/rakanlinux/coolProjects/WebAlumni/test_data_2014_2015.xlsx"
    df_sorted.to_excel(output_file, index=False, sheet_name="Alumni_Data")
    
    print(f"\nCreated test file: {output_file}")
    print(f"This file should produce exactly:")
    print(f"- Total graduates: 251")
    print(f"- Male graduates: 162")  
    print(f"- Female graduates: 89")
    
    return output_file

if __name__ == "__main__":
    create_test_data_2014_2015()