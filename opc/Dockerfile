FROM ubuntu:18.04
RUN \
       apt update \
    && apt upgrade -y \
    && apt install -y software-properties-common python3 python3-setuptools python3-pip \
    && add-apt-repository ppa:gijzelaar/snap7 \
    && apt update \
    && apt install -y libsnap7-dev libsnap7-1
WORKDIR /code
ADD requiremens.txt .
RUN pip3 install -r requiremens.txt
ADD . .
EXPOSE 5001
ENTRYPOINT "python3" "main.py"