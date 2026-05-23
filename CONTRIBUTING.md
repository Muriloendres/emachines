# Contributing to emachines

Thank you for contributing to emachines! This document explains how we work together to build this project collaboratively.

## Getting Started (Using Docker)

1. **Clone the repository**
   ```bash
   git clone https://github.com/NaveenDeepak/emachines.git
   cd emachines
   ```

2. **Set up Docker environment** (see [SETUP.md](./SETUP.md))
   ```bash
   docker-compose up
   # Then open http://localhost:8888 in your browser
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Develop in Jupyter notebooks** (see section below)

5. **Push your branch** and open a Pull Request

6. **Wait for review** and address any feedback

7. **Merge** once approved by the maintainer

### ✅ Why Docker?

Docker ensures **everyone has the exact same environment**:
- ✓ Same Python version (3.10)
- ✓ Same nbdev installation
- ✓ Same dependencies and versions
- ✓ Same JupyterLab setup
- ✓ Works on macOS, Windows, and Linux identically

**Setup takes 2 minutes:** `docker-compose up` and you're done! 🚀

## Developing with nbdev

This project uses **nbdev** for notebook-driven development. This means:
- Code and documentation live together in Jupyter notebooks
- Easy to explain logic and reasoning
- Tests are embedded in notebooks
- Python modules are auto-generated from notebooks

### Notebook Structure

All development happens in `nbs/` directory:

```
nbs/
├── 00_core.ipynb           # Core functionality
├── 01_utilities.ipynb      # Utility functions
├── index.ipynb             # Documentation/overview
└── README.ipynb            # Setup and usage guide
```

Each notebook corresponds to a Python module in `/emachines/`.

### How to Develop a Feature

1. **Open JupyterLab** (automatically running with `docker-compose up`)
2. **Navigate to `nbs/` folder**
3. **Create or edit a notebook** (e.g., `02_my_feature.ipynb`)
4. **Add cells with code and documentation**
   ```python
   # Cell 1: Imports
   import numpy as np
   from emachines.core import BaseClass
   
   # Cell 2: Implementation
   def my_function(x: float) -> float:
       """
       My function description.
       
       Args:
           x: Input value
           
       Returns:
           Processed value
       """
       return x * 2
   
   # Cell 3: Tests
   assert my_function(5) == 10
   print("✓ Test passed!")
   
   # Cell 4: Examples
   result = my_function(3.14)
   print(f"Result: {result}")
   ```

5. **Add directives for nbdev** (special comments)
   - `#| export` - Export this cell to Python
   - `#| hide` - Hide from documentation
   - `#| default_exp module_name` - Set module for exports

### Example nbdev Cell Structure

```python
#| default_exp core

#| export
def calculate_winding_factor(slots: int, poles: int) -> float:
    """
    Calculate winding factor for electric machine.
    
    Args:
        slots: Number of stator slots
        poles: Number of poles
        
    Returns:
        Winding factor value
    """
    return (slots / (poles * 3))


#| hide
# This is a test cell - hidden from documentation
assert calculate_winding_factor(36, 4) > 0
print("✓ Winding factor calculation works")
```

### Building Python from Notebooks

After editing notebooks, export to Python:

**In container terminal:**
```bash
docker-compose exec emachines-dev bash
nbdev_build_lib
```

**Or in JupyterLab terminal:**
```bash
nbdev_build_lib
```

This creates/updates Python files in `/emachines/` from your notebooks.

### Running Tests

Tests can be run in three ways:

**1. Inside notebook cells** (best for development)
```python
assert result == expected_value
```

**2. Run all notebook tests**
```bash
nbdev_test_nbs
```

**3. Traditional pytest** (for separate test files)
```bash
pytest tests/
```

### Documentation

Documentation is auto-generated from notebooks:
- Cell markdown becomes documentation
- Code becomes examples
- Tests become validation

**The more detailed your notebooks, the better the documentation!**

### Notebook Conventions

1. **Cell order matters** - Start with imports, then implementation
2. **Use markdown cells** - Explain your code
3. **Include examples** - Show how to use functions
4. **Add tests** - Validate your code works
5. **Use type hints** - Help readers understand input/output
6. **Document assumptions** - Explain scientific/mathematical reasoning

### Example PR with nbdev

**Before (notebook in `nbs/01_feature.ipynb`):**
```
- Feature code
- Explanation markdown
- Working examples
- Tests validating logic
```

**After building (`nbdev_build_lib`):**
```
- `/emachines/feature.py` - Auto-generated Python module
- Documentation auto-generated from notebook
- Tests extracted and ready to run
```

