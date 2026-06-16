# AWS VPC Peering Troubleshooting Guide

## 1. Symptoms of Peering Failure
- Timeout when trying to reach an IP in the peered VPC.
- "Destination Unreachable" errors.
- Successful DNS resolution but failed TCP connection.

## 2. Check Routing Tables
Ensure both VPCs have route table entries pointing the destination CIDR to the VPC Peering Connection (`pcx-xxxx`).
- **Common Error:** Forgetting to update the route table in *both* the Requester and Accepter VPCs.

## 3. Security Groups
Security groups must explicitly allow traffic from the peered VPC's CIDR range or Security Group ID.
- **Note:** Referencing a Security Group ID across peered VPCs only works if the peering is in the *same* region.

## 4. Network ACLs (NACLs)
Check both Inbound and Outbound NACL rules. NACLs are stateless, so you must allow both the request and the return traffic.

## 5. Overlapping CIDRs
VPC Peering will NOT work if the CIDR blocks overlap.
- **Resolution:** Use Private NAT Gateway or Transit Gateway with NAT if IP ranges overlap.
