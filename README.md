# Hacker-Helper

Small web app for templated recon for pentesting and CTFs
By default, the scanner runs an nmap scan, and several gobuster checks for file, directory, and vhost enumeration
You can add https support by selecting the SSL option in the scan page and selecting the DNS option will perform subdomain bruteforcing as well
A list of all scans performed can be found [here](https://github.com/edrapac/Hacker-Helper/blob/main/app/entrypoint.sh)

### Usage
Navigate to the root directory and run `docker-compose up -d`
This will start a hedgedoc instance on 127.0.0.1:3000 for reporting and the scanner at 127.0.0.1:5002