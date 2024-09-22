# Program to Compute \( f(x) = \ln|\sin(x)| \) Using Maclaurin Series Expansion

## Programming Language

The program is written in **Python 3**.

## Development Environment

- **IDE**: PyCharm 2024.2.2 (Professional Edition)
- **Runtime version**: 21.0.3+13-b509.15 aarch64 (JCEF 122.1.9)
- **VM**: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
- **Operating System**: macOS 14.6.1
- **Hardware**:
  - Memory: 4096M
  - Cores: 12
## How to Run the Program

1. **Prerequisites**:
   - Ensure you have Python 3 installed on your system.
   - The program is compatible with Python 3.6 and above.

2. **Files**:
   - `main.py`: The main program file containing the implementation.

3. **Running the Program**:
   - Open a terminal or command prompt.
   - Navigate to the directory containing `main.py`.
   - Run the program using the command:
     ```bash
     python main.py
     ```
   - Follow the on-screen prompts to input the function argument `x` and the precision `e`.
   - To exit the program, input `Кінець` when prompted for the function argument.

4. **Sample Run**:
   ```
   Enter the function argument: 0.5
   Enter the precision: 0.0001
   f(x, e) = -0.693147180560
   N(x, e) = 2
   Enter the function argument: Кінець
   No results to save.
   ```

## How to Run the Tests

1. **Prerequisites**:
   - Ensure you have the `unittest` module available (it comes pre-installed with Python).

2. **Test Files**:
   - `test_compute_bernoulli_numbers.py`: Unit tests for the Bernoulli numbers computation.
   - `test_compute_ln_sin_x.py`: Unit tests for the `compute_ln_sin_x` function.
   - `test_main.py`: Integration tests for the main program.

3. **Running the Tests**:
   - From the terminal, run the following commands:
     ```bash
     python -m unittest test_compute_bernoulli_numbers.py
     python -m unittest test_compute_ln_sin_x.py
     python -m unittest test_main.py
     ```
   - Each command will run the respective test suite and display the results.

4. **Sample Output**:
   ```
   ----------------------------------------------------------------------
   Ran 4 tests in 0.005s

   OK
   ```

## Debugging the Program

- **Debugging Tools**:
  - Use PyCharm's built-in debugger for step-by-step execution.
  - Insert `print` statements to display variable values at different stages.

- **Common Issues and Solutions**:
  - **OverflowError**: Occurs when computing factorials for large `n`. The code has been updated to handle this by using logarithms.
  - **ValueError**: Raised when invalid inputs are provided. Ensure that `x` and `e` are within the valid ranges.

- **Logging**:
  - You can add logging statements to capture detailed information during execution.

## Additional Notes

- **File Permissions**:
  - Ensure that the program has permission to read and write files in the directory when saving results.

- **Character Encoding**:
  - The program uses UTF-8 encoding for file operations to support Ukrainian characters.

- **System Locale**:
  - If you plan to use Ukrainian letters in filenames, ensure your system's locale supports them.

- **Time Constraints**:
  - The program includes a computation time limit of 15 minutes to prevent excessively long calculations.