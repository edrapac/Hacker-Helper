#!/bin/bash
set -ou pipefail
export DEBIAN_FRONTEND=noninteractive

# Default values
SSL="no"
DNS_SCAN="no"

# Parse arguments
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    --ssl)
      SSL="yes"
      shift # past flag
      ;;
    --dns)
      DNS_SCAN="yes"
      shift # past flag
      ;;
    *)
      POSITIONAL+=("$1") # save positional arg
      shift
      ;;
  esac
done
set -- "${POSITIONAL[@]}" # restore positional params

HOST="${1:-}"
if [[ -z "$HOST" ]]; then
  echo "Usage: $0 [--ssl] [--dns] <host>"
  exit 1
fi

# Extract hostname without port for nmap
HOST_ONLY="${HOST%%:*}"

sudo nmap -sS -A -Pn -sV -oN /tmp/nmap.txt "$HOST_ONLY"
# make this conditional as well
#sudo nmap -p- -oN /tmp/nmap_allports.txt "$HOST_ONLY"

if [[ "$SSL" == "yes" ]]; then
  URL="https://$HOST"
else
  URL="http://$HOST"
fi

gobuster dir -u "$URL" -w /usr/share/wordlists/raft-large-directories.txt -o /tmp/gobuster_dirs.txt -b 404 -t 30
gobuster dir -u "$URL" -w /usr/share/wordlists/raft-large-files.txt -o /tmp/gobuster_files.txt -b 404 -t 30
gobuster vhost -u "$URL" -t 50 -w /usr/share/wordlists/subdomains-top1million-5000.txt -o /tmp/gobuster_vhosts.txt

if [[ "$DNS_SCAN" == "yes" ]]; then
  gobuster dns -d "$HOST" -w /usr/share/wordlists/subdomains-top1million-5000.txt -t 30 -o /tmp/gobuster_dns.txt
fi