# -*- coding: utf-8 -*-

"""Processing a list of power plants in Germany.

SPDX-FileCopyrightText: 2016-2021 Uwe Krien <krien@uni-bremen.de>

SPDX-License-Identifier: MIT
"""


import math
import os

import pandas as pd

from deflex import config as cfg
from deflex import geometries


def get_grid_capacity(grid, plus, minus):
    """Read the grid capacity from a given region pair from the renpass db."""
    tmp_grid = grid.query(
        "plus_region_id == {:0d} & ".format(plus)
        + "minus_region_id == {:1d} & ".format(minus)
        + "scenario_name == 'status_quo_2012_distance'"
    )

    if len(tmp_grid) > 0:
        capacity = tmp_grid.capacity_calc.sum()
        distance = tmp_grid.distance.iloc[0]
    else:
        capacity = 0
        distance = 0
    return capacity, distance


def add_reverse_direction(df):
    """
    Duplicate all entries of a DataFrame with a reverse index. The index must
    contain a dash between two sub-strings.
    """
    values = df.copy()

    def id_inverter(name):
        """Swap the sub-parts of a string left and right of a dash."""
        return "-".join([name.split("-")[1], name.split("-")[0]])

    df.index = df.index.map(id_inverter)

    return pd.DataFrame(pd.concat([values, df]))


def get_electrical_transmission_default(power_lines, both_directions=False):
    """
    Creates a default set of transmission capacities, distance and efficiency.
    The map of the lines must exist in the geometries directory. The default
    values are infinity for the capacity, nan for the distance and 1 for the
    efficiency.

    Parameters
    ----------
    power_lines : iterable[str]
        A list of names of transmission lines. All name must contain a dash
        between the id of the regions (FromRegion-ToRegion).
    both_directions : bool
        If True any line will be replicated in the reverse direction.

    Returns
    -------
    pd.DataFrame
        Transmission capacity, distance and efficiency between regions

    Examples
    --------
    >>> de21 = geometries.deflex_power_lines("de21")
    >>> df=get_electrical_transmission_default(de21.index)
    >>> df.loc['DE10-DE12', 'capacity']
    inf
    >>> df.loc['DE10-DE12', 'distance']
    nan
    >>> df.loc['DE10-DE12', 'efficiency']
    1.0
    >>> len(df)
    39
    >>> de22 = geometries.deflex_power_lines("de22")
    >>> len(get_electrical_transmission_default(de22.index))
    40
    >>> de17_idx = geometries.deflex_power_lines("de17").index
    >>> len(get_electrical_transmission_default(de17_idx))
    31
    >>> len(get_electrical_transmission_default(
    ...     geometries.deflex_power_lines("de02").index))
    1
    >>> my_lines=['reg1-reg2', 'reg2-reg3']
    >>> df=get_electrical_transmission_default(power_lines=my_lines)
    >>> df.loc['reg1-reg2', 'capacity']
    inf
    >>> df=get_electrical_transmission_default(power_lines=my_lines,
    ...                                          both_directions=True)
    >>> df.loc['reg2-reg1', 'capacity']
    inf

    """
    trans = pd.DataFrame()

    for length in power_lines:
        trans.loc[length, "capacity"] = float("inf")
        trans.loc[length, "distance"] = float("nan")
        trans.loc[length, "efficiency"] = 1

    if both_directions is True:
        trans = add_reverse_direction(trans)
    return trans


