import subprocess
import pandas as pd


def run_jmeter_test(local_jmeter_path, local_test_plan_path):
    command = [local_jmeter_path, '-n', '-t', local_test_plan_path, '-l', 'result.jtl']
    result.jtl = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.jtl


jmeter_path = 'C:/Dương/apache-jmeter-5.6.3/apache-jmeter-5.6.3/bin/jmeter.bat'
test_plan_path = 'C:/Dương/apache-jmeter-5.6.3/apache-jmeter-5.6.3/bin/JmeterWithPy.jmx'

result = run_jmeter_test(jmeter_path, test_plan_path)

if result.returncode == 0:
    print("Test executed successfully.")
else:
    print("Test execution failed.")
    print(result.stderr.decode('utf-8'))


def parse_jmeter_results(local_results_file):
    local_df = pd.read_csv(local_results_file)
    return local_df


results_file = 'result.jtl'
df = parse_jmeter_results(results_file)

# Display basic statistics
print(df.describe())

# For example, get average response time
average_response_time = df['elapsed'].mean()
print(f'Average Response Time: {average_response_time} ms')
