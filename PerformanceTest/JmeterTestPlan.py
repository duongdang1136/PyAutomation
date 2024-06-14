import os
import pandas as pd
from pymeter.api.config import TestPlan
from pymeter.api.samplers import HTTPSampler
from pymeter.api.timers import ConstantTimer
from pymeter.api.config_elements import CSVDataSet


def create_test_plan(test_plan_path: str) -> TestPlan:
    """
    Creates a JMeter test plan.

    Args:
        test_plan_path (str): Path to the JMeter test plan (.jmx file).

    Returns:
        TestPlan: Configured TestPlan object.
    """
    # Load existing test plan
    test_plan = TestPlan(test_plan_path)
    return test_plan


def run_jmeter_test(test_plan: TestPlan, result_file: str = 'result.jtl'):
    """
    Runs a JMeter test plan.

    Args:
        test_plan (TestPlan): TestPlan object to be executed.
        result_file (str, optional): Path to the result file where JMeter will store the results. Defaults to 'result.jtl'.

    Returns:
        None
    """
    test_plan.run(result_file=result_file)
    print("Test executed successfully.")


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


# Example usage
test_plan_path = '/path/to/JmeterWithPy.jmx'  # Path to your JMeter test plan

# Ensure the test plan file exists
if not os.path.isfile(test_plan_path):
    raise FileNotFoundError(f"Test plan file not found at path: {test_plan_path}")

# Create and run the test plan
test_plan = create_test_plan(test_plan_path)
result_file = 'result.jtl'
run_jmeter_test(test_plan, result_file)

# Parse and analyze results
try:
    df = parse_jmeter_results(result_file)
    analyze_jmeter_results(df)
except (FileNotFoundError, ValueError) as e:
    print(e)

# Additional handling or processing can be done here based on the analysis
