# Development environment for emachines
# Ensures consistent environment across macOS, Windows, and Linux
# Python 3.10 with nbdev, Jupyter, and all dependencies

FROM python:3.10-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /workspace/

# Install Python dependencies from pyproject.toml
RUN pip install --upgrade pip setuptools wheel

# Install the project in development mode with all dependencies
RUN pip install -e ".[dev]"

# Install nbdev and additional dev tools
RUN pip install \
    nbdev>=2.3.0 \
    jupyterlab>=4.0.0 \
    black>=23.7.0 \
    isort>=5.12.0 \
    pylint>=2.17.0 \
    flake8>=6.0.0 \
    mypy>=1.4.0 \
    pre-commit>=3.3.0

# Install pre-commit hooks
RUN pre-commit install --install-hooks || true

# Expose JupyterLab port
EXPOSE 8888

# Set up Jupyter configuration
RUN jupyter notebook --generate-config && \
    echo "c.NotebookApp.ip = '0.0.0.0'" >> ~/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> ~/.jupyter/jupyter_notebook_config.py

# Default command: start JupyterLab
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--allow-root", "--no-browser"]
