from typing import List, Dict, Any, Optional
import json
from enum import Enum

class ReportType(str, Enum):
    PAYOUT = 'payout'
    AVG_RATE = 'avg_rate'

def generate_payout_report(employees: List[Dict[str, Any]], 
                         output_format: str = 'text') -> str:
    """Generate payout report grouped by department."""
    departments = {}
    
    for emp in employees:
        dept = emp['department']
        if dept not in departments:
            departments[dept] = {
                'employees': [],
                'total_hours': 0,
                'total_payout': 0
            }
        
        payout = emp['hours_worked'] * emp['hourly_rate']
        departments[dept]['employees'].append({
            'name': emp['name'],
            'hours': emp['hours_worked'],
            'rate': emp['hourly_rate'],
            'payout': payout
        })
        departments[dept]['total_hours'] += emp['hours_worked']
        departments[dept]['total_payout'] += payout
    
    if output_format == 'json':
        return json.dumps(departments, indent=2)
    
    # Text format
    report_lines = [
        "|    | name  | hours | rate | payout |",
        "|---|---|---|---|---|"
    ]
    
    for dept, data in departments.items():
        report_lines.append(f"| {dept}    |    |    |    |    |")
        
        for emp in data['employees']:
            report_lines.append(
                f"| ---   | {emp['name']} | {emp['hours']:.0f}  | {emp['rate']:.0f}    | ${emp['payout']:.0f}    |"
            )
        
        report_lines.append(
            f"|    |    | {data['total_hours']:.0f}  |    | ${data['total_payout']:.0f}    |"
        )
    
    return "\n".join(report_lines)

def generate_avg_rate_report(employees: List[Dict[str, Any]], 
                           output_format: str = 'text') -> str:
    """Generate average hourly rate report by department."""
    departments = {}
    
    for emp in employees:
        dept = emp['department']
        if dept not in departments:
            departments[dept] = {
                'total_rate': 0,
                'count': 0
            }
        
        departments[dept]['total_rate'] += emp['hourly_rate']
        departments[dept]['count'] += 1
    
    for dept in departments:
        departments[dept]['avg_rate'] = (
            departments[dept]['total_rate'] / departments[dept]['count']
        )
    
    if output_format == 'json':
        return json.dumps(
            {dept: data['avg_rate'] for dept, data in departments.items()},
            indent=2
        )
    
    # Text format
    report_lines = [
        "| Department | Average Rate |",
        "|---|---|"
    ]
    
    for dept, data in departments.items():
        report_lines.append(
            f"| {dept} | {data['avg_rate']:.2f} |"
        )
    
    return "\n".join(report_lines)

def generate_report(report_type: str, 
                   employees: List[Dict[str, Any]], 
                   output_format: str = 'text') -> str:
    """Generate the requested report type."""
    try:
        report_type_enum = ReportType(report_type)
    except ValueError:
        raise ValueError(f"Unknown report type: {report_type}. Available: {[rt.value for rt in ReportType]}")
    
    if report_type_enum == ReportType.PAYOUT:
        return generate_payout_report(employees, output_format)
    elif report_type_enum == ReportType.AVG_RATE:
        return generate_avg_rate_report(employees, output_format)