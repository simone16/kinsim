# Kinsim.py

Simulates chemical reaction kinetics based on a given mechanism.

## Requirements

Kinsim is a python script, so you need a [python](https://www.python.org/) interpreter to run it.
The program also uses [matplotlib](http://matplotlib.org/index.html) to display results,
you can find info on how to install the library on their website.

## Usage

Run kinsim from the command line:
```
cd whathever/kinetics\ simulation
python kinsim.py input-file-path
```
To get a list of the available options run:
```
python kinsim.py --help
```

## Input file syntax

The input file contains info on the mechanism and initial conditions of the reaction.
Each elementary step is written on a line in the form:
`aA + bB + ... -> cC + dD + ... const=value`
or
`aA + bB + ... <=> cC + dD + ... k1=value k-1=value`
While initial concentrations are set as (if not set default to zero):
`[A]=value`

You can also check the example.input files provided.
The symbols used can be modified by changing the first part of the script (kinsim.py file).

## Kinetic laws

The steps given are assumed to be elementary, so a step with N reagents is assumed
to follow a rate law of order N, eg: `A + B -> C` is described by `dx/dt = k[A][B]` 
where `dx = d[C]`.

Note: when counting reagents, the coefficients are ignored. This means that:
`A + A -> B` will have order 2 `dx/dt = k[A][A]`
while
`2A -> B` has order 1 `dx/dt = k[A]`
This allows for use of non-integer coefficients.

