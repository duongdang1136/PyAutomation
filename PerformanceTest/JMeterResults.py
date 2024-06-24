import pandas as pd


def parse_jmeter_results(results_file):
    df = pd.read_csv(results_file)
    return df


results_file = 'result.jtl'
df = parse_jmeter_results(results_file)

# Display basic statistics
print(df.describe())

# For example, get average response time
average_response_time = df['elapsed'].mean()
print(f'Average Response Time: {average_response_time} ms')
