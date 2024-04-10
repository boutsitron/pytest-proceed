import argparse
import re
import subprocess
import traceback


def main():
    """
    Run pytest for specific test file and all test files that follow it alphabetically.

    This function takes a partial name of a test file as input and runs pytest for that test file and all the test files
    that come after it alphabetically. It performs the following steps:
    1. Parses the command-line arguments to get the partial name of the test file.
    2. Checks if the test file has a syntax error.
    3. Lists all the test files available in the test suite.
    4. Extracts only the test file paths from the test output.
    5. Finds the index of the test file that matches the partial name.
    6. Generates the pytest command to run the tests.
    7. Executes the pytest command.

    Note: This function assumes that pytest is installed and available in the system.

    Raises:
        SystemExit: If a syntax error is detected in the test file.
        CalledProcessError: If the pytest command fails.
    """
    # Setup Argument Parsing
    parser = argparse.ArgumentParser(
        description="Run pytest for specific test file and all test files that follow it alphabetically."
    )
    parser.add_argument(
        "test_file",
        type=str,
        help="Partial name of the test file to start from (e.g., tests/test_continuation.py)",
    )
    args = parser.parse_args()
    test_file_partial = args.test_file

    # Check if the test file has a syntax error
    try:
        with open(test_file_partial, "r", encoding="utf-8") as file:
            source = file.read()
        compile(source, test_file_partial, "exec")
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
    if test_file_partial not in " ".join(unique_test_files):
        print(
            f"No test file starting with '{test_file_partial}' found in the test suite."
        )
    else:
        start_index = next(
            (
                i
                for i, test_file in enumerate(unique_test_files)
                if test_file.startswith(test_file_partial)
            ),
            None,
        )

        # Generate pytest command
        files_to_run = " ".join(unique_test_files[start_index:])
        pytest_command = f"pytest -x {files_to_run}"

        # Execute the pytest command
        print(f"Running: {pytest_command}")
        subprocess.run(pytest_command.split(), check=True)


if __name__ == "__main__":
    main()
