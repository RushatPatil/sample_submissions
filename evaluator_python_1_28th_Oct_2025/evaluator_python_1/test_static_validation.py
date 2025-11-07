"""
Test script for Python static validation
Run this to verify that the static validation tools are working correctly
"""

import sys
import subprocess
from pathlib import Path


def check_pylint():
    """Check if pylint is installed and working"""
    try:
        result = subprocess.run(
            ["pylint", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✓ pylint is installed: {version}")
            return True
        else:
            print("✗ pylint is installed but not responding correctly")
            return False
    except FileNotFoundError:
        print("✗ pylint is NOT installed")
        print("  Install with: pip install pylint>=3.0.0")
        return False
    except Exception as e:
        print(f"✗ Error checking pylint: {e}")
        return False


def check_bandit():
    """Check if bandit is installed and working"""
    try:
        result = subprocess.run(
            ["bandit", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ bandit is installed: {version}")
            return True
        else:
            print("✗ bandit is installed but not responding correctly")
            return False
    except FileNotFoundError:
        print("✗ bandit is NOT installed")
        print("  Install with: pip install bandit>=1.7.0")
        return False
    except Exception as e:
        print(f"✗ Error checking bandit: {e}")
        return False


def check_py_compile():
    """Check if py_compile is available"""
    try:
        import py_compile
        print("✓ py_compile is available (Python standard library)")
        return True
    except ImportError:
        print("✗ py_compile is NOT available (this should not happen)")
        return False


def check_validators_module():
    """Check if the validators module can be imported"""
    try:
        # Add src to path
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))

        from validators.python_validator import PythonValidator
        print("✓ PythonValidator module can be imported")

        # Try to instantiate
        validator = PythonValidator()
        print("✓ PythonValidator can be instantiated")
        return True
    except ImportError as e:
        print(f"✗ Cannot import PythonValidator: {e}")
        return False
    except Exception as e:
        print(f"✗ Error with PythonValidator: {e}")
        return False


def check_generic_evaluator():
    """Check if the generic evaluator module can be imported"""
    try:
        # Add src to path if not already there
        src_path = Path(__file__).parent / "src"
        if str(src_path) not in sys.path:
            sys.path.insert(0, str(src_path))

        from evaluators.generic_evaluator import GenericEvaluator
        print("✓ GenericEvaluator module can be imported")
        return True
    except ImportError as e:
        print(f"✗ Cannot import GenericEvaluator: {e}")
        return False
    except Exception as e:
        print(f"✗ Error with GenericEvaluator: {e}")
        return False


def main():
    """Run all checks"""
    print("=" * 60)
    print("Static Validation Installation Check")
    print("=" * 60)
    print()

    print("Checking required tools:")
    print("-" * 60)

    checks = [
        check_py_compile(),
        check_pylint(),
        check_bandit(),
    ]

    print()
    print("Checking Python modules:")
    print("-" * 60)

    module_checks = [
        check_validators_module(),
        check_generic_evaluator(),
    ]

    print()
    print("=" * 60)

    all_passed = all(checks) and all(module_checks)

    if all_passed:
        print("✓ All checks passed! Static validation is ready to use.")
        print()
        print("Next steps:")
        print("1. Start the server: python src/main.py")
        print("2. Test the /generic_evaluation endpoint")
        print("3. See QUICK_START.md for usage examples")
    else:
        print("✗ Some checks failed. Please install missing dependencies:")
        print("   pip install -r requirements.txt")

    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
