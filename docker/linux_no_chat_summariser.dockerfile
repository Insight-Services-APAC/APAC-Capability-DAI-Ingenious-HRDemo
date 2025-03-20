# syntax=docker/dockerfile:1
FROM docker.io/library/python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Expose port 80
EXPOSE 80

# Set the working directory
WORKDIR /ingen_app

# Add required dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        sudo \
        lsof \
        unixodbc \
        unixodbc-dev \
        libodbc2 \
        libodbccr2 \
        git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Use pip to install the `ingenious` package from the GitHub repository
#RUN pip install git+https://github.com/Insight-Services-APAC/Insight_Ingenious.git#egg=ingenious --force-reinstall
RUN pip install git+https://github.com/Insight-Services-APAC/Insight_Ingenious.git@v0.0.10 --force-reinstall

# Copy the application files into the container
COPY ./ingenious_extensions /ingen_app/ingenious_extensions
COPY ./tmp /ingen_app/tmp

# Set the command to run the app
CMD ["ingen_cli", "run-rest-api-server"]
#CMD ["ingen_cli" ,"run-prompt-tuner"]