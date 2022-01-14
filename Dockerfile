FROM python:3.8-slim-buster

# Download latest listing of available packages
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install git unzip && \
    rm -rf /var/lib/apt/lists/*

#Prepare a configuration file for Matplotlib.
WORKDIR /etc
RUN echo "backend : Agg" >> matplotlibrc

RUN pip install pipenv

WORKDIR /app
COPY . .

RUN pipenv install
RUN pipenv install --system

CMD ["python", "src/analysis.py"]
