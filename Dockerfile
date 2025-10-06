FROM python:3.8
RUN apt update && apt -y install nmap sudo gobuster tar curl python3 python3-pip
RUN pip3 install flask requests flask-marshmallow
EXPOSE 5001
RUN curl https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-large-directories.txt --create-dirs -o /usr/share/wordlists/raft-large-directories.txt
RUN curl https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-large-files.txt --create-dirs -o /usr/share/wordlists/raft-large-files.txt
RUN curl https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/DNS/subdomains-top1million-5000.txt --create-dirs -o /usr/share/wordlists/subdomains-top1million-5000.txt
COPY entrypoint.sh /app/entrypoint.sh
WORKDIR /app
RUN sudo chmod +x entrypoint.sh
CMD python app.py