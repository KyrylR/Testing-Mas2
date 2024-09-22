import math
import re
import datetime
import time
import sys

def compute_bernoulli_numbers(n_max):
    """
    Computes Bernoulli numbers B_0 to B_n_max using the Akiyama–Tanigawa algorithm.

    Parameters:
    n_max (int): The maximum index n for which to compute B_n.

    Returns:
    list: A list containing Bernoulli numbers from B_0 to B_n_max.

    Raises:
    ValueError: If n_max is negative or not an integer.
    """
    if not isinstance(n_max, int) or n_max < 0:
        raise ValueError("n_max must be a non-negative integer.")

    A = [0.0] * (n_max + 1)  # Temporary list for computations
    B = [0.0] * (n_max + 1)  # List to store Bernoulli numbers

    for m in range(n_max + 1):
        A[m] = 1 / (m + 1)
        for j in range(m, 0, -1):
            A[j - 1] = j * (A[j - 1] - A[j])
        B[m] = A[0]  # The first element is the Bernoulli number B_m

    # Adjust signs according to standard definitions
    for n in range(1, n_max + 1):
        if n == 1:
            B[n] = -B[n]  # Correct the sign for B_1
        elif n % 2 == 1 and n > 1:
            B[n] = 0.0  # Set B_n = 0 for odd n > 1

    return B  # Returns a list of Bernoulli numbers B[0] to B[n_max]


def compute_ln_sin_x(x, e):
    """
    Computes f(x) = ln|sin(x)| using the Maclaurin series expansion.

    Parameters:
    x (float): The function argument.
    e (float): The desired precision (0 < e < 1).

    Returns:
    tuple: A tuple containing:
        - f_x_e (float): The computed value of the function.
        - N (int): The number of terms used in the series expansion.

    Raises:
    ValueError: If the function cannot be computed for the given x and e.
    TimeoutError: If the computation cannot achieve desired precision within 15 minutes.

    """
    # Validate input e
    if not (0 < e < 1):
        raise ValueError("Precision e must be in the interval (0;1).")

    x_mod_pi = x % math.pi  # Reduce x modulo pi
    if x_mod_pi == 0 or x_mod_pi == math.pi:
        raise ValueError("Function undefined for x = k * pi")
    if x_mod_pi > math.pi / 2:
        x_mod_pi = math.pi - x_mod_pi  # Use symmetry of sine function
    if x_mod_pi == 0:
        raise ValueError("Function undefined for x = k * pi")

    ln_x_mod_pi = math.log(abs(x_mod_pi))  # Compute ln|x_mod_pi|
    sum_terms = 0.0  # Initialize sum of terms
    N = 0  # Term counter
    n = 1
    max_n = 10000  # Increase limit to allow more terms

    # Compute Bernoulli numbers up to necessary order
    B = compute_bernoulli_numbers(2 * max_n + 2)  # Compute B[0] to B[2*max_n+2]

    start_time = time.time()
    ln_2 = math.log(2)
    ln_abs_x_mod_pi = math.log(abs(x_mod_pi))
    ln_e = math.log(e)
    ln_min_float = math.log(sys.float_info.min)
    while n <= max_n:
        # Check computation time
        if time.time() - start_time > 15 * 60:  # 15 minutes limit
            raise TimeoutError("Cannot achieve desired precision within 15 minutes.")

        B_2n = B[2 * n]  # Get Bernoulli number B_{2n}
        if B_2n == 0:
            n += 1
            continue

        # Compute ln(|T_n|)
        ln_T_n = (2 * n - 1) * ln_2 + math.log(abs(B_2n)) + 2 * n * ln_abs_x_mod_pi - math.log(n) - math.lgamma(2 * n +1)

        # Compute T_n = sign_T_n * exp(ln_T_n)
        sign_B_2n = 1 if B_2n > 0 else -1
        sign_T_n = (-1) ** (n - 1) * sign_B_2n

        # Avoid underflow
        if ln_T_n < ln_min_float:
            T_n = 0.0
        else:
            T_n = sign_T_n * math.exp(ln_T_n)

        sum_terms += T_n  # Add term to sum
        N = n  # Update term counter
        n += 1

        # Compute ln(|T_n_plus1|) for next term
        if 2 * n <= len(B) -1:
            B_2n_next = B[2 * n]
            if B_2n_next == 0:
                continue
            ln_T_n_plus1 = (2 * n - 1) * ln_2 + math.log(abs(B_2n_next)) + 2 * n * ln_abs_x_mod_pi - math.log(n) - math.lgamma(2 * n +1)
            if ln_T_n_plus1 < ln_e:
                break
        else:
            break
    else:
        raise ValueError("Cannot achieve desired precision with given x and e.")

    f_x_e = ln_x_mod_pi - sum_terms
    return f_x_e, N


