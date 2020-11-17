## 3.2. Estimating retention

### 3.2.1. Theory

The theoretical principles for estimating retention in lakes are described by [Vollenweider (1975)](https://link.springer.com/article/10.1007/BF02505178). The mass balance for a non-volatile substance in a lake or reservoir is given by

$$
\frac{dM}{dt} = m_i - m_o - S \quad \quad \quad (3)
$$

where $$M$$ is the mass of substance in the lake; $$m_i$$ is the sum of all inflow fluxes; $$m_o$$ is the flux from the lake outflow; and $$S$$ represents all internal processes that remove the substance from the lake. $$S$$ is assumed to be proportional to $$M$$, such that the greater the amount of substance in the lake, the faster it is removed by internal processing

$$
S = \sigma M \quad \quad \quad (4)
$$

Rewriting the input and output fluxes as the product of discharge and concentration, and combining equations [3] and [4] gives

$$
\frac{dM}{dt} = q_i [m_i] - q_o [m_o] - \sigma M \quad \quad \quad (5)
$$

where $$q_i$$ and $$q_o$$ are the inflow and outflow discharges, respectively, and $$[m_i]$$ and $$[m_o ]$$ are the inflow and outflow concentrations. For a perfectly mixed lake, $$[m_o] = M/V$$, where $$V$$ is the lake volume. Assuming steady state, $$dM/dt = 0$$ and $$V$$ is constant, which implies $$q_i = q_o = q$$

$$
q[m_i] - q[m_o] - \sigma V [m_o] = 0 \quad \quad \quad (6)
$$

Defining the water renewal rate as $$\rho = q/V$$ (i.e. the reciprocal of the residence time) and rearranging gives

$$
\frac{[m_o]}{[m_i]} = \frac{\rho}{\sigma + \rho} \quad \quad \quad (7)
$$

Because $$q$$ is constant, the ratio of concentrations, $$[m_o] / [m_i]$$, is also the ratio of fluxes, $$m_o / m_i$$. The retention factor, $$R$$, is defined as

$$
R = 1 - \frac{m_o}{m_i} = 1 - \frac{\rho}{\sigma + \rho} = \frac{\sigma}{\sigma + \rho} \quad \quad \quad (8)
$$

In this formulation, the water renewal rate, $$\rho$$, is hydrologically determined, and $$\sigma$$ is a parameter-specific constant representing the rate of internal cycling and removal. Although equation [8] has a sound scientific basis, several authors (e.g. [Larsen and Mercier, 1976](https://cdnsciencepub.com/doi/10.1139/f76-221); [Vink and Peters, 2003](https://onlinelibrary.wiley.com/doi/abs/10.1002/hyp.1286)) have found empirically that a modified equation of the form

$$
R = \frac{\sigma}{\sigma + \rho^n} \quad \quad \quad (9)
$$

provides a better fit to observations. Note, however, that there is no mechanistic theory behind equation [9]; unless $$n = 1$$, the units in the denominator are not physically compatible.

### 3.2.2. Datasets

For some metals, the literature provides suggested values for the parameters $$\sigma$$ and $$n$$ in equation [9] (e.g. [Vink and Peters, 2003](https://onlinelibrary.wiley.com/doi/abs/10.1002/hyp.1286)). However, these values depend on catchment characteristics and are therefore specific to the hydrological, geochemical and climatic conditions under which they were derived. Studies focusing on the Norwegian context are rare, so for TEOTIL Metals it will likely be necessary to estimate relationships directly from Norwegian data.

An alternative is to use existing water chemistry data and/or statistical relationships to estimate surface water metal concentrations directly for each regine catchment. This approach *implicitly* accounts for retention by estimating $$[m_o]$$ directly, instead of starting with an estimate for $$m_i$$ and assuming steady state. In this case, retention for all catchments in the model can be assumed to be zero, and fluxes for each substance calculated simply as the product of outflow discharge and concentration, $$q_o [m_o]$$.

\
\
\
<<[Previous](04_local_inputs.html) --------- [Contents](00_intro_and_toc.html) --------- [Next](06_statistical_relationships.html)>>

        [Home](https://nivanorge.github.io/teotil2/)

{% include lib/mathjax.html %}