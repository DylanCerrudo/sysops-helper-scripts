# Regex helps find patterns in text, like finding ERROR lines
import re


# Function that takes one input: the path to a log file 
def analyze_log_file(log_file_path):
    """
    Analyzes a log file and detects errors
    """
    log_pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(INFO|ERROR|WARNING|CRITICAL)\s+(.+)'

    # Empty list to store all the errors we find
    errors = []

    # Empty list to store all the warnings we find
    warnings = []
    
    # Empty list to store all the critical issues we find
    criticals = []

    # Counter variable to count how many times we process
    total_lines = 0


    try:
        with open(log_file_path, 'r') as file:

            for line in file:

                total_lines +=1

                match = re.match(log_pattern, line)

                if match:

                    timestamp, level, message = match.groups()


                    if level == 'ERROR':

                        errors.append({'timestamp': timestamp, 'message': message})
                    

                    elif level == 'WARNING':

                        warnings.append({'timestamp': timestamp, 'message': message})
                    
                    elif level == 'CRITICAL':
                        criticals.append({'timestamp': timestamp, 'message': message})

        print(f"\n{'='*60}")
        print(f"LOG ANALYSIS REPORT")
        print(f"{'='*60}")
        print(f"Total lines processed: {total_lines}")
        print(f"Errors found: {len(errors)}")
        print(f"Warnings found: {len(warnings)}")
        print(f"Critical issues: {len(criticals)}")
        print(f"{'='*60}\n")

        if criticals:

            print("CRITICAL ISSUES:")

            for critical in criticals:

                print(f"  [{critical['timestamp']}] {critical['message']}")
            

            print()

        if errors:
            
            print("ERRORS:")

            for error in errors:
                
                print(f"  [{error['timestamp']}] {error['message']}")
            
            print()

        if warnings:

            print("WARNINGS:")

            for warning in warnings:

                print(f"  [{warning['timestamp']}] {warning['message']}")
    except FileNotFoundError:
        print(f"Error: Log file '{log_file_path}' not found")

    except Exception as e:

        print(f"An error has occurred: {str(e)}")
    

            
if __name__ == "__main__":
    analyze_log_file('sample_app.log')