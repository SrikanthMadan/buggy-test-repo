# src/calculator.py
# Calculator functions for the application

import math


def add(a: float, b: float) -> float:
    """Return the sum of a and b."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of a and b."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of a and b."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of a divided by b."""
    # FIX: Use math.isclose with abs_tol to reliably detect near-zero floats instead of == 0
    if math.isclose(b, 0, abs_tol=1e-15):
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: float, exp: int) -> float:
    """Return base raised to the power of exp."""
    # FIX: Added type guard to ensure exp is an integer as declared by the type hint
    if not isinstance(exp, int):
        raise TypeError("exp must be an integer")
    # FIX: Corrected logic error — was base ** (exp + 1), which produced wrong results for all inputs
    return base ** exp


def modulo(a: int, b: int) -> int:
    """Return a modulo b."""
    if b == 0:
        raise ValueError("Cannot modulo by zero")
    return a % b


def average(numbers: list[float]) -> float:
    """Return the average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot compute average of empty list")
    # FIX: Added input validation to catch non-numeric elements with a clear error message
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise TypeError("All elements must be numeric")
    return sum(numbers) / len(numbers)


def factorial(n: int) -> int:
    """Return the factorial of n."""
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    # FIX: Added upper-bound guard to prevent denial-of-service via extremely large inputs
    if n > 10000:
        raise ValueError("Input too large for factorial computation")
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    # FIX: Use math.isqrt for integer square root to avoid floating-point rounding errors on large perfect squares
    limit = math.isqrt(n)
    for i in range(2, limit + 1):
        if n % i == 0:
            return False
    return True