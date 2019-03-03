# //TODO 1. rename variables to something more meaningful
# //TODO 2. create the package (refactor to methods and classes)

# Variables

# factors affecrting eto are only climatic factors, so it can be calculated based on only weather data
# evaporating power of atmosphere in a specific location and time
ETo = 'reference crop evapotranspiration [mm / day]'

# factor considered:
# disease-free, well-fertilized crops, grown in large fields under optimun water conditions and achive full production under given climatic condiitions
# etc will be aprox. 1-9 mm/day from cool to warn average temparatures
ETc = 'crop evapotranspiration under standard conditions'

# weather
direct_solar_radiation = ''
air_temperature = ''
air_relative_humidity = ''
wind_speed = ''

# crop
crop_transpiration_resistance = ''
crop_roughness = ''
crop_height_ref = ''
crop_reflection = ''
crop_ground_cover = ''
crop_root_characteristics = ''
crop_density = ''

# soil
soil_salinity = ''
soil_fertility = ''
soil_roughness = ''
soil_water_content = ''

# variable buckets
variable_bucket = {
                    'ETo':'reference crop evapotranspiration [mm / day]',
                    'ETc':'crop evapotranspiration under standard conditions',
                    'Rn':'net radiation',
                    'H':'sensible heat',
                    'G':'soil heat flux',
}

# EQUATION FOR AN EVAPORATING SURFACE
	# Rn: net radiation at crop surface [MJ]/ pow(m, 2) * day]
	# H: sensible heat
	# G: soil heat flux [MJ / pow(m, 2) * day]
	# ƛET: latent heat flux
Rn - G - ƛET - H = 0  # EQUATION 1

# PENMAN-MONTEITH EQUATION
	# Rn = net radiation
	# (es - ea) = s the vapour pressure deficit of the air [kPa]
	# ∆ =  the slope of the saturation vapour pressure temperature relationship
	# γ = psychrometric constant
	# rs, ra = (bulk) surface and aerodynamic resistances
	# Pa = the mean air density at constant pressure
	# Cp = the specific heat of the air
ƛET = (∆ * (Rn - G) + Pa * Cp * ((Es - Ea) / ra)) / (∆ + γ * (1 + (rs / ra))) # EQUATION 3

# AREODYNAMIC RESISTANCE (ra)
	# ra = aerodynamic resistances [s pow(m, -1)]
	# Zm = height of wind measurements [m] meters
	# Zh = height of humidity measurements [m] meters
	# d = zero plane displacement height [m] meters
	# Zom = roughness length governing momentum transfer [m] meters
	# Zoh = roughness length governing transfer of heat and vapour [m] meters
	# k = von Karman's constant, 0.41 [None]
	# Uz = wind speed at height z [m / s]
from math import log, pow
ra = (log((Zm - d) / Zom) * log((Zh - d) / Zoh)) / (pow(K, 2) * Uz) # EQUATION 4

# (BULK) SURFACE RESISTANCE (rs)
	# rs = (bulk) surface resistances [s pow(m, -1)]
	# rl = bulk stomatal resistance of the well-illuminated leaf [s pow(m, -1)]
	# LAI_active = active (sunlit) leaf area index [pow(m, 2) (leaf area) pow(m, -2) (soil surface)] meters
		# The LAI values for various crops differ widely but values of 3-5 are common for many mature crops. For a given
		# crop, green LAI changes throughout the season and normally reaches its maximum before or at flowering
		# LAI further depends on the plant density and the crop variety.
		# A general equation for LAIactive is: LAI_active = 0.5 LAI
			# which takes into consideration the fact that generally only the upper half of dense clipped grass is actively
			# contributing to the surface heat and vapour transfer. For clipped grass a general equation for LAI is:
			# LAI = 24 * h
			# where h is the crop height [m] meter
			# The stomatal resistance, rl of a single leaf has a value of about 100 s m-1 under well-watered conditions
LAI = 24 * crop_height_ref
LAI_active = 0.5 * LAI

rs = rl / LAI_active # EQUATION 5

