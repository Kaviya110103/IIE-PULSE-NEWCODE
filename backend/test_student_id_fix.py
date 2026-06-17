"""
Test script to verify student ID generation works correctly.
Tests the core fix: using max numeric ID instead of count + 1.
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IIE.settings')
django.setup()

from connect.models import Students
from connect.api_views import generate_student_id
import re

def test_student_id_generation():
    """Test that student ID generation works correctly."""
    print("=" * 70)
    print("STUDENT ID GENERATION FIX VERIFICATION TEST")
    print("=" * 70)
    
    # Test 1: Create test students with specific IDs to simulate imported data
    print("\n1. Creating test students with specific IDs...")
    print("   (Simulating imported production data with gaps)")
    
    test_students = [
        {'student_id': '100FT-STU001', 'branch': '100ft', 'email': f'student1@test.com'},
        {'student_id': '100FT-STU005', 'branch': '100ft', 'email': f'student2@test.com'},
        {'student_id': '100FT-STU010', 'branch': '100ft', 'email': f'student3@test.com'},
        {'student_id': 'HOPES-STU001', 'branch': 'hopes', 'email': f'student4@test.com'},
        {'student_id': 'HOPES-STU003', 'branch': 'hopes', 'email': f'student5@test.com'},
    ]
    
    for test_data in test_students:
        try:
            student = Students.objects.create(
                student_id=test_data['student_id'],
                branch=test_data['branch'],
                email=test_data['email'],
                first_name='Test',
                last_name='Student',
                mobile_no='9999999999',
                date_of_birth='2000-01-01',
                city='Test City',
                state='Test State',
                qualification='Test',
                course='Test Course',
                gender='Other'
            )
            print(f"   ✅ Created: {test_data['student_id']}")
        except Exception as e:
            print(f"   ⚠️  Could not create {test_data['student_id']}: {str(e)}")
    
    # Test 2: Verify generation finds the max ID, not count
    print("\n2. Testing ID generation with gaps (core fix)...")
    print("   Expected: Next IDs should be based on MAX existing IDs, not count+1")
    
    tests = [
        ('100ft', '100FT-STU011'),  # Max is 010, next should be 011
        ('hopes', 'HOPES-STU004'),   # Max is 003, next should be 004
    ]
    
    all_passed = True
    for branch, expected_next in tests:
        try:
            next_id = generate_student_id(branch)
            print(f"\n   Branch: {branch}")
            print(f"   Expected: {expected_next}")
            print(f"   Got:      {next_id}")
            
            if next_id == expected_next:
                print(f"   ✅ PASS: Correct ID generated")
            else:
                print(f"   ❌ FAIL: Wrong ID!")
                all_passed = False
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            all_passed = False
    
    # Test 3: Verify the generated IDs don't already exist
    print("\n3. Verifying generated IDs are unique...")
    for branch, expected_next in tests:
        try:
            next_id = generate_student_id(branch)
            if Students.objects.filter(student_id=next_id).exists():
                print(f"   ❌ FAIL: ID {next_id} already exists!")
                all_passed = False
            else:
                print(f"   ✅ OK: {next_id} is unique")
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            all_passed = False
    
    # Test 4: Test branch name mappings
    print("\n4. Testing branch name mappings...")
    branch_tests = [
        ('100ft', '100FT'),
        ('hopes', 'HOPES'),
        ('kuniyamuthur', 'KUNIYA'),
        ('kunniyamuthur', 'KUNIYA'),
    ]
    
    for branch_input, expected_prefix in branch_tests:
        try:
            next_id = generate_student_id(branch_input)
            if next_id.startswith(expected_prefix):
                print(f"   ✅ {branch_input} → {expected_prefix}: {next_id}")
            else:
                print(f"   ❌ {branch_input} → Expected {expected_prefix}, got {next_id[:len(expected_prefix)]}")
                all_passed = False
        except Exception as e:
            print(f"   ⚠️  {branch_input}: {str(e)}")
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ ALL TESTS PASSED - Student ID generation fix is working!")
    else:
        print("❌ SOME TESTS FAILED - Check the output above")
    print("=" * 70)
    
    # Cleanup
    print("\n5. Cleaning up test data...")
    Students.objects.filter(student_id__in=[s['student_id'] for s in test_students]).delete()
    print("   ✅ Cleanup complete")
    
    return all_passed

if __name__ == '__main__':
    try:
        success = test_student_id_generation()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
