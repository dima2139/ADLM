import sys
import os
from panoptica import Panoptica_Statistic
from panoptica_statistics import make_curve_over_setups

stat1 = Panoptica_Statistic.from_file("C:/Users\jeanb\PycharmProjects\panoptica\panoptica_out/baseline.tsv")
stat2 = Panoptica_Statistic.from_file("C:/Users\jeanb\PycharmProjects\panoptica\panoptica_out\highres1.tsv")
stat3 = Panoptica_Statistic.from_file("C:/Users\jeanb\PycharmProjects\panoptica\panoptica_out\highres2.tsv")

statistics_dict = {
    "baseline": stat1,
    "highres1": stat2,
    "highres2": stat3
}

#print(stat1.metricnames)
#print(stat1.groupnames)

metric = "sq_dsc"  # or any metric name found in your TSVs
groups = ["kidney", "masses", "tumor"]  # optional: choose groups to compare

fig = make_curve_over_setups(
    statistics_dict=statistics_dict,
    metric=metric,
    groups=groups,
    plot_as_barchart=True,
    plot_std=True,
    figure_title=f"Comparison of {metric} across setups",
    xaxis_title="Model",
    yaxis_title=metric,
    height=600,
    width=800,
)

fig.show()
fig.write_image("C:/Users\jeanb\PycharmProjects\panoptica\panoptica_out\setups.png")