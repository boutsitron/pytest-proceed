import sys
import re
import subprocess
import traceback


def main():
    """
    Run pytest for specific test file and all test files that follow it alphabetically, with options.

    This function takes pytest options and a partial name of a test file as input and runs pytest for that test file
    and all the test files that come after it alphabetically. It performs the following steps:
    1. Collects all command-line arguments.
    2. Identifies the test file among the arguments.
    3. Separates pytest options from the test file.
    4. Checks if the test file has a syntax error.
    5. Lists all the test files available in the test suite.
    6. Extracts only the test file paths from the test output.
    7. Finds the index of the test file that matches the partial name.
    8. Generates the pytest command to run the tests with the given pytest options.
    9. Executes the pytest command.

    Raises:
        SystemExit: If a syntax error is detected in the test file or if the test file is not specified.
        CalledProcessError: If the pytest command fails.
    """
    # Collect all arguments after the script name
    all_args = sys.argv[1:]

    if not all_args:
        print("Error: You must specify a test file.")
        exit(1)

    test_file_partial = None
    pytest_options = []

    # Identify the test file and collect pytest options
    for arg in all_args:
        if arg.endswith(".py") or (
            not arg.startswith("-") and not arg.startswith("--")
        ):
            if not test_file_partial:
                test_file_partial = arg
            else:
                pytest_options.append(arg)
        else:
            pytest_options.append(arg)

    if not test_file_partial:
        print("Error: You must specify a test file.")
        exit(1)

    # Check if the test file exists
    try:
        with open(test_file_partial, "r", encoding="utf-8") as file:
            source = file.read()
        compile(source, test_file_partial, "exec")
    except FileNotFoundError:
        print(f"Error: The test file '{test_file_partial}' was not found.")
        exit(1)
    except SyntaxError:
        traceback.print_exc()
        exit(
            "Syntax error detected in the test file. Please correct it before proceeding."
        )

    # List all tests
    completed_process = subprocess.run(
        ["pytest", "--collect-only", "-q"], capture_output=True, text=True, check=True
    )
    test_output = completed_process.stdout.splitlines()

    # Extract only the test file paths
    test_files = [re.split(r"::", test)[0] for test in test_output if "::" in test]
    unique_test_files = list(dict.fromkeys(test_files))  # Remove duplicates

    # Find and run tests
    matched_files = [f for f in unique_test_files if f.startswith(test_file_partial)]
    if not matched_files:
        print(
            f"No test file starting with '{test_file_partial}' found in the test suite."
        )
        exit(1)
    else:
        start_index = unique_test_files.index(matched_files[0])
        files_to_run = unique_test_files[start_index:]
        pytest_command = ["pytest"] + pytest_options + files_to_run

        # Execute the pytest command
        print(f"Running: {' '.join(pytest_command)}")
        subprocess.run(pytest_command, check=True)


if __name__ == "__main__":
    main()
