ARG PYTHON_VERSION=3.13.7
FROM python:${PYTHON_VERSION}-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.5.1 /uv /uvx /bin/

ENV NODE_MAJOR=22

# Install System Dependencies
RUN apt-get update \
    && apt-get install --no-install-recommends -y git make gringo

# Install Node.js as it is needed for draco1 vs draco2 comparison demos
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl gnupg \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list \
    && apt-get update && apt-get install nodejs -y \
    && npm install -g npm@latest

WORKDIR /home/app

# Copy the project source code and install dependencies
COPY . .
RUN make install
