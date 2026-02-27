# src/calculator.py
# Calculator functions for the application

# FIX: Added math import for factorial and isqrt usage
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
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def power(base: float, exp: int) -> float:
    """Return base raised to the power of exp."""
    # FIX: Added guard for zero base with negative exponent to give descriptive error
    if base == 0 and exp < 0:
        raise ValueError("Cannot raise zero to a negative power")
    # FIX: Corrected logic error — was base ** (exp + 1), now base ** exp
    return base ** exp


# FIX: Updated modulo to accept float arguments for a consistent API surface matching divide/multiply
def modulo(a: float, b: float) -> float:
    """Return a modulo b. Accepts floats for consistency with other arithmetic functions."""
    if b == 0:
        raise ValueError("Cannot modulo by zero")
    return a % b


# FIX: Changed parameter type annotation from untyped list to list[float] for type safety
def average(numbers: list[float]) -> float:
    """Return the average of a list of numbers."""
    if not numbers:
        raise ValueError("Cannot compute average of empty list")
    # FIX: Added runtime type validation to catch non-numeric elements with a descriptive error
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise TypeError("All elements must be numeric")
    return sum(numbers) / len(numbers)


def factorial(n: int) -> int:
    """Return the factorial of n."""
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    # FIX: Added upper bound guard to prevent resource exhaustion from very large inputs
    if n > 10000:
        raise ValueError("Input too large; n must be <= 10000")
    # FIX: Replaced manual iterative loop with math.factorial (C implementation, faster and maintained)
    return math.factorial(n)


def is_prime(n: int) -> bool:
    """Return True if n is a prime number."""
    if n < 2:
        return False
    # FIX: Replaced floating-point int(n ** 0.5) with math.isqrt(n) for exactness and correctness on large n
    for i in range(2, math.isqrt(n) + 1):
        if n % i == 0:
            return False
    return True