# REFERENCE CROP EVAPOTRANSPIRATION
	# ETo = reference evapotranspiration [mm / day]
	# Rn = net radiation at the crop surface [MJ / (pow(m, 2) * day]
	# G = soil heat flux density [MJ / (pow(m, 2) * day)]
	# T = mean daily air temperature at 2 m height [°C]
	# Uz = wind speed at z or 2 m height [m / s] # calculations should be done at 2 m height
	# es = saturation vapour pressure [kPa]
	# ea = actual vapour pressure [kPa]
	# es - ea = saturation vapour pressure deficit [kPa]
	# ∆ = slope vapour pressure curve [kPa / °C]
	# γ = psychrometric constant [kPa / °C]

Eto = (0.408 * ∆ * (Rn - G) + γ * (900 / (T + 273)) * Uz * (es - ea)) / (∆ + γ * (1 + 0.34 * Uz)) # EQUATION 6

# ATMOSPHERIC PRESSURE [kPa]
	# z = elevation above sea level [m] meters
from math import pow
atmospheric_pressure = 101.3 * pow(((293 - 0.0065 * z) / 293), 5.26) # EQUATION 7

# PSYCHROMETRICS CONSTANT
	# γ = psychrometric constant [kPa / °C]
	 # λ = latent heat of vaporization, 2.45 [MJ / kg]
	 # Cp = specific heat at constant pressure, 1.013 10-3 [MJ / kg * °C]
	 # ε = ratio molecular weight of water vapour/dry air = 0.622
γ = (Cp * atmospheric_pressure) / (ε * λ)  # EQUATION 8
γ = 0.665e-3 * atmospheric_pressure # EQUATION 8

# AIR TEMPERATURE
	# temperature in KELVIN
kelvin = centigrades + 273.16
T_mean = (T_max - T_min) / 2 # EQUATION 9

# RELATIVE HUMIDITY
	# The relative humidity (RH) expresses the degree of saturation of the air as a ratio of the actual (ea) to the
	# saturation (eo(T)) vapour pressure at the same temperature (T):
RH = 100 * (ea / eo) # EQUATION 10

# MEAN SATURATION VAPOUR PRESSURE (es)
	# As saturation vapour pressure is related to air temperature, it can be calculated from the air temperature. The relationship is expressed by
	# eo(T) saturation vapour pressure at the air temperature T [kPa]
	# air_temp = air temperature [°C]
	# exp[..] 2.7183 (base of natural logarithm) raised to the power [..].
# //TODO check if eo formula is the right way to calculate this formula
from math import expm1, exp
eo = pow(0.6108, ((17.27 * air_temp) / (air_temp + 237.3)) # EQUATION 11 # function based on temperature
es = (eo_T_max + eo_T_min)) / 2 # EQUATION 12

# ACTUAL VAPOUR PRESSURE (ea) DERIVED FROM DEWPOINT TEMPERATURE
    # T_dew = dewpoint temperature [°C]
