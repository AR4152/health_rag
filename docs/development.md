# Development

## How to Start Developing

1. **Clone the repository** and navigate into the project directory:

   ```bash
   git clone https://github.com/AR4152/health_rag.git
   cd health_rag
   ```

2. **Install dependencies:**

   Install the main development dependencies from `requirements-dev.txt`:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Set up pre-commit hooks (recommended):**

   ```bash
   pre-commit install
   ```

4. You are now ready to start developing! Refer to [MLHub](https://survivor.togaware.com/mlhub/) for more details.


## Code Style

This project uses modern Python tooling for consistent code style, type safety, and maintainability.

### Linting and Formatting

This project uses **[Ruff](https://docs.astral.sh/ruff/)** for linting and auto-formatting. Relevant settings are defined in [`pyproject.toml`](../pyproject.toml).

**Usage:**

To lint the code:

```bash
ruff check .
```

To auto-fix issues:

```bash
ruff check . --fix
```

To auto-format:

```bash
ruff format .
```

### Static Type Checking

This project uses [Mypy](http://mypy-lang.org/) in **strict mode**, which enforces rigorous type safety.


**Usage:**

Run type checks:

```bash
mypy .
```

### Pre-commit Hooks

This project uses **pre-commit** to automatically check code quality before each commit.


**Setup:**

```bash
pip install pre-commit
pre-commit install
```

**Run manually:**

```bash
pre-commit run --all-files
```

Hooks will run automatically every time you commit.

### Docstrings

This project follows **Google’s Python docstring style**. All public modules, classes, and functions should include docstrings formatted according to the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).
