FROM python:3.10.8-buster
WORKDIR /usr/src/app

# Make /tmp writable, needed for Jupyter Notebooks
ENV HOME=/tmp

# Install dependencies using Poetry
RUN python -m pip install --upgrade pip &&  \
    pip install poetry
COPY pyproject.toml poetry.lock ./
# Purposely not using --no-dev here to install dev dependencies needed for Jupyter Notebooks
RUN poetry config virtualenvs.create false && \
    poetry install && \
    pip install git+https://github.com/cmudig/draco2.git#egg=draco  # Install Draco2 from git, needed for notebooks

# Copy the project source code
COPY . .
