import os
import subprocess
import pandas as pd
from typing import List, Optional

def run_jmeter_test(jmeter_path: str, test_plan_path: str, result_file: str = 'result.jtl',
                    additional_args: Optional[List[str]] = None) -> subprocess.CompletedProcess:
    """
    Runs a JMeter test plan.

    Args:
        jmeter_path (str): Path to the JMeter executable.
        test_plan_path (str): Path to the JMeter test plan (.jmx file).
        result_file (str, optional): Path to the result file where JMeter will store the results. Defaults to 'result.jtl'.
        additional_args (List[str], optional): Additional command-line arguments to pass to JMeter.

    Returns:
        subprocess.CompletedProcess: The result of the subprocess.run call, which includes information about the execution.
    """
    # Check if the JMeter executable path exists
    if not os.path.isfile(jmeter_path):
        raise FileNotFoundError(f"JMeter executable not found at path: {jmeter_path}")

    # Check if the test plan path exists
    if not os.path.isfile(test_plan_path):
        raise FileNotFoundError(f"Test plan file not found at path: {test_plan_path}")

    command = [jmeter_path, '-n', '-t', test_plan_path, '-l', result_file]

    if additional_args:
        command.extend(additional_args)

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        print("Test executed successfully.")
    except subprocess.CalledProcessError as e:
        result = e
        print("Test execution failed.")
        print(result.stderr.decode('utf-8'))

    return result

def parse_jmeter_results(results_file: str) -> pd.DataFrame:
    """
    Parses JMeter results from a .jtl file into a pandas DataFrame.

    Args:
        results_file (str): Path to the JMeter results file.

    Returns:
        pd.DataFrame: DataFrame containing the parsed JMeter results.
    """
    try:
        df = pd.read_csv(results_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Results file not found: {results_file}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"Results file is empty: {results_file}")
    except pd.errors.ParserError:
        raise ValueError(f"Error parsing results file: {results_file}")

    return df

def analyze_jmeter_results(df: pd.DataFrame):
    """
    Analyzes JMeter results stored in a DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing JMeter results.
    """
    # Display basic statistics
    print("Basic Statistics:")
    print(df.describe())

    # Calculate average response time
    if 'elapsed' in df.columns:
        average_response_time = df['elapsed'].mean()
        print(f'Average Response Time: {average_response_time} ms')
    else:
        print("Column 'elapsed' not found in the results file.")

    # Additional analysis can be added here, e.g., error rates, percentiles, etc.

def display_jtl_file_contents(results_file: str):
    """
    Display the contents of the JMeter results file.

    Args:
        results_file (str): Path to the JMeter results file.
    """
    try:
        with open(results_file, 'r') as file:
            contents = file.read()
            print("Contents of result.jtl:")
            print(contents)
    except FileNotFoundError:
        print(f"Results file not found: {results_file}")

# Example usage
jmeter_path = 'C:/Dương/apache-jmeter-5.6.3/apache-jmeter-5.6.3/bin/jmeter.bat'  # Path to JMeter executable
test_plan_path = 'C:/Dương/apache-jmeter-5.6.3/apache-jmeter-5.6.3/bin/JmeterWithPy.jmx'  # Path to your JMeter test plan

try:
    result = run_jmeter_test(jmeter_path, test_plan_path)
    display_jtl_file_contents('result.jtl')  # Display the contents of the result.jtl file
    df = parse_jmeter_results('result.jtl')
    analyze_jmeter_results(df)
except FileNotFoundError as e:
    print(e)
except ValueError as e:
    print(e)

# Additional handling or processing can be done here based on the analysis
