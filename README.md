# Codes_Healthcare_districting_COR
# Two-Level Healthcare Districting — Code and Instances
---

## Description

This repository contains the implementation of exact and heuristic methods for the two-level healthcare districting problem. The goal is to partition a geographic region into *K* balanced and connected districts, simultaneously optimizing the allocation of primary and secondary healthcare resources.

---

## Requirements

- Python 3.8+
- [Gurobi](https://www.gurobi.com/) (license required)
- Python libraries: `numpy`, `pandas`, `networkx`, `matplotlib`, `Pillow`, `pytesseract`

Install dependencies:
```bash
pip install numpy pandas networkx matplotlib Pillow pytesseract
```

---

## Repository Structure

```
├── Read_Instance.py       # Instance reading and parameter definition
├── models.py              # MILP formulations (MTZ, DSF, MCF) and clique models
├── functions.py           # Auxiliary functions: result saving and node reindexing
├── fixing_variables.py    # Variable fixing and spanning tree construction
├── main_heuristic.py      # Spanning-tree-based heuristic
├── main.py                # Main script: Branch-and-Bound resolution
└── instances/             # Random instances used in computational experiments
```

---

## Execution Flow

### 1. Prepare the instance
Instances are read from a `.txt` file in tabular format. Each line contains:

```
num_instance  instance  uni  pob  recurso_h  recurso_c  MA  poblacion  ...  distancia  tam_reg
```

### 2. Run the exact model (`main.py`)

```bash
python main.py <instance_file> <K> <beta> <var> <symmetry> <fixing> <model>
```

| Argument | Description | Values |
|----------|-------------|--------|
| `instance_file` | Path to the instance `.txt` file | — |
| `K` | Number of districts | integer ≥ 2 |
| `beta` | Weight of secondary resource (0 = primary only, 1 = secondary only) | [0, 1] |
| `var` | Variable type | `1` = binary, `0` = continuous (LP relaxation) |
| `symmetry` | Enable symmetry-breaking constraints | `1` = yes, `0` = no |
| `fixing` | Enable variable fixing (district centers) | `1` = yes, `0` = no |
| `model` | Connectivity formulation | `MTZ`, `DSF`, `MCF` |

**Example:**
```bash
python main.py instances/instance_16.txt 4 0.5 1 1 1 DSF
```

### 3. Run the heuristic (`main_heuristic.py`)

```bash
python main_heuristic.py <instance_file> <K> <beta>
```

---

## Module Descriptions

### `Read_Instance.py`
Reads the instance and defines all problem parameters: set of territorial units *V*, arcs *E*, population, primary (`recurso_c`) and secondary (`recurso_h`) resources, distances, and balance parameters (`PP`, `coef`, `Lmax`).

### `models.py`
Contains the MILP formulations:
- **`max_clique()`**: solves the maximum clique problem to identify candidate district centers.
- **`max_weighted_clique()`**: selects the *K* centers with the highest combined weight.
- **`model_a_z()`**: builds the base model with assignment variables (`a`) and spanning tree variables (`z`), balance, compactness, and connectivity constraints.
- **`MTZ()`**, **`DSF()`**, **`MCF()`**: add connectivity constraints according to the chosen formulation.
- **`Symmetry_Breaking()`**: adds symmetry-breaking constraints.

### `functions.py`
- **`archivos()`**: saves the solution and computational performance to `.txt` files.
- **`reorder_nodes_after_clique()`**: reindexes graph nodes placing selected centers in the first positions.
- **`reindex_nodes()`**: builds the reindexing mapping.

### `fixing_variables.py`
- **`nodos_posibles()`**: determines which territorial units can belong to each district given the fixed center, respecting distance and population constraints.
- **`DFS()`**: builds a spanning tree via DFS for each district, used as the initial solution in the heuristic.

### `main.py`
Main script. Executes in order:
1. Maximum clique and maximum weighted clique resolution to select district centers.
2. Graph reindexing.
3. Construction and resolution of the MILP model with Gurobi (Branch-and-Bound).
4. Result saving.

---

## Outputs

The program generates two files per run:

- `Solution_<model>_<suffix>.txt`: assignment of territorial units to districts, population and resources per district.
- `Performance_<model>_<suffix>.txt`: objective value, bounds, optimality gap, computation time, and nodes explored.

Suffixes: `_S` (symmetry), `_F` (fixing), `_S_F` (both).

---

## Instances

This repository includes randomly generated instances of varying sizes (number of territorial units and number of districts *K*), used to evaluate the computational performance of the proposed methods.

```