def save_results_to_file(filename, session_results):
    """
    Saves the session results to the specified file.

    Parameters:
    filename (str): The name of the file to save results.
    session_results (list): A list of dictionaries containing the session results.

    Returns:
    int: The total number of entries in the file after saving.

    Raises:
    Exception: If there is an error while writing or reading the file.

    """
    date_str = datetime.datetime.now().strftime("%d.%m.%Y")
    try:
        with open(filename, 'a', encoding='utf-8') as f:
            for result in session_results:
                x = result['x']
                e = result['e']
                f_x_e = result['f_x_e']
                N = result['N']
                f.write(f"{date_str}, {x}, {e}, {f_x_e:.12f}, {N}\n")
    except Exception as ex:
        print("An error occurred while writing to the file:", ex)
        return None
    # Count total number of entries in the file
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            total_entries = sum(1 for line in f)
    except Exception as ex:
        print("An error occurred while reading the file:", ex)
        return None
    return total_entries

def main():
    """
    Main function to interact with the user, compute the function values,
    and handle file operations according to user input.

    """
    session_results = []  # Store results of the current session
    created_files = []  # Keep track of created files in the session
    last_file = None  # Keep track of the last opened file
    max_files = 5  # Maximum number of files allowed to be created
    while True:
        x_input = input("Enter the function argument: ")
        if x_input.strip() == "Кінець":
            if not session_results:
                print("No results to save.")
                break
            save_choice = input("Would you like to save the results to a file? (Yes/No): ").strip()
            if save_choice.lower() == 'no':
                print("Data not saved to file")
                break
            elif save_choice.lower() == 'yes':
                if last_file:
                    save_last_choice = input(f"Save results to the file '{last_file}'? (Yes/No): ").strip()
                    if save_last_choice.lower() == 'yes':
                        total_entries = save_results_to_file(last_file, session_results)
                        if total_entries is not None:
                            print(f"Data saved to file '{last_file}'. Total number of entries: {total_entries}")
                        break
                    elif save_last_choice.lower() == 'no':
                        if len(created_files) < max_files:
                            file_prompt = "Enter the name of an existing file or a new file (up to 5 letters, Latin/Ukrainian letters and/or digits) or '*' to cancel and exit: "
                        else:
                            file_prompt = "Enter the name of an existing file or '*' to cancel and exit: "
                        filename = input(file_prompt).strip()
                        if filename == '*':
                            print("Data not saved to file")
                            break
                        else:
                            if not (1 <= len(filename) <= 5):
                                print("Filename must be 1 to 5 characters long.")
                                continue
                            if not re.match(r'^[a-zA-Zа-яА-Яіїєє0-9]{1,5}$', filename):
                                print("Filename must contain only Latin/Ukrainian letters and digits.")
                                continue
                            if filename not in created_files and len(created_files) >= max_files:
                                print("Cannot create new file. Maximum number of files reached.")
                                continue
                            total_entries = save_results_to_file(filename, session_results)
                            if total_entries is not None:
                                print(f"Data saved to file '{filename}'. Total number of entries: {total_entries}")
                                if filename not in created_files:
                                    created_files.append(filename)
                                last_file = filename
                            break
                    else:
                        print("Invalid input. Please answer 'Yes' or 'No'.")
                        continue
                else:
                    file_prompt = "Enter a new file name (up to 5 letters, Latin/Ukrainian letters and/or digits) or '*' to cancel and exit: "
                    filename = input(file_prompt).strip()
                    if filename == '*':
                        print("Data not saved to file")
                        break
                    else:
                        if not (1 <= len(filename) <= 5):
                            print("Filename must be 1 to 5 characters long.")
                            continue
                        if not re.match(r'^[a-zA-Zа-яА-Яіїєє0-9]{1,5}$', filename):
                            print("Filename must contain only Latin/Ukrainian letters and digits.")
                            continue
                        total_entries = save_results_to_file(filename, session_results)
                        if total_entries is not None:
                            print(f"Data saved to file '{filename}'. Total number of entries: {total_entries}")
                            created_files.append(filename)
                            last_file = filename
                        break
            else:
                print("Invalid input. Please answer 'Yes' or 'No'.")
                continue
        else:
            try:
                x = float(x_input)
            except ValueError:
                print("Invalid input for x. Please enter a number or 'Кінець' to exit.")
                continue
            e_input = input("Enter the precision: ")
            try:
                e = float(e_input)
                if not (0 < e < 1):
                    print("Precision e must be in (0;1).")
                    continue
            except ValueError:
                print("Invalid input for e. Please enter a number between 0 and 1.")
                continue
            try:
                start_time = time.time()
                f_x_e, N = compute_ln_sin_x(x, e)
                computation_time = time.time() - start_time
                if computation_time > 15 * 60:
                    print("Cannot achieve desired precision within reasonable time.")
                    continue
                print(f"f(x, e) = {f_x_e:.12f}")
                print(f"N(x, e) = {N}")
                result = {
                    'x': x,
                    'e': e,
                    'f_x_e': f_x_e,
                    'N': N
                }
                session_results.append(result)
            except TimeoutError as te:
                print(te)
                continue
            except Exception as ex:
                print("An error occurred:", ex)
                continue
    # Program ends here

if __name__ == "__main__":
    main()
