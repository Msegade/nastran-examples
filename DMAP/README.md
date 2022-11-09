# DMAP

## List subdmaps

- Basic sol1 model, list all sequence| [sol1-list.bdf](sol1-list.bdf)
- Find location of matrices on the sequence | [sol1-findLocation.bdf](sol1-findLocation.bdf)
- Save solution matrices in op4 format | [sol1-matrices.bdf](sol1-matrices.bdf)

## Print KGG and KAA Matrices

Cantilever beam modeled with PBARL, L = 10m, E = 10e6, h = 0.3, b = 0.2

$$ 
\begin{equation}
\frac{EA}{L} = 60 000 \quad \frac{12EI}{L^3} = 54
\end{equation}
$$

- Print after PHASE1DR subDMAP | [kgg-kaa.bdf](kgg-kaa.bdf)

