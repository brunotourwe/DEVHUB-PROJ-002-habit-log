# Base Devcontainer
# Provides the canonical development environment for the Dev Hub

FROM node:20-bookworm-slim

# Avoid interactive prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install minimal system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
    openssh-client \
    less \
    && rm -rf /var/lib/apt/lists/*

# Enable corepack and pin pnpm
RUN corepack enable \
    && corepack prepare pnpm@10.0.0 --activate

# Create non-root user
ARG USERNAME=dev
ARG USER_UID=1000
ARG USER_GID=1000

RUN set -eux; \
    existing_user=""; \
    if getent passwd ${USER_UID} >/dev/null; then \
        existing_user="$(getent passwd ${USER_UID} | cut -d: -f1)"; \
    fi; \
    if [ -n "$existing_user" ]; then \
        if [ "$existing_user" != "${USERNAME}" ]; then \
            usermod -l ${USERNAME} "$existing_user"; \
            usermod -d /home/${USERNAME} -m ${USERNAME}; \
        fi; \
    else \
        if ! getent group ${USER_GID} >/dev/null; then \
            groupadd --gid ${USER_GID} ${USERNAME}; \
        fi; \
        useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}; \
    fi

USER ${USERNAME}
WORKDIR /workspace

# Ensure predictable shell
SHELL ["/bin/bash", "-c"]

# Default command (VS Code will override)
CMD ["bash"]
