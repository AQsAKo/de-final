FROM prefecthq/prefect:2.6.6-python3.11

RUN apt-get update -y
RUN apt-get install unzip wget curl -y
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install dbt-core dbt-bigquery
RUN pip install prefect prefect-gcp prefect-dbt[cli] google-cloud-bigquery-storage
WORKDIR /home/final

RUN curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-cli-429.0.0-linux-x86_64.tar.gz
RUN tar -xf google-cloud-cli-429.0.0-linux-x86_64.tar.gz
RUN ./google-cloud-sdk/install.sh -q
RUN PATH=/home/final/google-cloud-sdk/bin:$PATH
RUN wget https://releases.hashicorp.com/terraform/1.4.6/terraform_1.4.6_linux_amd64.zip 
#COPY terraform_1.4.6_linux_amd64.zip terraform_1.4.6_linux_amd64.zip
RUN unzip terraform_1.4.6_linux_amd64.zip -d /usr/bin

RUN pip install tqdm
ENV PATH="$PATH:/home/final/google-cloud-sdk/bin"
RUN mkdir gtfs
COPY terraform terraform
COPY flows flows
COPY wmata_bus wmata_bus
COPY splitter.sh splitter.sh



CMD [ "bash" ]