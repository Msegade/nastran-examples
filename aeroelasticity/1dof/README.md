# 1 DOF Airfoil

Dimitriadis p. 22

Airfoil properties:

- Half Chord: $b=6\text{ft}$
- Elastic axis position 50% chord: $a=1.00$
- Leading edge position: $X_{LE} = -3.0$
- Trailing edge position: $X_{TE} = 3.0$
- Torsional stiffness: $K_{\theta}=50.0\text{ft-lb/rad}$

The aerodynamics considered are thin airfoil theory

$$
C_m = 2 \pi \alpha
$$

## Files 

- Python script to calculate with the formula  | [main.py](main.py)
- 1Dof using nastran strip theory  | [diverg.bdf](diverg.bdf)

In nastran theodorsen function is used for unsteady aerodynamics, in this example 
the parameters are irrelevant for static aeroelasticity



