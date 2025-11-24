# TSPLIB95 File Format for CVRP
This document provides a brief overview of the TSPLIB95 format.  
The goal is to explain how the program uses data in TSPLIB95 format.

### Common Sections in a `.vrp` file:

**NAME : \<string\>**
- A unique name for the problem instance.  
  
**COMMENT : \<string\>**
- Informational comments about the instance.

**TYPE : \<string\>**
- Specifies the problem type. For this project `CVRP` (Capacitated Vehicle Routing Problem) 

**DIMENSION : \<integer\>**
- the total number of nodes and depots

**EDGE_WEIGHT_TYPE : \<string\>**
- Defines how edge weights are calculated. `EUC_2D` means Euclidean distances in 2D.

**euclidean distance calculation**  
xd = x[i] - x[j];  
yd = y[i] - y[j];  
dij = nint( sqrt( xd * xd + yd * yd) );

**CAPACITY : \<integer\>**
- The maximum capacity of each vehicle. All vehicles are assumed to have the same capacity.

**NODE_COORD_SECTION**
- This section lists the coordinates of each node.
- The first node is usually the depot
- Format: `<integer> <real> <real>`

```
Example:
1 145 215
2 151 264
3 159 261
4 130 254
...
```

**DEMAND_SECTION**
- This section lists the amount to be delivered for each node.
- Format: `<integer> <integer>`
- The depot node typically has a demand of 0.

```
Example:
1 0
2 1100
3 700
4 800
...
```

**DEPOT_SECTION**
- Specifies the ID(s) of the depot nodes.
- For standard CVRP, there is usually only one.
- The list is terminated with -1.
- Format: `DEPOT_ID`

```
Example:
1
-1
```

**EOF**
- End of file marker.