def get_electrical_transmission_renpass(both_directions=False):
    """
    Prepare the transmission capacity and distance between de21 regions from
    the renpass database. The original table of the reegis database is
    transferred to a csv file, which is part of the reegis package. As renpass
    is deprecated it will not change in the future. The index uses the format
    'region1-region2'. The distance is taken from centroid to centroid. By
    default every region pair exists only once. It is possible to get an entry
    in both directions if the parameter `both_directions` is set True.

    The capacity calculation is taken from the description of the renpass
    package [1]_. The data is taken from the renpass database [2]_.

    This function is only valid for the original renpass region set.

    Parameters
    ----------
    both_directions : bool
        If True any line will be replicated in the reverse direction.

    Returns
    -------
    pd.DataFrame
        Transmission capacity and distance between regions

    References
    ----------
    .. [1] Wiese, Frauke (2015). „Renewable Energy Pathways Simulation
        System – Open Source as an approach to meet challenges in energy
        modeling“. Diss. University of Flensburg. URL :
        https://www.reiner-lemoine-stiftung.de/pdf/dissertationen/Dissertation_Frauke_Wiese.pdf.
        (page 49)
    .. [2] Wiese, F.: Renpass - Renewable Energy Pathways Simulation System,
        https://github.com/fraukewiese/renpass

    Examples
    --------
    >>> translines=get_electrical_transmission_renpass()
    >>> int(translines.loc['DE11-DE17', 'capacity'])
    2506
    >>> int(translines.loc['DE18-DE17', 'distance'])
    119
    >>> translines.loc['DE08-DE06']
    capacity    7519.040402
    distance     257.000000
    Name: DE08-DE06, dtype: float64
    >>> translines=get_electrical_transmission_renpass(both_directions=True)
    >>> int(translines.loc['DE11-DE17', 'capacity'])
    2506
    >>> int(translines.loc['DE17-DE11', 'capacity'])
    2506
    """
    # from [1] Wiese, Frauke (2015) (s. above)
    security_factor = 0.7
    current_max = 2720

    grid = pd.read_csv(
        os.path.join(
            os.path.dirname(__file__),
            "data",
            "static",
            "renpass_transmission.csv",
        )
    )

    grid["capacity_calc"] = (
        grid.circuits
        * current_max
        * grid.voltage
        * security_factor
        * math.sqrt(3)
        / 1000
    )

    pwr_lines = pd.DataFrame(geometries.deflex_power_lines(rmap="de21"))

    for idx in pwr_lines.index:
        split = idx.split("-")
        a = int("110{0}".format(split[0][2:]))
        b = int("110{0}".format(split[1][2:]))
        # print(a, b)
        cap1, dist1 = get_grid_capacity(grid, a, b)
        cap2, dist2 = get_grid_capacity(grid, b, a)

        if cap1 == 0 and cap2 == 0:
            pwr_lines.loc[idx, "capacity"] = 0
            pwr_lines.loc[idx, "distance"] = 0
        elif cap1 == 0:
            pwr_lines.loc[idx, "capacity"] = cap2
            pwr_lines.loc[idx, "distance"] = dist2
        elif cap2 == 0:
            pwr_lines.loc[idx, "capacity"] = cap1
            pwr_lines.loc[idx, "distance"] = dist1

    # plot_grid(pwr_lines)
    df = pwr_lines[["capacity", "distance"]]

    if both_directions is True:
        df = add_reverse_direction(df)

    return df


def scenario_transmission(regions, name, lines):
    """Get power plants for the scenario year

    Examples
    --------
    >>> my_regions=geometries.deflex_regions(rmap="de21")  # doctest: +SKIP
    >>> pp=scenario_powerplants(dict(), my_regions, 2014, "de21"
    ...     )  # doctest: +SKIP
    >>> lines=scenario_transmission(pp, my_regions, "de21")  # doctest: +SKIP
    >>> int(lines.loc["DE07-DE05", ("electrical", "capacity")]
    ...     )  # doctest: +SKIP
    1978
    >>> int(lines.loc["DE07-DE05", ("electrical", "distance")]
    ...     )  # doctest: +SKIP
    199
    >>> float(lines.loc["DE07-DE05", ("electrical", "efficiency")]
    ...     )  # doctest: +SKIP
    0.9
    >>> cfg.tmp_set("creator", "copperplate", "True")
    >>> lines=scenario_transmission(pp, regions, "de21"
    ...     )  # doctest: +SKIP
    >>> cfg.tmp_set("creator", "copperplate", "False")
    >>> float(lines.loc["DE07-DE05", ("electrical", "capacity")]
    ...     )  # doctest: +SKIP
    inf
    >>> float(lines.loc["DE07-DE05", ("electrical", "distance")]
    ...     )  # doctest: +SKIP
    nan
    >>> float(lines.loc["DE07-DE05", ("electrical", "efficiency")]
    ...     )  # doctest: +SKIP
    1.0
    """

    # This should be done automatic e.g. if representative point outside the
    # landmass polygon.
    offshore_regions = geometries.divide_off_and_onshore(regions).offshore

    if name in ["de21", "de22"] and not cfg.get("creator", "copperplate"):
        elec_trans = get_electrical_transmission_renpass()
        general_efficiency = cfg.get(
            "creator", "default_transmission_efficiency"
        )
        if general_efficiency is not None:
            elec_trans["efficiency"] = general_efficiency
        else:
            msg = (
                "The calculation of the efficiency by distance is not yet "
                "implemented"
            )
            raise NotImplementedError(msg)
    else:
        elec_trans = get_electrical_transmission_default(power_lines=lines)

    # Set transmission capacity of offshore power lines to installed capacity
    # Multiply the installed capacity with 1.1 to get a buffer of 10%.
    for offreg in offshore_regions:
        elec_trans.loc[
            elec_trans.index.str.contains(offreg), "capacity"
        ] = "inf"

    elec_trans = pd.concat(
        [elec_trans], axis=1, keys=["electrical"]
    ).sort_index(1)
    if cfg.get("creator", "map") == "de22" and not cfg.get(
        "creator", "copperplate"
    ):
        elec_trans.loc["DE22-DE01", ("electrical", "efficiency")] = 0.999999
        elec_trans.loc["DE22-DE01", ("electrical", "capacity")] = 9999999
    return elec_trans


if __name__ == "__main__":
    pass
