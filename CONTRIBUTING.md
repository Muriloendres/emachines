# Contributing to emachines

Thank you for contributing to emachines! This document explains how we work together to build this project collaboratively.

## Getting Started

1. **Fork or clone** the repository
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** with clear, focused commits
4. **Push your branch** and open a Pull Request
5. **Wait for review** and address any feedback
6. **Merge** once approved by the maintainer

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
