## 4. Conclusion

The TEOTIL2 model has been extended to simulate fluxes of eight metals (arsenic, lead, cadmium, copper, chromium, mercury, nickel and zinc) at the scale of Norway's "regine" catchment network. The spatial distribution of "diffuse source" metal concentrations in Norwegian surface waters has been [derived from the 2019 "1000 Lakes" dataset](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/dev03_teotil2_metals_1k_lakes_2019.ipynb), while temporal changes at regional scale are [inferred from long-term monitoring](https://nbviewer.jupyter.org/github/NIVANorge/teotil2/blob/main/notebooks/dev04_teotil2_metals_over_time.ipynb) in major rivers collected as part of Elveovervåkingsprogrammet. Direct point discharges (e.g. from industry) are also included based on data extracted from Miljødirektoratet's discharge licensing database.

For most metals and most locations, the model adequately reproduces patterns in observed metal fluxes. Assessment of the model's performance demonstrates it is clearly superior to the current "default" approach of considering only point discharges, as done by e.g. Elveovervåkingsprogrammet. However, for some metals - most notably copper and nickel - the model's performance is consistently poor. There is also evidence that the point discharge dataset used to drive the model may contain significant errors for some locations and years, leading to sudden implausible spikes in the model output. With further refinement of the input datasets, it may be possible to improve these aspects of model performance. 

The TEOTIL2 modelling framework (including TEOTIL2 Metals) is Open Source and available to download [here](https://github.com/NIVANorge/teotil2). The model is both flexible & easily extensible, and provides considerable improvements in performance compared to earlier versions.

\
\
\
<<[Previous](07_1000_lakes.html) --------- [Contents](00_intro_and_toc.html) --------- [Next](09_references.html)>>

        [Home](https://nivanorge.github.io/teotil2/)