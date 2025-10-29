"""
SysOps Log Analyzer
Automates error detection in system logs to reduce troubleshooting time.
Parses log files using regex patterns and generates detailed error reports.
"""

import re
from datetime import datetime


# Function that takes one input: the path to a log file 
def analyze_log_file(log_file_path):
    """
    Analyzes a log file and categorizes issues by severity level.

    This function parses system logs line-by-line, extracts timestamp and
    severity information, and generates a summary report showing all errors,
    warnings, and critical issues found.
    """

    # Regex pattern breakdown:
    # (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - Captures ISO timestamp
    # (INFO|ERROR|WARNING|CRITICAL) - Matches log severity level
    # (.+) - Captures the entire message content
    log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(INFO|ERROR|WARNING|CRITICAL)\s+(.+)'


    errors = []     # Production errors that need immediate attention
    warnings = []   # Potential issues that should be monitored
    criticals = []  # System-threating issues requiring urgent action
    total_lines = 0 # Track total lines processed for metrics


    try:
        # Open log file in read-only mode
        # Using 'with' ensures file is properly closed even if errors occur
        with open(log_file_path, 'r') as file:

            # Process each log entry line-by-line to minimize memory usage
            for line in file:
                total_lines +=1

                # Attempt to match the line against our log pattern
                match = re.match(log_pattern, line)

                # Only process lines that match the expected log format
                # Ignores malformed or empty lines
                if match:
                    # Extract the captured groups: timestamp, severity, message
                    timestamp, level, message = match.groups()

                    # Categorize by severity level for prioritized reporting
                    if level == 'ERROR':

                        errors.append({'timestamp': timestamp, 'message': message})
                    

                    elif level == 'WARNING':

                        warnings.append({'timestamp': timestamp, 'message': message})
                    
                    elif level == 'CRITICAL':
                        criticals.append({'timestamp': timestamp, 'message': message})

        # Generate summary report header
        print(f"\n{'='*60}")
        print(f"LOG ANALYSIS REPORT")
        print(f"{'='*60}")
        print(f"Total lines processed: {total_lines}")
        print(f"Errors found: {len(errors)}")
        print(f"Warnings found: {len(warnings)}")
        print(f"Critical issues: {len(criticals)}")
        print(f"{'='*60}\n")
        
        # Display critical issues first - highest priority
        if criticals:

            print("CRITICAL ISSUES:")

            for critical in criticals:

                print(f"  [{critical['timestamp']}] {critical['message']}")
            
            print()
            
        # Display errors second - need attention but not urgent
        if errors:
            
            print("ERRORS:")

            for error in errors:
                
                print(f"  [{error['timestamp']}] {error['message']}")
            
            print()
            
        # Display warnings last - informational, monitor over time
        if warnings:

            print("WARNINGS:")

            for warning in warnings:

                print(f"  [{warning['timestamp']}] {warning['message']}")
                
    # Handle case where log file doesn't exist
    except FileNotFoundError:
        print(f"Error: Log file '{log_file_path}' not found")
        print("Please verify the file path and try again.")
        
    # Catch any unexpected errors during processing
    except Exception as e:
        print(f"An error has occurred: {str(e)}")
        print("Please verify the file path and try again.")

# Entry point - only runs when script is executed directly  
if __name__ == "__main__":
    # Analyze the sample log file in the current directory
    analyze_log_file('sample_app.log')