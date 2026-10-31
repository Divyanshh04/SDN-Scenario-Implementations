# Problem 4: Intent-Based Networking Using ONOS

## 1. Aim

To implement intent-based networking using the ONOS SDN controller by creating and verifying a Point-to-Point Intent between two hosts in a Mininet topology.

## 2. Technologies Used

- ONOS 2.7.0
- Docker
- Mininet
- Open vSwitch
- OpenFlow 1.3
- REST API

## 3. Start ONOS Using Docker

Download and run the ONOS 2.7.0 container:

```bash
sudo docker run -d --name onos \
  --restart unless-stopped \
  -p 8181:8181 \
  -p 8101:8101 \
  -p 6653:6653 \
  -p 6640:6640 \
  onosproject/onos:2.7.0
```

Access the ONOS web interface:

```text
http://localhost:8181/onos/ui/#/topo2
```

Default lab credentials:

- Username: `onos`
- Password: `rocks`

## 4. Activate Required Applications

Activate the OpenFlow and forwarding applications:

```bash
curl -u onos:rocks -X POST http://localhost:8181/onos/v1/applications/org.onosproject.openflow/active

curl -u onos:rocks -X POST http://localhost:8181/onos/v1/applications/org.onosproject.fwd/active
```

## 5. Create the Mininet Topology

Start a two-host topology connected through one Open vSwitch:

```bash
sudo mn --topo single,2 --mac --switch ovs,protocols=OpenFlow13 --controller remote,ip=127.0.0.1,port=6653
```

The topology consists of:

- h1: 10.0.0.1
- h2: 10.0.0.2
- Switch: s1

The switch connects to the ONOS controller through OpenFlow port 6653.

## 6. Discover Network Devices and Hosts

After starting Mininet, ONOS discovers the connected switch and hosts.

Observed topology:

| Component | Discovered Information |
|---|---|
| Device | `of:0000000000000001` |
| Host 1 | `10.0.0.1` |
| Host 2 | `10.0.0.2` |
| Switch port for h1 | 1 |
| Switch port for h2 | 2 |

## 7. Create a Point-to-Point Intent

An intent describes the desired connectivity between network endpoints. ONOS determines and installs the required forwarding behavior.

The following REST API request creates a Point-to-Point Intent from switch port 1 to switch port 2:

```bash
curl -u onos:rocks -X POST \
-H "Content-Type: application/json" \
http://localhost:8181/onos/v1/intents \
-d '{
  "type": "PointToPointIntent",
  "appId": "org.onosproject.cli",
  "priority": 100,
  "ingressPoint": {
    "device": "of:0000000000000001",
    "port": "1"
  },
  "egressPoint": {
    "device": "of:0000000000000001",
    "port": "2"
  },
  "selector": {
    "criteria": [
      {
        "type": "ETH_TYPE",
        "ethType": "0x800"
      }
    ]
  },
  "treatment": {
    "instructions": [
      {
        "type": "NOACTION"
      }
    ]
  }
}'
```

## 8. Verify the Intent

Retrieve the installed intents using the ONOS REST API:

```bash
curl -s -u onos:rocks http://localhost:8181/onos/v1/intents | python3 -m json.tool
```

The created intent was verified with:

- Intent type: `PointToPointIntent`
- Intent ID: `0x0`
- Application ID: `org.onosproject.cli`
- State: `INSTALLED`

## 9. Connectivity Testing

From the Mininet CLI, execute:

```bash
h1 ping -c 5 h2
```

**Observed result:**

- Packets transmitted: 5
- Packets received: 5
- Packet loss: 0%
- Average RTT: 1.010 ms

The ONOS dashboard also displayed:

- 1 connected device
- 2 discovered hosts
- 1 intent
- 5 flows

## 10. Result

Intent-based networking was implemented successfully using the ONOS controller. A Point-to-Point Intent was created through the REST API and its state was verified as `INSTALLED`.

The Mininet connectivity test confirmed successful communication between the two hosts with 0% packet loss.

*Note: The configured intent specifies traffic from switch port 1 to port 2. The successful ping test was observed in the running ONOS environment, which also had the forwarding application and installed flows.*
