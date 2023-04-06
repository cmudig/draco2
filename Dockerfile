FROM python:3.10.11-bullseye

# Install Node.js as it is needed as a dev dependency
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    lsb-release &&  \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - &&  \
    apt-get install -y nodejs && \
    npm install -g npm@latest

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
    pip install poetry==1.4.0
COPY pyproject.toml poetry.lock ./
# Installing all dependency groups to build a complete dev environment
RUN poetry config virtualenvs.create false && \
    poetry install --with web

# Copy the project source code
COPY . .

# Install draco2 from local sources, needed for notebooks
RUN pip install -e .

# Grant permissions to the notebook user
RUN chown -R ${NB_USER} ${HOME}
USER ${NB_USER}
