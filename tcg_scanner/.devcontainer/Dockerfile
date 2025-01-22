FROM --platform=linux/amd64 python:3.10-slim-bookworm

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Install system dependencies and development tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    curl \
    unzip \
    vim \
    zsh \
    zip \
    tesseract-ocr \
    libgl1 \
    libxcb-cursor0 libxcb-xinerama0 libxcb-util1 \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - 

# Add Poetry to PATH
ENV PATH="${POETRY_HOME}/bin:$PATH"

# Set zsh as default shell
RUN chsh -s $(which zsh)

# Create and set workspace directory
WORKDIR /workspace

# Switch back to dialog for any ad-hoc use of apt-get
ENV DEBIAN_FRONTEND=dialog

# Set default shell to zsh
CMD ["zsh"]
