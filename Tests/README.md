<!-- This test suite includes two test cases:

1. test_index:

Mocks the psutil.cpu_percent() and psutil.virtual_memory().percent to return high values (90% CPU, 85% memory).
Calls the index() function and asserts that the response contains the expected warning message and the correct CPU and memory utilization values.


2. test_index_normal_utilization:
Mocks the psutil.cpu_percent() and psutil.virtual_memory().percent to return normal values (50% CPU, 60% memory).

Calls the index() function and asserts that the response does not contain the warning message and displays the correct CPU and memory utilization values.



To run the tests, you'll need to have the unittest module installed. You can run the tests from the command line with the following command: -->

python -m unittest monitoring-app-test

<!-- This will execute the test suite and display the results.

The test suite demonstrates how to use the unittest.mock module to patch the psutil functions and control the input values for testing the index() function. It also shows how to assert the content and status code of the Flask response.
Let me know if you have any questions or if you'd like me to explain any part of the test suite in more detail. -->

