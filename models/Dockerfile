FROM nvidia/cuda:12.8.0-devel-ubuntu22.04

WORKDIR /app

# Set proxy
ENV http_proxy=http://172.30.188.150:3128
ENV https_proxy=http://172.30.188.150:3128
ENV no_proxy=localhost,127.0.0.0/8,172.24.0.0/16,*.azure.com,*.azure.net,*.azureedge.net,oai-gpt4-us2.openai.azure.com

# Gunakan bash sebagai shell default
SHELL ["/bin/bash", "-c"]

# Install system dependencies
RUN sed -i 's|http://archive.ubuntu.com|https://archive.ubuntu.com|g' /etc/apt/sources.list && \
    sed -i 's|http://security.ubuntu.com|https://security.ubuntu.com|g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y wget git curl build-essential libnvidia-compute-525 libnvidia-container-tools nvidia-container-toolkit && \
    apt-get clean

# Install Miniconda
RUN wget -O miniconda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash miniconda.sh -b -p /opt/miniconda && \
    rm miniconda.sh

# Tambahkan conda ke PATH
ENV PATH="/opt/miniconda/bin:$PATH"

# Copy entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Buat environment Conda dan install package
RUN conda create -n vllm python=3.10 -y

# Gunakan entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
 