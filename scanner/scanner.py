import argparse
import socket
import pickle
import ipaddress

def scan_ports(target, ports):
    results = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            results.append(f"Host: {target}\tPorts: {port}/open/tcp////")
        sock.close()
    return results

def save_scan_results(results):
    with open('scan_results.pkl', 'wb') as f:
        pickle.dump(results, f)

def load_scan_results():
    try:
        with open('scan_results.pkl', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def print_scan_results(target, results):
    if results:
        print(f"*Target - {target}: Full scan results:*")
        for result in results:
            print(result)
    else:
        print(f"*Target - {target}: No new records found in the last scan.*")

def main(targets):
    ports = [22, 25, 80]  # Define the ports to scan
    previous_results = load_scan_results()
    current_results = []
    for target in targets:
        if "-" in target:
            start_ip, end_ip = target.split("-")
            start_ip = ipaddress.ip_address(start_ip.strip())
            end_ip = ipaddress.ip_address(end_ip.strip())
            ip_range = ipaddress.summarize_address_range(start_ip, end_ip)
            for network in ip_range:
                for ip in network:
                    current_results.extend(scan_ports(str(ip), ports))
        else:
            current_results.extend(scan_ports(target, ports))
    save_scan_results(current_results)
    if current_results == previous_results:
        for target in targets:
            print_scan_results(target, [])
    else:
        for target in targets:
            print_scan_results(target, current_results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Port scanner")
    parser.add_argument("targets", nargs="+", help="IP addresses or IP ranges to scan")
    args = parser.parse_args()
    targets = []
    for target in args.targets:
        try:
            ip_network = ipaddress.ip_network(target)
            for ip in ip_network:
                targets.append(str(ip))
        except ValueError:
            targets.append(target)
    main(targets)