**Your PR includes:**
- The notebook (readable, explainable)
- Auto-generated Python files
- Clear commit message

---

## Branch Naming Conventions

Use descriptive branch names:
- `feature/add-authentication` - New features
- `fix/login-bug` - Bug fixes
- `docs/update-readme` - Documentation
- `refactor/optimize-query` - Code improvements
- `test/add-coverage` - Testing

**Avoid:** Generic names like `fix`, `update`, `work`, `temp`

## Commit Message Guidelines

Write clear, descriptive commit messages:

**Good Examples:**
```
Add user authentication module with JWT
Fix data import error in CSV parser
Update documentation for API endpoints
Refactor database connection pooling
```

**Bad Examples:**
```
fix
update
test
stuff
```

**Format:**
- Use imperative mood: "Add feature" not "Added feature"
- Keep first line under 50 characters
- Add detailed explanation in the body if needed:
  ```
  Add user authentication module with JWT
  
  - Implements JWT token generation and validation
  - Adds password hashing with bcrypt
  - Includes login and logout endpoints
  ```

## Code Style & Standards

### Python Code Quality
- **Style Guide**: PEP 8
- **Type Hints**: Required for new functions/classes
- **Docstrings**: Include for all public functions
- **Linting**: Run `pylint` before pushing
- **Formatting**: Use `black` for consistent formatting

### Testing
- **Test Framework**: pytest
- **Coverage**: Aim for >80% code coverage
- **Naming**: Test files as `test_*.py`, test functions as `test_*`
- **Run tests locally**: `pytest tests/` before pushing

### Example Function
```python
def fetch_user_data(user_id: int) -> dict:
    """
    Fetch user data from the database.
    
    Args:
        user_id: The unique identifier for the user
        
    Returns:
        A dictionary containing user information
        
    Raises:
        ValueError: If user_id is invalid
    """
    if user_id <= 0:
        raise ValueError("user_id must be positive")
    return get_user_from_db(user_id)
```

## Pull Request Process

### Before Creating a PR
1. **Update your branch** with the latest `main`: `git pull origin main`
2. **Run tests locally**: `pytest tests/`
3. **Run linter**: `pylint src/`
4. **Run formatter**: `black .`
5. **Update documentation** if behavior changed
6. **Check for merge conflicts** and resolve if any

### Creating a PR
1. **Use the PR template** (auto-filled when you open a PR)
2. **Write a clear title**: "Add user authentication" not "Update stuff"
3. **Describe what changed** and why
4. **Link related issues**: "Closes #42"
5. **Request review** from the maintainer
6. **Be responsive** to feedback and suggestions

### PR Review Checklist
Your PR should pass these checks before merge:
- ✓ All tests pass
- ✓ Code linting passes
- ✓ No merge conflicts
- ✓ Documentation is updated
- ✓ Commit messages are clear
- ✓ No sensitive information (API keys, passwords) in code

## Review Process

### For Contributors
- **Be responsive** to feedback (turnaround: 24-48 hours)
- **Don't take criticism personally** - it's about the code
- **Ask questions** if feedback isn't clear
- **Make requested changes** and push updates
- **Don't force-push** after review started

### For Maintainers
- **Review promptly** (within 24-48 hours)
- **Be constructive** and respectful
- **Explain why** changes are needed
- **Approve and merge** once all checks pass

## Common Issues & Solutions

### My tests are failing
```bash
# Run tests with verbose output
pytest tests/ -v

# Run a specific test
pytest tests/test_file.py::test_function
```

### My code has style issues
```bash
# Check style
pylint src/

# Auto-format code
black .
```

### I have merge conflicts
```bash
# Update your branch
git pull origin main

# Resolve conflicts in your editor
# Then commit and push
git add .
git commit -m "Resolve merge conflicts"
git push
```

### I need to update my PR
```bash
# Make changes
git add .
git commit -m "Address review feedback"
git push  # Don't force-push!
```

## Project Structure

```
emachines/
├── src/              # Main source code
├── tests/            # Test files
├── docs/             # Documentation
├── data/             # Data files (if applicable)
├── README.md         # Project overview
├── requirements.txt  # Python dependencies
└── .github/          # GitHub configuration
```

## Getting Help

- **Bug reports**: Open an Issue with details
- **Feature requests**: Discuss in Issues first
- **Questions**: Ask in the Issue or PR discussion
- **Design decisions**: Create an Issue for team discussion

## Questions or Concerns?

If you have questions about the contribution process, feel free to ask in a GitHub Issue or discussion. We want to make contributing as smooth as possible!

---

**Happy contributing! 🚀**
