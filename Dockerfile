FROM python:3.8-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Clone the s4pred repository
RUN git clone https://github.com/psipred/s4pred

WORKDIR /app/s4pred

RUN pip install torch
RUN pip install Bio

# Download s4pred
RUN wget http://bioinfadmin.cs.ucl.ac.uk/downloads/s4pred/weights.tar.gz \
    && tar -xvzf weights.tar.gz \
    && rm weights.tar.gz


# Set PATH and other necessary environment variables
ENV PATH="/app/s4pred:${PATH}"

