from typing import List, Dict, Any
import os
import logging

def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """Read and validate CSV file with employee data."""
    employees = []
    required_fields = {'name', 'department', 'hours_worked'}
    rate_fields = {'hourly_rate', 'rate', 'salary'}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            header = file.readline().strip().split(',')
            
            # Validate header
            missing_fields = required_fields - set(header)
            if missing_fields:
                raise ValueError(
                    f"Missing required fields in {file_path}: {missing_fields}"
                )
            
            rate_field = next((f for f in rate_fields if f in header), None)
            if not rate_field:
                raise ValueError(
                    f"No rate field found in {file_path}. Expected one of: {rate_fields}"
                )
            
            for line_num, line in enumerate(file, 2):
                if not line.strip():
                    continue
                    
                try:
                    values = line.strip().split(',')
                    if len(values) != len(header):
                        raise ValueError(
                            f"Line {line_num}: expected {len(header)} columns, got {len(values)}"
                        )
                    
                    employee = dict(zip(header, values))
                    
                    # Convert and validate numeric fields
                    employee['hours_worked'] = float(employee['hours_worked'])
                    employee['hourly_rate'] = float(employee[rate_field])
                    
                    employees.append(employee)
                    
                except ValueError as e:
                    logging.warning(
                        f"Skipping invalid data in {file_path}, line {line_num}: {e}"
                    )
    
    except UnicodeDecodeError:
        raise ValueError(f"File {file_path} is not a valid UTF-8 encoded file")
    
    return employees

def process_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """Process multiple CSV files with error handling."""
    all_employees = []
    
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        logging.info(f"Processing file: {file_path}")
        try:
            employees = read_csv_file(file_path)
            all_employees.extend(employees)
            logging.info(f"Processed {len(employees)} records from {file_path}")
        except Exception as e:
            logging.error(f"Error processing {file_path}: {e}")
            raise
    
    if not all_employees:
        raise ValueError("No valid employee records found in input files")
    
    return all_employees