import os
import pytest
from data_processor import read_csv_file, process_files

@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a temporary CSV file for testing."""
    content = """id,email,name,department,hours_worked,hourly_rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40"""
    
    file_path = tmp_path / "test.csv"
    file_path.write_text(content)
    return str(file_path)

@pytest.fixture
def sample_csv_file_with_rate(tmp_path):
    """Create a temporary CSV file with 'rate' column instead of 'hourly_rate'."""
    content = """id,email,name,department,hours_worked,rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40"""
    
    file_path = tmp_path / "test_rate.csv"
    file_path.write_text(content)
    return str(file_path)

def test_read_csv_file(sample_csv_file):
    """Test reading a CSV file."""
    employees = read_csv_file(sample_csv_file)
    
    assert len(employees) == 2
    assert employees[0]['name'] == 'Alice Johnson'
    assert employees[0]['hours_worked'] == 160
    assert employees[0]['hourly_rate'] == 50

def test_read_csv_file_with_rate_column(sample_csv_file_with_rate):
    """Test reading a CSV file with 'rate' column."""
    employees = read_csv_file(sample_csv_file_with_rate)
    
    assert len(employees) == 2
    assert employees[0]['name'] == 'Alice Johnson'
    assert employees[0]['hours_worked'] == 160
    assert employees[0]['hourly_rate'] == 50

def test_process_files(sample_csv_file, sample_csv_file_with_rate):
    """Test processing multiple files."""
    employees = process_files([sample_csv_file, sample_csv_file_with_rate])
    
    assert len(employees) == 4
    assert all('hourly_rate' in emp for emp in employees)

def test_process_files_nonexistent():
    """Test processing with non-existent file."""
    with pytest.raises(FileNotFoundError):
        process_files(["nonexistent.csv"])