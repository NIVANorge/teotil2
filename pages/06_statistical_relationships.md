## 3.3. Statistical relationships

TEOTIL Metals is underpinned by the idea that significant relationships exist between key sources/drivers of metal inputs (geology, atmospheric deposition, hydrology and point discharges) and the fluxes observed in surface waters. To test this, statistical models were developed linking the 2019 national water chemistry dataset to a range of possible explanatory variables (full details and code are [here](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/dev02_teotil2_metals_interp_and_regress.ipynb)). The analysis considered only the metals As, Cr, Cu, Ni, Pb and Zn; Cd and Hg were not considered, as they are missing from one or more of the required input datasets. The following variables were incorporated:

 * **Water chemistry**. Concentrations of metals [μg/l], plus TOC [mgC/l] and pH [-] were extracted from the database for the 2019 lake survey. Catchment boundaries representing the area upstream of each sampling location were also obtained

 * **Geology**. The mean metal concentration [mg/kg] measured in river sediments was calculated for each catchment by averaging IDW interpolated values within each catchment boundary (*[Fig. 2b](https://nivanorge.github.io/teotil2/pages/04_local_inputs.html)*)

 * **Atmospheric deposition**. The IDW interpolated moss dataset from 2005 (*[Fig. 3b](https://nivanorge.github.io/teotil2/pages/04_local_inputs.html)*) was averaged over each catchment to obtain values proportional to deposition inputs [mg/kg]. 2005 was chosen because later moss survey datasets contain fewer sampling points (see [Section 3.1.2](04_local_inputs.html))

### 3.3.1. Exploratory data analysis

Scatter plots with lowess smoothing were used to summarise relationships between variables and to highlight general trends (see [here](https://nbviewer.jupyter.org/github/JamesSample/rid/blob/master/notebooks/nope_metals_3.ipynb#8.1.-Data-exploration) and [here](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/dev02_teotil2_metals_interp_and_regress.ipynb#7.-Regression) for details). Although there is a lot of noise, the smoothing picks out plausible relationships: most metal concentrations are higher under organic carbon-rich or acidic conditions, and there are clear positive relationships with deposition (mosses) and geology (river sediments). Furthermore, in some cases the relationship with pH approximates exponential decay, which can be linearised by converting from pH units to the concentration of $$H^+$$ ions

$$
[H^+] = 10^{-pH} \quad \quad \quad (10)
$$

When this is done, the relationships on the scatter plots are all approximately linear, suggesting multiple linear regression as an appropriate tool for further analysis.

### 3.3.2. Multiple linear regression

Multiple linear regression models of the following form were fitted for each metal, $$X$$

$$
C_i^X= \beta_0^X + \beta_1^X M_i^X + \beta_2^X G_i^X + \beta_3^X C_i^{TOC} + \beta_4^X C_i^{H^+} \quad \quad \quad (11)
$$

Where $$C_i^X$$ is the concentration of metal $$X$$ in lake $$i$$; $$M_i^X$$ is the average concentration of $$X$$ in mosses in catchment $$i$$; $$G_i^X$$ is the average concentration of $$X$$ in river sediments in catchment $$i$$; $$C_i^{TOC}$$ is the concentration of TOC in lake $$i$$; $$C_i^{H^+}$$ is the concentration of $$H^+$$ ions in lake $$i$$ (estimated using equation [10]) and the $$\beta_j^X$$ are the regression parameters for each metal.

All variables were standardised prior to regression and a "best subsets" approach applied to find the model with the lowest AIC from all possible combinations of the five explanatory variables. Note that, in general, best subsets is prone to overfitting the data (regularised techniques such as lasso or ridge regression are usually preferable), but it does provide a useful comparison to the "full" model, which is of interest here.

Fig. 5a shows the fitted versus observed values for Pb for the “best” model identified. This model explains roughly 59% of the data variance (R^2=0.59) and the residuals (Fig. 5b) are approximately normally distributed. The fitted equation (using standardised values) is

C_i^Pb=0.20C_i^TOC+0.47C_i^(H^+ )+〖0.23M〗_i^Pb+0.17G_i^Pb+ε                                        (12)

and all variables are highly significant (p≪0.05). The model coefficients are plausible and indicate that Pb has positive relationships with both geological and atmospheric inputs, as well as with concentrations of organic matter and H+. Looking at the standardised coefficients, it appears that the concentration of H+ has the biggest effect size, followed by mosses (i.e. deposition), concentration of TOC, and geochemistry. These results are consistent with the literature survey in Section 1, which states that lead concentrations in Norway are dominated by LRTAP, but strongly modified by pH and complexation with organic matter (Table 1)


The relationships identified above are much more robust than those obtained using the 1995 1000 Lakes dataset: all relationships are highly statistically significant and most are physically plausible. However, the explanatory power for several of the metals is poor (i.e. the effect size is small/negligible). Furthermore, in most cases the effects of other water chemistry parameters (especially TOC concentration) are more important than either the moss or geochemistry variables. This is problematic, because TEOTIL enforces a simple conceptual framework that is incapable of representing such "process-based" or "mechanistic" effects.

Note: Similar problems have been documented previously for the original TEOTIL model when simulating phosphorus: because a significant fraction of the P-load is typically bound to particulates, the model performs poorly compared to nitrogen (where most of the flux is dissolved).

This notebook highlights the following problems/challenges with developing TEOTIL2 Metals:

The geochemistry dataset only includes values for six out of eight metals of interest

Although the moss suveys take place every five years, the number of data points has reduced substantially since 2005. Data for Hg are missing from the 1990 survey and, furthermore, in surveys prior to 2005 detection limits were substantially higher (similar to the 1995 1000 Lakes survey)

The statistical analysis required to identify export coefficients for the model identifies significant but weak relationships, where the best predictors are usually other water chemistry variables (pH and TOC) and not the moss or geochemistry datasets. Since we do not have national scale datasets of pH and TOC through time (the "1000 Lakes" are 20 years apart), it is not possible to use these relationships effectively. Furthermore, relationships restricted to using only the moss and geochemistry datasets are very poor

With these points in mind, I do not think it is sensible to continue development of TEOTIL2 Metals in this direction, at least for the moment. Instead, I will explore an alternative solution that makes better use of the 2019 1000 Lakes dataset.



\
\
\
<<[Previous](05_retention.html) --------- [Contents](00_intro_and_toc.html) --------- [Next]()>>

{% include lib/mathjax.html %}