ea = eo * pow(0.6108, ((17.27 * T_dew) / (T_dew + 237.3))  # EQUATION 14 # function based on temperature

# ACTUAL VAPOUR PRESSURE (ea) DERIVED FROM PSYCHROMETRIC DATA
    # ea = actual vapour pressure [kPa]
    # eo(T_wet) = saturation vapour pressure at wet bulb temperature [kPa]
    # γ_psy = psychrometric constant of the instrument [kPa / °C]
    # T_dry - T_wet = wet bulb depression, with T_dry the dry bulb and T_wet the wet bulb temperature [°C]
    # for γ_psy
        # 0.000662 for ventilated (Asmann type) psychrometers, with an air movement of some 5 m/s,
        # 0.000800 for natural ventilated psychrometers (about 1 m/s),
        # 0.001200 for non-ventilated psychrometers installed indoors.
ea = eo * T_wet - γ_psy * (T_dry - T_wet) # EQUATION 15

# ACTUAL VAPOUR PRESSURE (ea) DERIVED FROM RELATIVE HUMIDITY DATA
    # ea = actual vapour pressure [kPa]
    # eo_T_min = saturation vapour pressure at daily minimum temperature [kPa]
    # eo_T_max = saturation vapour pressure at daily maximum temperature [kPa]
    # RH_max = maximum relative humidity [%]
    # RH_min = minimum relative humidity [%]

# --for RH_max and RH_min
ea = (eo_T_min * (RH_max / 100) + eo_T_max * (RH_min / 100)) / 2 # EQUATION 17

# --for RH_max -- When using equipment where errors in estimating RH min can be large, or when RH data integrity are in doubt, then one should use only RH max
ea = eo_T_min * (RH_max / 100) # EQUATION 18

# --for RH_mean -- In the absence of RH max and RH min , another equation can be used to estimate e a
    # RH_mean = the mean relative humidity, defined as the average between RH max and RH min .
ea = (RH_mean / 100) * ((eo_T_max + eo_T_min) / 2) # EQUATION 19

# VAPOUR PRESSURE DEFICIT (es - ea)
    # The vapour pressure deficit is the difference between the saturation (es) and actual vapour pressure (ea) for a
    # given time period. For time periods such as a week, ten days or a month e s is computed from Equation 12 using
    # the T max and T min averaged over the time period and similarly the e a is computed with one of the equations 4 to
    # 19, using average measurements over the period.
result = es - ea

# SLOPE OF SATURATION VAPOUR PRESSURE CURVE (∆)
    # For the calculation of evapotranspiration, the slope of the relationship between saturation vapour pressure and
    # temperature, ∆, is required. The slope of the curve (Figure 11) at a given temperature is given by.
    # ∆ = slope of saturation vapour pressure curve at air temperature T [kPa °C ],
    # air_temp = air temperature [°C],
    # exp[..] 2.7183 (base of natural logarithm) raised to the power [..].
    # Values of slope ∆ for different air temperatures are given in Annex 2 (Table 2.4). In the FAO Penman-Monteith
    # equation, where ∆ occurs in the numerator and denominator, the slope of the vapour pressure curve is
    # calculated using mean air temperature.
∆ = (4098 * pow(0.6108, ((17.27 * air_temp) / (air_temp + 237.3))) / (pow(air_temp + 237.3), 2) # EQUATION 13

# EXTRATERRESTRIAL RADIATION (Ra)
from math import pi, sin, cos, tan, acos
    # day_of_the_year = is the number of the day in the year between 1 (1 January) and 365 or 366 (31 December)
dr = 1 + 0.033 * cos(((2 * pi) / 365) * day_of_the_year) # EQUATION 23
δ = 0.409 * sin(((2 * pi) / 365) * day_of_the_year - 1.39) # EQUATION 24
ωs = acos(-tan(φ) * tan (δ)) # EQUATION 25
    # Ra = extraterrestrial radiation [MJ / m * day]
    # dr = inverse relative distance Earth-Sun (Equation 23)
    # φ = latitude [rad] (Equation 22)
    # Gsc = solar constant = 0.0820 MJ m min
    # ωs = sunset hour angle (Equation 25 or 26) [rad]
    # δ = solar decimation (Equation 24) [rad]
Ra = ((24 * 60) / pi) * Gsc * dr * (ωs * sin(φ) * cos(δ) + cos(φ) * cos(δ) * sin(ωs)) # EUQATION 21

# EXTRATERRESTRIAL RADIATION FOR HOURLY OR SHORTER PERIODS (Ra)
    # t = standard clock time at the midpoint of the period [hour]. For example for a period between 14.00 and 15.00 hours, t = 14.5,
    # Lz = longitude of the centre of the local time zone [degrees west of Greenwich]. For example, Lz = 75, 90, 105 and 120° for the Eastern, Central, Rocky Mountain and Pacific time zones (United States) and Lz = 0° for Greenwich, 330° for Cairo (Egypt), and 255° for Bangkok (Thailand),
    # Lm = longitude of the measurement site [degrees west of Greenwich],
    # Sc = seasonal correction for solar time [hour].
    # Of course, ω < -ω s or ω > ω s from Equation 31 indicates that the sun is below the horizon so that, by definition, Ra is zero.
ω = (pi / 12) * ((t + 0.066667 * (Lz - Lm) + Sc) - 12) # EQUATION 31
    # day_of_the_year = is the number of the day in the year between 1 (1 January) and 365 or 366 (31 December)
b = (2 * pi * (day_of_the_year - 81)) / 364 # EQUATION 33
Sc = 0.1645 * sin(2 b) - 0.1255 * cos(b) - 0.025 * sin(b) # EQUATION 32
    # ω = solar time angle at midpoint of hourly or shorter period [rad],
    # t1 = length of the calculation period [hour]: i.e., 1 for hourly period or 0.5 for a 30-minute period.
ωs1 = ω - ((pi * t1) / 24) # EUQATION 29
ωs2 = ω + ((pi * t1) / 24) # EUQATION 30
    # Ra = extraterrestrial radiation in the hour (or shorter) period [MJ / pow(m, 2) * hour]
    # Gsc = solar constant = 0.0820 MJ / pow(m, 2) * min
    # dr = inverse relative distance Earth-Sun (Equation 23)
    # δ = solar declination [rad] (Equation 24)
    # φ = latitude [rad] (Equation 22)
    # ωs1 = solar time angle at beginning of period [rad] (Equation 29)
    # ωs2 = solar time angle at end of period [rad] (Equation 30)
Ra = ((12 * 60) / pi) * Gsc * dr * ((ωs2 - ωs1) * sin(φ) * cos(δ) + cos(φ) * cos(δ) * (sin(ωs2) - sin(ωs1)) ) # EUQATION 28

# DAYLIGHT HOURS (N)
    # ωs = the sunset hour angle in radians given by Equation 25 or 26. Mean values for N
N = (24 / pi) * ωs # EQUATION 34

# SOLAR RADIATION (Rs)
    # If the solar radiation, Rs, is not measured, it can be calculated with the Angstrom formula which relates solar
    # radiation to extraterrestrial radiation and relative sunshine duration:

    # Rs = solar or shortwave radiation [MJ / m * day]
    # n = actual duration of sunshine [hour]
    # N = maximum possible duration of sunshine or daylight hours [hour]
    # n/N = relative sunshine duration [-]
    # Ra = extraterrestrial radiation [MJ / m * day]
    # as = regression constant, expressing the fraction of extraterrestrial radiation reaching the earth on overcast days (n = 0),
    # as + bs = fraction of extraterrestrial radiation reaching the earth on clear days (n = N).
    # Rs is expressed in the above equation in [MJ / m * day]. The corresponding equivalent evaporation in [mm / day] is
    # obtained by multiplying Rs by 0.408 (Equation 20). Depending on atmospheric conditions (humidity, dust) and
    # solar declination (latitude and month), the Angstrom values a s and b s will vary. Where no actual solar radiation
    # data are available and no calibration has been carried out for improved as and bs parameters, the values as = 0.25 and bs = 0.50 are recommended.
Rs = (as + bs * (n / N)) * Ra # EQUATION 35

# CLEAR-SKY SOLAR RADIATION (Rso)
    # The calculation of the clear-sky radiation, Rso, when n = N, is required for computing net longwave radiation.
    # Rso = clear-sky solar radiation [MJ / m * day]
    # as + bs = fraction of extraterrestrial radiation reaching the earth on clear-sky days (n = N)
# --For near sea level or when calibrated values for as and bs are available --
Rso = (as + bs) * Ra # EQUATION 36

# NET SOLAR OR NET SHORTWAVE RADIATION (Rns)
    # Rns = net solar or shortwave radiation [MJ / pow(m, 2) * day]
    # αlbedo = albedo or canopy reflection coefficient, which is 0.23 for the hypothetical grass reference crop [dimensionless]
    # Rs = the incoming solar radiation [MJ / m * day]
    # Rns = is expressed in the above equation in [MJ / pow(m, 2) * day]
Rns = (1 - αlbedo) * Rs # EQUATION 38

# NET LONGWAVE RADIATION (Rnl)
    # Rnl = net outgoing longwave radiation [MJ pow(m, 2) * day]
    # σ = Stefan-Boltzmann constant [4.903 10 -9 MJ / pow(K, 4) * pow(m, 2) * day]
    # T_max_k = maximum absolute temperature during the 24-hour period [K = °C + 273.16]
    # T_min_k = minimum absolute temperature during the 24-hour period [K = °C + 273.16]
    # ea = actual vapour pressure [kPa]
    # Rs / Rso = relative shortwave radiation (limited to ≤ 1.0)
    # Rs = measured or calculated. (Equation 35) solar radiation [MJ / pow(m, 2) * day]
    # Rso = calculated (Equation 36 or 37) clear-sky radiation [MJ / pow(m, 2) * day]
from math import sqrt
Rnl = STEFAN_BOLTZMANN * ((pow(T_max_k, 4) + pow(T_min_k, 4)) / 2) * (0.34 - 0.14 * sqrt(ea)) * (1.35 * (Rs / Rso) - 0.35) # EQUATION 39

# NET RADIATION (Rn)
    # The net radiation (R n ) is the difference between the incoming net shortwave radiation (R ns ) and the outgoing net longwave radiation (R nl )
Rn = Rns - Rnl # EQUATION 40

# SOIL HEAT FLUX (G)
    #
    # -- For day and ten-day periods --
    # As the magnitude of the day or ten-day soil heat flux beneath the grass reference surface is relatively
    # small, it may be ignored and thus:
Gday ≈ 0 # EQUATION 42
    # -- For hourly or shorter periods --
    # For hourly (or shorter) calculations, G beneath a dense cover of grass does not correlate well with air
    # temperature. Hourly G can be approximated during DAYLIGHT periods as:
Ghr = 0.1 * Rn # EQUATION 45
    # and during NIGHTTIME periods as:
Ghr = 0.5 * Rn # EQUATION 46
    # Where the soil is warming, the soil heat flux G is positive. The amount of energy required for this
    # process is subtracted from R n when estimating evapotranspiration.

# WIND PROFILE RELATIONSHIP
    # Wind speeds measured at different heights above the soil surface are different. Surface friction tends
    # to slow down wind passing over it. Wind speed is slowest at the surface and increases with height.
    # For this reason anemometers are placed at a chosen standard height, i.e., 10 m in meteorology and
    # 2 or 3 m in agrometeorology. For the calculation of evapotranspiration, wind speed measured at 2 m
    # above the surface is required. To adjust wind speed data obtained from instruments placed at
    # elevations other than the standard height of 2 m, a logarithmic wind speed profile may be used for
    # measurements above a short grassed surface

    # u2 = wind speed at 2 m above ground surface [m / s]
    # uz = measured wind speed at z m above ground surface [m * s]
    # z = height of measurement above ground surface [m]
    # The corresponding multipliers or conversion factors are given in Annex 2 (Table 2.9) and are plotted in Figure 16.
from math import log
u2 = uz * (4.87 / log(67.8 * z - 5.42))



###############################################################################
#########            CALCULATING ETo
###############################################################################

# ASSUMPTIONS

class ETo():

    '''this is a class to calculate evapotranspiration crop reference:
    The reference surface is a hypothetical grass reference crop with an assumed crop height, surface resistance and an albedo
    The reference surface closely resembles an extensive surface of green, well-watered grass of uniform height, actively growing and completely shading the ground. The fixed surface resistance of 70 s m-1 implies a moderately dry soil surface resulting from about a weekly irrigation frequency.'''

    ### CLASS VARIABLES
    # aerodynamic_resistance
    KARMAN_CONSTANT = 0.41 # [None]
    # surface_resistance
    STOMATAL_RESISTANCE = 100 # [s / m]
    # specific_air_heat_at_constant_pressure
    RATIO_MOLECULAR_WEIGHT_WATER_VAPOUR_AND_DRY_AIR = 0.622
    VAPORIZATION_LATENT_HEAT = 2.45 # [MJ / kg] # This is the latent heat for an air temperature of about 20°C.
    # mean_air_density_at_constant_pressure
    SPECIFIC_GAS_CONSTANT = 0.287 # [kJ / kg * K]



    def __init__(self,  crop_height_ref = 0.12,
                        wind_measurement_height = 2,
                        RH_measurement_height = 2,
                        wind_speed_measurement,
                        atmospheric_pressure = None,
                        elevation_above_sea_level = 10,
                        air_temperature = 25,
                        ):
        # aerodynamic_resistance
        self.crop_height_ref = crop_height_ref # meters
        self.wind_measurement_height = wind_measurement_height
        self.RH_measurement_height = RH_measurement_height
        self.wind_speed_measurement = wind_speed_measurement

        # atmospheric_pressure
        if not atmospheric_pressure:
            self.elevation_above_sea_level = elevation_above_sea_level
            self.atmospheric_pressure = self.average_atmospheric_pressure(self.elevation_above_sea_level)

        #
        self.air_temperature = air_temperature
        # surface_resistance
        # //TODO this surface_Resistance has been calculated already
        self.surface_resistance = 70 # seconds / meter
        self.albedo = 0.23


    def penman_monteith(self):
        # ORIGINAL equation
        # PENMAN-MONTEITH EQUATION
        	# Rn = net radiation
        	# (es - ea) = s the vapour pressure deficit of the air [kPa]
        	# ∆ =  the slope of the saturation vapour pressure temperature relationship
        	# γ = psychrometric constant
        	# rs, ra = (bulk) surface and aerodynamic resistances
        	# Pa = the mean air density at constant pressure
        	# Cp = the specific heat of the air


        # assuming the ideal gas law

        numerator_one = saturation_vapour_pressure_slope * (net_radiation - soil_heat_flux)
        numerator_two =  self.mean_air_density_at_constant_pressure() * self.specific_air_heat_at_constant_pressure() * ((saturation_vapour_pressure - actual_vapour_pressure) / self.aerodynamic_resistance())
        denominator = saturation_vapour_pressure_slope + self.psychrometric_constant() * (1 + (self.surface_resistance() / self.aerodynamic_resistance()))
        return (first + second) / third
        # ƛET = (∆ * (Rn - G) + Pa * Cp * ((es - ea) / ra)) / (∆ + γ * (1 + (rs / ra))) # EQUATION 3
        # return (∆ * (Rn - G) + Pa * Cp * ((es - ea) / ra)) / (∆ + γ * (1 + (rs / ra))) # EQUATION 3



    def aerodynamic_resistance(self):
        # AREODYNAMIC RESISTANCE (ra)
        	# ra = aerodynamic resistances [s pow(m, -1)]
        	# wind_measurement_height = height of wind measurements [m] meters
        	# RH_measurement_height = height of humidity measurements [m] meters
        	# d = zero plane displacement height [m] meters
        	# Zom = roughness length governing momentum transfer [m] meters
        	# Zoh = roughness length governing transfer of heat and vapour [m] meters
        	# k = von Karman's constant, 0.41 [None]
        	# Uz = wind speed at height z [m / s]
        from math import log, pow
        d = (2 / 3) * self.crop_height_ref
        Zom = (2 / 3) * self.crop_height_ref
        Zoh = 0.1 * Zom
        return (log((self.wind_measurement_height - d) / Zom) * log((self.RH_measurement_height - d) / Zoh)) / (pow(Eto.KARMAN_CONSTANT, 2) * self.wind_speed_measurement) # EQUATION 4


    def surface_resistance(self):
        # (BULK) SURFACE RESISTANCE (rs)
        	# rs = (bulk) surface resistances [s pow(m, -1)]
        	# rl = bulk stomatal resistance of the well-illuminated leaf [s pow(m, -1)]
        	# LAI_active = active (sunlit) leaf area index [pow(m, 2) (leaf area) pow(m, -2) (soil surface)] meters
        		# The LAI values for various crops differ widely but values of 3-5 are common for many mature crops. For a given
        		# crop, green LAI changes throughout the season and normally reaches its maximum before or at flowering
        		# LAI further depends on the plant density and the crop variety.
        		# A general equation for LAIactive is: LAI_active = 0.5 LAI
        			# which takes into consideration the fact that generally only the upper half of dense clipped grass is actively
        			# contributing to the surface heat and vapour transfer. For clipped grass a general equation for LAI is:
        			# LAI = 24 * h
        			# where h is the crop height [m] meter
        			# The stomatal resistance, rl of a single leaf has a value of about 100 s m-1 under well-watered conditions
        LAI = 24 * self.crop_height_ref
        LAI_active = 0.5 * LAI
        return ETo.STOMATAL_RESISTANCE / LAI_active # EQUATION 5


    def evapotranspiration_ref(self):
        # REFERENCE CROP EVAPOTRANSPIRATION
        	# ETo = reference evapotranspiration [mm / day]
        	# Rn = net radiation at the crop surface [MJ / (pow(m, 2) * day]
        	# G = soil heat flux density [MJ / (pow(m, 2) * day)]
        	# T = mean daily air temperature at 2 m height [°C]
        	# Uz = wind speed at z or 2 m height [m / s] # calculations should be done at 2 m height
        	# es = saturation vapour pressure [kPa]
        	# ea = actual vapour pressure [kPa]
        	# es - ea = saturation vapour pressure deficit [kPa]
        	# ∆ = slope vapour pressure curve [kPa / °C]
        	# γ = psychrometric constant [kPa / °C]
                # Radiation is MJ / pow(m, 2) * day -> (converted to mm / day) = radiation / 2.45 = 0.408*radiation = [mm / day]
                # (∆ * (Rn - G) + Pa * Cp * ((es - ea) / ra)) / (∆ + γ * (1 + (rs / ra))) # EQUATION 3
        return (0.408 * saturation_vapour_pressure_slope * (net_radiation - soil_heat_flux) + self.psychrometric_constant() * (900 / (T + 273)) * self.wind_speed_measurement * (saturation_vapour_pressure - actual_vapour_pressure)) / (saturation_vapour_pressure_slope + self.psychrometric_constant() * (1 + 0.34 * self.wind_speed_measurement)) # EQUATION 6


    def specific_air_heat_at_constant_pressure(self): # [MJ / kg * celcius]
        # //TODO atmospheric_pressure and psychrometric_constant
        return (psychrometric_constant * ETo.RATIO_MOLECULAR_WEIGHT_WATER_VAPOUR_AND_DRY_AIR * ETo.VAPORIZATION_LATENT_HEAT) / self.atmospheric_pressure #

    def mean_air_density_at_constant_pressure(self): # [kg / pow(m, 3)]
        # considering the ideal gas law
        # //TODO atmospheric_pressure
        virtual_temperature = 1.01 * (self.air_temperature + 273)
        return self.atmospheric_pressure / (virtual_temperature * ETo.SPECIFIC_GAS_CONSTANT)

    def psychrometric_constant(self):
        # PSYCHROMETRICS CONSTANT
        	# γ = psychrometric constant [kPa / °C]
        	 # λ = latent heat of vaporization, 2.45 [MJ / kg]
        	 # Cp = specific heat at constant pressure, 1.013 10-3 [MJ / kg * °C]
        	 # ε = ratio molecular weight of water vapour/dry air = 0.622
        γ = (specific_air_heat_at_constant_pressure * self.atmospheric_pressure) / (ETo.RATIO_MOLECULAR_WEIGHT_WATER_VAPOUR_AND_DRY_AIR * ETo.VAPORIZATION_LATENT_HEAT)  # EQUATION 8
        γ = 0.665e-3 * self.atmospheric_pressure # EQUATION 8

    def average_atmospheric_pressure(self):
        # ATMOSPHERIC PRESSURE [kPa]
        	# z = elevation above sea level [m] meters
        from math import pow
        return 101.3 * pow(((293 - 0.0065 * self.elevation_above_sea_level) / 293), 5.26) # EQUATION 7
