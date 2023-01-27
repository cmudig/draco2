FROM python:3.10.9-buster

# Create user with a home directory
ARG NB_USER="draco2"
ARG NB_UID="1000"
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}/app

# Install dependencies using Poetry
RUN python -m pip install --upgrade pip &&  \
    pip install poetry
COPY pyproject.toml poetry.lock ./
# Purposefully not using --no-dev here to install dev dependencies needed for Jupyter Notebooks
RUN poetry config virtualenvs.create false && \
    poetry install

# Copy the project source code
COPY . .

# Install draco2 from local sources, needed for notebooks
RUN pip install -e .

# Grant permissions to the notebook user
RUN chown -R ${NB_USER} ${HOME}
USER ${NB_USER}
