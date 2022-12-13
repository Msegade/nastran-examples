# 2 DOF Airfoil

Roden p. 265

Airfoil properties:

- Half Chord: $b=6\text{ft}$
- Elastic axis position 40% chord: $a=-0.20$
- Leading edge position: $X_{LE} = -2.4$
- Trailing edge position: $X_{TE} = 3.6$
- Center of gravity position 45% chord:  $x_{\theta}=0.10$
- Airfoil mass: $m=1.3447\text{slugs}$
- Static unbalance about elastic axis: $s_{\theta}=-0.40342\text{slug-ft}$
- Radius of gyration about elastic axis: $r_{\theta}=0.5$
- Moment of inertia  about elastic axis: $i_{\theta}=3.0256\text{slug-ft}^2$
- Bending stiffness: $K_{h}=134.47\text{lb/ft}$
- Torsional stiffness: $K_{\theta}=1891.0\text{ft-lb/rad}$

## Files 

- Based on this nastran example  | [ha145a.bdf](ha145a.bdf)
- 2Dof using CONM1  | [2dof-massMatrix.bdf](2dof-massMatrix.bdf)
- 2Dof using CONM2 and rbar  | [2dof-rbar.bdf](2dof-rbar.bdf)

For this model, the center of mass has to be modeled with another grid point and 
joined to the elastic axis using a RBAR element. A CONM2 is located a the center of mass, and the 
moment of inertia is calculated through:

$$
i_{c.g} = i_{\theta} - m(b x_{\theta})^2 = 2.9046 \text{slug-ft}^2
$$


