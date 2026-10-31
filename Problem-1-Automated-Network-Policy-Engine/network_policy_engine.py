import requests
import time

# Ryu Controller REST API configuration
CONTROLLER = "http://127.0.0.1:8080"
CHECK_INTERVAL = 5

# Traffic threshold in bytes
TRAFFIC_THRESHOLD = 1000

# IP addresses to block ICMP traffic between
SOURCE_IP = "10.0.0.1"
DESTINATION_IP = "10.0.0.2"

session = requests.Session()


def get_switches():
    """Fetch connected switch datapath IDs."""
    url = f"{CONTROLLER}/stats/switches"

    response = session.get(url, timeout=5)
    response.raise_for_status()

    switches = response.json()

    print("\nConnected Switches:", switches)
    return switches


def get_port_statistics(dpid):
    """Fetch and parse port statistics for a switch."""
    url = f"{CONTROLLER}/stats/port/{dpid}"

    response = session.get(url, timeout=5)
    response.raise_for_status()

    data = response.json()
    port_stats = data.get(str(dpid), [])

    total_bytes = 0

    print(f"\nPort Statistics for Switch {dpid}")

    for port in port_stats:
        port_no = port.get("port_no")
        rx_bytes = port.get("rx_bytes", 0)
        tx_bytes = port.get("tx_bytes", 0)

        total_bytes += rx_bytes + tx_bytes

        print(
            f"Port {port_no}: "
            f"RX={rx_bytes} bytes, "
            f"TX={tx_bytes} bytes"
        )

    print("Total Traffic:", total_bytes, "bytes")
    return total_bytes


def block_icmp_traffic(dpid):
    """Install a flow rule to drop ICMP packets."""
    url = f"{CONTROLLER}/stats/flowentry/add"

    payload = {
        "dpid": int(dpid),
        "priority": 200,
        "idle_timeout": 0,
        "hard_timeout": 0,
        "match": {
            "dl_type": 2048,
            "nw_proto": 1,
            "nw_src": SOURCE_IP,
            "nw_dst": DESTINATION_IP
        },
        "actions": []
    }

    response = session.post(url, json=payload, timeout=5)
    response.raise_for_status()

    print(f"\n[POLICY ENFORCED] Switch {dpid}")
    print(f"ICMP traffic blocked: {SOURCE_IP} -> {DESTINATION_IP}")
    print("Flow rule installed successfully!")


def monitor_network():
    """Continuously monitor traffic and enforce network policies."""

    installed_switches = set()

    print("=" * 55)
    print("SDN AUTOMATED NETWORK POLICY ENGINE")
    print("=" * 55)

    while True:
        try:
            switches = get_switches()

            if not switches:
                print("No switches connected to controller.")

            for dpid in switches:
                total_bytes = get_port_statistics(dpid)

                if total_bytes > TRAFFIC_THRESHOLD:
                    print("\nTraffic threshold exceeded!")

                    if dpid not in installed_switches:
                        block_icmp_traffic(dpid)
                        installed_switches.add(dpid)

                else:
                    print("Traffic within configured threshold.")

        except requests.exceptions.RequestException as error:
            print("\nREST API Error:", error)

        except KeyboardInterrupt:
            print("\nNetwork monitoring stopped.")
            break

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_network()
