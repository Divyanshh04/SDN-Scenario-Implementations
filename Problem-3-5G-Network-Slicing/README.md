# Problem 3: 5G Network Slicing Using SDN

## 1. Aim

To implement network slicing using Software-Defined Networking (SDN) by configuring multiple QoS queues on an Open vSwitch and classifying traffic using DSCP values.

## 2. Technologies Used

- Ubuntu 22.04
- Mininet
- Open vSwitch (OVS)
- OpenFlow 1.3
- Linux HTB Queueing
- DSCP-based traffic classification

## 3. Network Topology

A simple Mininet topology with two hosts connected through one Open vSwitch:

```text
       h1
        |
        |
       s1
        |
        |
       h2
```

- h1: 10.0.0.1
- h2: 10.0.0.2
- Switch: s1

## 4. Start the Network Topology

Launch Mininet with OpenFlow 1.3:

```bash
sudo mn --topo single,2 --mac --switch ovs,protocols=OpenFlow13 --controller remote,ip=127.0.0.1,port=6653
```

Check connectivity:

```bash
pingall
```

## 5. Configure QoS Queues

QoS was configured using the Linux HTB queueing discipline.

The parent bandwidth was configured to 60 Mbps.

### Queue Configuration

| Queue | Purpose | Minimum Rate | Maximum Rate |
|---|---|---:|---:|
| Queue 1 | High-priority streaming traffic | 20 Mbps | 50 Mbps |
| Queue 2 | Control traffic | 5 Mbps | 10 Mbps |

The queues were configured on the switch interfaces using Open vSwitch QoS settings and Linux HTB.

## 6. DSCP-Based Traffic Classification

Differentiated Services Code Point (DSCP) values were used to classify traffic into different queues.

| Traffic Type | DSCP Value | Queue |
|---|---:|---:|
| Streaming traffic | 46 | Queue 1 |
| Control traffic | 10 | Queue 2 |

### OpenFlow Rules

The following rules classify traffic and assign it to the appropriate queues.

**Streaming traffic (DSCP 46):**

```text
priority=200,in_port=1,ip,ip_dscp=46,actions=set_queue:1,output:2
priority=200,in_port=2,ip,ip_dscp=46,actions=set_queue:1,output:1
```

**Control traffic (DSCP 10):**

```text
priority=200,in_port=1,ip,ip_dscp=10,actions=set_queue:2,output:2
priority=200,in_port=2,ip,ip_dscp=10,actions=set_queue:2,output:1
```

These rules ensure that packets are classified based on their DSCP values and forwarded through the corresponding QoS queue.

## 7. Verification and Testing

The configured OpenFlow rules were verified using:

```bash
sudo ovs-ofctl -O OpenFlow13 dump-flows s1
```

The flow entries showed:
- DSCP 46 traffic matched with `nw_tos=184` and assigned to Queue 1.
- DSCP 10 traffic matched with `nw_tos=40` and assigned to Queue 2.

### Connectivity Tests

**Test 1: Streaming traffic**

```bash
h1 ping -Q 184 -c 5 h2
```

Result: 5 packets transmitted, 5 received, 0% packet loss.

**Test 2: Control traffic**

```bash
h1 ping -Q 40 -c 5 h2
```

Result: 5 packets transmitted, 5 received, 0% packet loss.

## 8. Result

Network slicing was implemented using Open vSwitch QoS queues and DSCP-based traffic classification. Two traffic classes were configured and mapped to separate queues with different bandwidth parameters.

The OpenFlow rules and connectivity tests verified that traffic was classified and forwarded through the intended queues.

*Note: The tests verified DSCP classification and connectivity. They did not independently measure bandwidth guarantees under congestion.*
