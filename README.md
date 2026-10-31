# Software Defined Networking (SDN) – Scenario Implementations

A collection of four practical Software Defined Networking (SDN) implementations demonstrating network policy automation, broadcast storm prevention, QoS-based network slicing, and intent-based networking.

The scenarios are implemented using **Ryu, Mininet, Open vSwitch (OVS), and ONOS** in an Ubuntu 22.04 environment.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Network automation and controller applications |
| Ryu Controller | SDN control and traffic management |
| Mininet | Network topology emulation |
| Open vSwitch (OVS) | Software-based network switching |
| OpenFlow 1.3 | Controller-switch communication |
| ONOS 2.7.0 | Intent-based network management |
| Docker | ONOS deployment |
| Linux HTB | QoS traffic shaping and queue management |

---

# Implemented Scenarios

## 1. Automated Network Policy Engine

**Objective:** Monitor network traffic statistics and automatically enforce network policies when a configured threshold is exceeded.

**Implementation:**
- Developed a Python-based policy engine using the Ryu REST API.
- Retrieved switch and port statistics.
- Compared cumulative traffic byte counters against a predefined threshold.
- Automatically installed an OpenFlow drop rule when the threshold condition was met.
- Blocked ICMP traffic from a specified source host to a destination host.

**Expected/Verified Outcome:**
- Successful retrieval of network statistics.
- Automatic policy enforcement.
- Installation and verification of the ICMP drop flow rule.

**Technologies:** Python, Ryu, Mininet, Open vSwitch, OpenFlow 1.3.

## 2. Broadcast Storm Prevention

**Objective:** Detect excessive broadcast traffic and prevent broadcast storms by dynamically installing flow rules.

**Implementation:**
- Created a multi-host network topology using Mininet.
- Used Ryu PacketIn events to monitor broadcast frames.
- Implemented threshold-based broadcast detection.
- Detected excessive broadcast traffic originating from a host.
- Installed a high-priority OpenFlow drop rule for broadcast frames from the detected source MAC address.

**Expected/Verified Outcome:**
- Detection of excessive broadcast traffic.
- Controller notification when the configured threshold is exceeded.
- Successful installation and verification of the broadcast drop rule.

**Technologies:** Python, Ryu, Mininet, Open vSwitch, OpenFlow 1.3.

## 3. 5G Network Slicing Using QoS

**Objective:** Demonstrate traffic classification and Quality of Service (QoS) using separate queues for different traffic categories.

**Implementation:**
- Configured Open vSwitch QoS using Linux Hierarchical Token Bucket (HTB).
- Created two traffic classes:
  - **Streaming Traffic:** DSCP 46, Queue 1.
  - **Control Traffic:** DSCP 10, Queue 2.
- Configured queue bandwidth parameters and maximum transmission rates.
- Installed OpenFlow rules to classify packets based on DSCP values.
- Directed classified packets to their corresponding QoS queues.

**Queue Configuration:**

| Parameter | Streaming Queue | Control Queue |
|---|---:|---:|
| Queue ID | 1 | 2 |
| DSCP Value | 46 | 10 |
| Minimum Rate | 20 Mbps | 5 Mbps |
| Maximum Rate | 50 Mbps | 10 Mbps |

The parent QoS rate was configured to 60 Mbps.

**Expected/Verified Outcome:**
- Successful QoS and queue configuration.
- Installation of DSCP-based OpenFlow rules.
- Successful testing of both traffic classes using DSCP-marked ICMP packets.
- Both connectivity tests completed with 0% packet loss.

**Technologies:** Ryu, Mininet, Open vSwitch, OpenFlow 1.3, Linux HTB.

## 4. Intent-Based Networking Using ONOS

**Objective:** Implement intent-based networking using the ONOS controller to establish communication between network endpoints.

**Implementation:**
- Deployed ONOS 2.7.0 using Docker.
- Connected a Mininet OpenFlow 1.3 switch to the ONOS controller.
- Activated the OpenFlow and forwarding applications.
- Discovered network devices and hosts through ONOS.
- Created a PointToPointIntent using the ONOS REST API.
- Configured the intent between switch port 1 and switch port 2.

**Verified Outcome:**
- ONOS successfully discovered 1 switch and 2 hosts.
- Successfully created a PointToPointIntent.
- Intent installation state verified as `INSTALLED`.
- Connectivity between h1 and h2 verified using ICMP ping.
- Achieved 0% packet loss during the five-packet connectivity test.

**Technologies:** ONOS 2.7.0, Docker, Mininet, Open vSwitch, OpenFlow 1.3.

---

# Project Verification Summary

| Scenario | Verification |
|---|---|
| Automated Network Policy Engine | Traffic statistics retrieved and ICMP drop rule installed |
| Broadcast Storm Prevention | Broadcast storm detected and drop rule installed |
| 5G Network Slicing | DSCP classification and QoS queue selection verified |
| ONOS Intent-Based Networking | Point-to-point intent installed and host connectivity verified |

---

# Project Structure

```text
SDN-Scenario-Implementations/
│
├── README.md
│
├── Problem-1-Automated-Network-Policy-Engine/
│   └── network_policy_engine.py
│
├── Problem-2-Broadcast-Storm-Prevention/
│   └── broadcast_prevention.py
│
├── Problem-3-5G-Network-Slicing/
│   └── README.md
│
└── Problem-4-ONOS-Intent-Based-Networking/
    └── README.md
```

Additional implementation files and configuration details are maintained in their respective scenario folders.

---

# Environment and Requirements

- Ubuntu 22.04
- Python 3
- Ryu SDN Controller
- Mininet
- Open vSwitch
- OpenFlow 1.3
- Docker
- ONOS 2.7.0

**Note:** Problems 1–3 use the Ryu controller, while Problem 4 uses ONOS. Both controllers use port 6653 in this setup and should be run separately.

---

# Learning Outcomes

- Understanding Software Defined Networking architecture.
- Implementing centralized network control using SDN controllers.
- Automating network monitoring and policy enforcement.
- Detecting and mitigating excessive broadcast traffic.
- Configuring QoS and traffic classification using DSCP.
- Understanding intent-based networking and Point-to-Point Intents.
- Building and testing virtual network topologies using Mininet and Open vSwitch.

---

## Author

**Divyansh Kumar Singh**  
B.Tech – Computer Science and Engineering  
SRM Institute of Science and Technology

---

*Academic project demonstrating practical implementation of Software Defined Networking concepts.*
