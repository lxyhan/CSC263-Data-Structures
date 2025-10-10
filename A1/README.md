# CSC263 Assignment 1: Network Discovery and Pathfinding

## Overview
Implementation of graph algorithms for network device discovery and cheapest path finding.

## Files
- `a1_submission.py` - Main implementation with Vertex, Graph, and Device classes

## Algorithms Implemented
- **Network Discovery**: Breadth-First Search (BFS)
- **Pathfinding**: Cheapest-First Search (CFS) / Dijkstra's Algorithm

## Features
- ✅ Graph data structure with vertices and edges
- ✅ BFS-based network discovery
- ✅ CFS algorithm for finding cheapest paths
- ✅ Handles cycles, disconnected components, and edge cases
- ✅ All 65 tests passing

## Usage
```python
from a1_submission import Device

# Create a device and discover its network
device = Device("router-1")
device.discover_network(find_devices_fn)

# Find cheapest path to another device
path = device.find_path("target-device")
```
