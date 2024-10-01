
# pytest-proceed

A pytest plugin to initiate test runs from a specific test file, proceeding alphabetically through the test suite. Perfect for targeted testing scenarios or partial test suite runs.

## Installation

Install using pip:

```bash
pip install pytest-proceed
```

## Usage

You can run `pytest-proceed` by specifying a test file to start from and pass any additional pytest options:

```bash
pytest-proceed tests/test_example.py -x -s
```

or

```bash
pytest-proceed -x -s tests/test_example.py
```

### Examples

- **Run all tests starting from a specific file**:  
  ```bash
  pytest-proceed tests/test_example.py
  ```

- **Run tests with pytest options (e.g., stop after first failure)**:  
  ```bash
  pytest-proceed -x tests/test_example.py
  ```
