FROM python:3.11.6-bookworm

# Install Node.js as it is needed as a dev dependency
ENV NODE_MAJOR=20
RUN apt-get update && apt-get install -y ca-certificates curl gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install nodejs -y && \
    npm install -g npm@latest

# Install Clingo so that it is available as an executable for the draco1 vs. draco2 comparison notebook
RUN apt-get update && apt-get install -y gringo

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
# Installing all dependency groups to build a complete dev environment
COPY pyproject.toml poetry.lock ./
RUN python -m pip install --upgrade pip &&  \
    pip install poetry  && \
    poetry config virtualenvs.create false && \
    poetry install --with web

# Copy the project source code
COPY . .

# Install draco2 from local sources, needed for notebooks
RUN pip install -e .

# Grant permissions to the notebook user
RUN chown -R ${NB_USER} ${HOME}
USER ${NB_USER}
