import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse

def check_headers(url):
    print(f"[*] Checking headers for {url}")
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        for header, value in headers.items():
            print(f"{header}: {value}")
    except Exception as e:
        print(f"Error: {e}")

def scan_ports(hostname, ports=[80, 443, 21, 22, 8080]):
    print(f"[*] Scanning ports on {hostname}")
    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((hostname, port))
                if result == 0:
                    print(f"[+] Port {port} is open")
        except Exception as e:
            print(f"Error scanning port {port}: {e}")

def xss_test(url):
    print(f"[*] Performing basic XSS test on {url}")
    test_payload = "<script>alert('XSS')</script>"
    try:
        response = requests.get(url, params={"q": test_payload}, timeout=10)
        if test_payload in response.text:
            print("[!] Potential XSS vulnerability detected!")
        else:
            print("[+] No XSS vulnerability detected.")
    except Exception as e:
        print(f"Error during XSS test: {e}")

def main():
    target = input("Enter the target URL (e.g., https://example.com): ").strip()
    parsed_url = urlparse(target)
    hostname = parsed_url.hostname
    if not hostname:
        print("Invalid URL.")
        return
    check_headers(target)
    scan_ports(hostname)
    xss_test(target)

if __name__ == "__main__":
    main()
