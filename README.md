# Artificial Intelligence (AI) - EL2 - 09

## 1. Introduction

This repository contains an Artificial Intelligence (AI) assignment consisting of three implementations: Expert System, Search Algorithm, and Multi-Agent System.

The purpose of this project is to understand and demonstrate fundamental AI concepts through Python programming.

### Project Topics

**A. Expert System: Laptop Damage Diagnosis**

An expert system that identifies potential laptop problems based on user-reported symptoms. It uses Forward Chaining and Certainty Factor (CF) to determine possible diagnoses and their confidence levels.

**B. Search Algorithm: Maze Pathfinding**

A program that compares five search algorithms for finding a path from a start point to a goal in a grid maze:
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Uniform Cost Search (UCS)
- Greedy Best-First Search
- A* Search using the Manhattan distance heuristic

The program compares path length, total path cost, expanded nodes, and execution time.

**C. Multi-Agent System: Collaborative Cleaning Robots**

A simulation of three autonomous robots cleaning dirt in a grid environment. It compares two operating modes:
- Independent mode, in which each robot selects its nearest dirt location.
- Coordinated mode, which uses the Contract Net Protocol to assign tasks based on the lowest distance bid.

The simulation compares completion time, total movement steps, wasted steps, and the number of dirt locations cleaned by each agent.

## 2. Requirement

The requirements for running these programs are:

- Python 3.x
- Visual Studio Code (VS Code) or another Python-compatible editor
- A terminal or command prompt

Python modules used:
- `heapq` for priority queues in search algorithms.
- `time` for measuring execution time.
- `collections.deque` for BFS.
- `random` for generating dirt locations in the multi-agent simulation.

All modules used in these programs are included in Python's standard library. No additional third-party libraries are required.

## 3. How to Use

### Step 1: Download the Repository

Clone the repository using:

```bash
git clone <repository-url>
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

### Step 2: Open
