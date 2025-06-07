#!/usr/bin/env python3
import argparse
import sys
import logging
from typing import List, Dict, Any
from data_processor import process_files
from reports import generate_report, ReportType

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('salary_report.log'),
            logging.StreamHandler()
        ]
    )

def parse_arguments() -> Dict[str, Any]:
    """Parse and validate command line arguments."""
    parser = argparse.ArgumentParser(
        description='Generate employee reports from CSV files.',
        epilog='Example: python main.py data1.csv data2.csv --report payout --format json'
    )
    
    parser.add_argument(
        'files',
        metavar='FILE',
        type=str,
        nargs='+',
        help='CSV files with employee data'
    )
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        choices=[rt.value for rt in ReportType],
        help='Type of report to generate'
    )
    parser.add_argument(
        '--format',
        type=str,
        default='text',
        choices=['text', 'json'],
        help='Output format (text or json)'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (if not specified, print to console)'
    )
    
    args = parser.parse_args()
    
    # Additional validation
    if not args.files:
        parser.error("At least one input file is required")
    
    return vars(args)

def save_output(content: str, output_path: str = None):
    """Save output to file or print to console."""
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        logging.info(f"Report saved to {output_path}")
    else:
        print(content)

def main():
    """Main function to process data and generate reports."""
    setup_logging()
    
    try:
        args = parse_arguments()
        logging.info(f"Starting report generation with args: {args}")
        
        employees = process_files(args['files'])
        report = generate_report(
            report_type=args['report'],
            employees=employees,
            output_format=args['format']
        )
        
        save_output(report, args.get('output'))
        logging.info("Report generated successfully")
        
    except FileNotFoundError as e:
        logging.error(f"File error: {e}")
        sys.exit(1)
    except ValueError as e:
        logging.error(f"Data error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()