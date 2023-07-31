FROM ubuntu:mantic

# Installation ttyd
RUN apt update
RUN apt install -y build-essential cmake git libjson-c-dev libwebsockets-dev
RUN git clone https://github.com/tsl0922/ttyd.git

RUN mkdir ttyd/build
WORKDIR /ttyd/build

RUN cmake ..
RUN make && make install

WORKDIR /home/ubuntu

# Install necessary tool to solve CTF
RUN apt install -y nmap iproute2 sqlmap dsniff tcpdump netcat-traditional vim nano john

# Copy password dictionary

RUN mkdir dictionaries
COPY rockyou-50.txt dictionaries

CMD ["ttyd", "-W" ,"bash"]
