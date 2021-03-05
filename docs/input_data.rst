Input data
===========

 * The input data is the data that must be provided to Deflex for it to create a scenario. This data con be provided either as csv or as an xlsx format.
 * Since the input data is quite varied, it is divided into 12 different groups, in order to have it more organized and clear. Taking the xlsx format as example, the data is divided into 12 sheets plus a last one where the data sources are indicated.
 * It is not necessary to fill in all the input data to create a scenario. Some data is necessary, others are optional with which more detailed scenarios can be created. An example of this is the heating sector, which expands the scenario covering this sector, but a scenario without it can also be created. In each group of input data it is indicated whether it is mandatory or not.
 * As a brief overview the data is divided into sources (which are subdivided into volatiles and commodities), demands (which are divided into power, heating and mobility), sotrages (electrical), and power lines.
 * The 12 different sheets are described below in the order in which the sheets are in the xlsx document.
 
----------
General
----------
*Not mandatory but highly recomended*. This sheet requires general data about the scenario such as the year of the data, the time step of it, name and the number of regions in which the scenario is divided. There is also the possibility to set a CO2 price. Here must be indicated if the heating sector is considered or not (if so, then the heating data becomes mandatory). The cooperplate mode means that all capacities and efficiencies in the power lines are infinite and 1 respectively (again if this option is dissabled, then capacities and efficiencies must be provided in the transmission lines sheet). Variable costs and downtime factor are with respect to the power plants sheet, and data must be provided in case these are activated.

----------
Commodity sources
----------
*Mandatory*. As the name says, this sheet requires data from all the commodities (i.e. non volatile) the scenario uses. It is important to remark that commodities does not mean fossil fuels, althought all of them are commodities. Commodities mean the fuels with which energy generation can be controlled. For each fuel, its generation cost [€/MWh] and emission level [t/MWh] (emission level for generating the fuel, do not confuse it with the emission level when generating electricity which is covered in the power plant sheet) must be provided.

----------
Demand series
----------
*Mandatory at least the electrical part*. This sheet requires the electrical and heating demand of the scenario. The demand must be provided in a time series form with the time step specified in the general sheet for each region in [MW]. This time series must be provided as a column form, therefore there will be as many columns as there are regions on the scenario. If the heating sector is included, then two colums of data are required for each region, one for electricity and one for heating. (add the DE_demand, lignite, natural gas, oil other)

----------
Mobility
----------
*Not mandatory*

----------
Mobility series
----------
*Not mandatory*

----------
Decentralized heat
----------
*Not mandatory* This sheet requires all the sources with which heat is generated along with their conversion efficiency

----------
Chp - heat plants
----------
*Not mandatory*

---------
Power plants
----------
*Mandatory*

----------
Volatiles plants
----------
*Mandatory*

----------
Volatiles series
----------
*Mandatory*

----------
Storages
----------
*Not mandatory*

----------
Power lines
----------
*Mandatory*

----------
Data sources
----------
*Not mandatory but highly recomended*
