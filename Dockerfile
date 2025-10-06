FROM  ubuntu:latest
RUN apt update && apt -y install nmap sudo gobuster tar curl
RUN curl https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-large-directories.txt --create-dirs -o /usr/share/wordlists/raft-large-directories.txt
RUN curl https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/raft-large-files.txt --create-dirs -o /usr/share/wordlists/raft-large-files.txt
RUN curl https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/DNS/subdomains-top1million-5000.txt --create-dirs -o /usr/share/wordlists/subdomains-top1million-5000.txt
COPY entrypoint.sh /entrypoint.sh
RUN sudo chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]