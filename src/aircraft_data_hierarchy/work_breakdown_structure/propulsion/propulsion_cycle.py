from typing import List, Optional
from pydantic import Field, field_validator
from ...common_base_model import CommonBaseModel



class BalanceComponent(CommonBaseModel):
    """
    Represents a balance component in the engine cycle.

    Attributes:
        balance_name (str): The name of the balance component.
        units (str, optional): The units of the balance component.
        eq_units (str, optional): The units of the equation associated with the balance component.
        lower (float, optional): The lower bound of the balance component.
        upper (float, optional): The upper bound of the balance component.
        lhs_name (str, optional): The name of the left-hand side variable in the balance equation.
        rhs_name (str, optional): The name of the right-hand side variable in the balance equation.
        rhs_val (float, optional): The value of the right-hand side of the balance equation.
        mult_val (float, optional): The multiplier value for the balance component. Defaults to 1.0.
        use_mult (bool, optional): Whether to use the multiplier value. Defaults to False.
    """

    balance_name: str = Field(..., description="The name of the balance component.")
    units: Optional[str] = Field(None, description="The units of the balance component.")
    eq_units: Optional[str] = Field(
        None, description="The units of the equation associated with the balance component."
    )
    lower: Optional[float] = Field(None, description="The lower bound of the balance component.")
    upper: Optional[float] = Field(None, description="The upper bound of the balance component.")
    lhs_name: Optional[str] = Field(
        None, description="The name of the left-hand side variable in the balance equation."
    )
    lhs_val: Optional[float] = Field(None, description="The value of the left-hand side of the balance equation.")
    rhs_name: Optional[str] = Field(
        None, description="The name of the right-hand side variable in the balance equation."
    )
    rhs_val: Optional[float] = Field(None, description="The value of the right-hand side of the balance equation.")
    mult_val: float = Field(1.0, description="The multiplier value for the balance component.")
    use_mult: bool = Field(False, description="Whether to use the multiplier value.")
    on_design: bool = Field(False, description="Should the balance only be used when in design mode.")


class EngineElement(CommonBaseModel):
    """
    Represents an individual element in the engine cycle.

    Attributes:
        name (str): The name of the engine element.
        options (dict, optional): The options associated with the engine element.
    """

    name: str = Field(..., description="The name of the engine element.")
    options: Optional[dict] = Field(None, description="The options associated with the engine element.")

class Shaft(EngineElement):
    """
    Shaft component of the engine.

    Attributes
    ----------
    num_ports : Optional[int]
        Number of ports on the shaft.
    nmech : Optional[float]
        Mechanical speed in RPM.
    """

    num_ports: Optional[int] = Field(None, description="Number of ports on the shaft")
    nmech: Optional[float] = Field(None, description="Mechanical speed in RPM")
    nmech_type: Optional[str] = Field(None, description="Low or high pressure shaft")

class Bleed(EngineElement):
    """
    Bleed output component

    Attributes
    ----------
    bleed_names : Optional[List[str]]
        Names of the bleed connections associated
    statics : Optional[bool]
        If true calculate static properties
    """

    bleed_names: Optional[List[str]] = Field(None, description="Names of the bleed connections associated")
    statics : Optional[bool] = Field(None, description="If true calculate static properties")



class OffDesignPoint(CommonBaseModel):
    """
    Represents an off-design point in a multi-point cycle analysis.

    Attributes:
        name (str): The name of the off-design point.
        parameters (dict): The parameter values for the off-design point.
    """

    name: str = Field(..., description="The name of the off-design point.")
    parameters: dict = Field(..., description="The parameter values for the off-design point.")


class FlightConditions(EngineElement):
    """
    Flight conditions for the engine.

    Attributes
    ----------
    mn : Optional[float]
        Mach number.
    alt : Optional[float]
        Altitude in feet.
    d_ts : Optional[float]
        Temperature deviation in degrees Rankine.
    """

    mn: Optional[List[float]] = Field(None, description="Mach number")
    alt: Optional[List[float]] = Field(None, description="Altitude in feet")
    d_ts: Optional[float] = Field(None, description="Temperature deviation in degrees Rankine")


class Inlet(EngineElement):
    """
    Inlet conditions for the engine.

    Attributes
    ----------
    mn : Optional[float]
        Mach number.
    ram_recovery : Optional[float]
        Ram recovery factor.
    """
    
    statics : Optional[bool] = Field(None, description="If true calculate static properties")
    mn: Optional[float] = Field(None, description="Mach number")
    ram_recovery: Optional[float] = Field(None, description="Ram recovery factor")
    area: Optional[float] = Field(None, description="Frontal area of component")


class Compressor(EngineElement):
    """
    Compressor component of the engine.

    Attributes
    ----------
    mn : Optional[float]
        Mach number.
    map_data : Optional[str]
        Map data for the compressor.
    bleed_names : Optional[List[str]]
        Names of the bleed ports.
    map_extrap : Optional[bool]
        Flag to indicate if map extrapolation is used.
    pr_des : Optional[float]
        Design condition pressure ratio
    eff_des : Optional[float]
        Design condition efficeincy
    """

    mn: Optional[float] = Field(None, description="Mach number")
    statics : Optional[bool] = Field(None, description="If true calculate static properties")
    map_data: Optional[str] = Field(None, description="Map data for the compressor")
    map_extrap: Optional[bool] = Field(None, description="Flag to indicate if map extrapolation is used")
    map_interp_method: Optional[str] = Field(None, description="Method to use for map interpolation.")
    alpha_map: Optional[str] = Field(None, description="Alpha Map")
    bleed_names: Optional[List[str]] = Field(None, description="Names of the bleed ports")
    pr_des : Optional[float] = Field(None, description="Design condition pressure ratio")
    eff_des : Optional[float] = Field(None, description="Design condition efficeincy")
    area: Optional[float] = Field(None, description="Frontal area of component")


class Splitter(EngineElement):
    """
    Splitter component of the engine.

    Attributes
    ----------
    bpr : Optional[float]
        Bypass ratio.
    mn1 : Optional[float]
        Mach number for the first flow path.
    mn2 : Optional[float]
        Mach number for the second flow path.
    area1 : Optional[float]
        Area for the second flow path.
    area2 : Optional[float]
        Area for the second flow path.
    """

    statics : Optional[bool] = Field(None, description="If true calculate static properties")
    bpr: Optional[float] = Field(None, description="Bypass ratio")
    mn1: Optional[float] = Field(None, description="Mach number for the first flow path")
    mn2: Optional[float] = Field(None, description="Mach number for the second flow path")
    area1: Optional[float] = Field(None, description="Frontal area for the first flow path")
    area2: Optional[float] = Field(None, description="Frontal area for the second flow path")


class Duct(EngineElement):
    """
    Duct component of the engine.

    Attributes
    ----------
    mn : Optional[float]
        Mach number.
    dp_qp : Optional[float]
        Pressure drop ratio.
    """

    statics : Optional[bool] = Field(None, description="If true calculate static properties")
    mn: Optional[float] = Field(None, description="Mach number")
    dPqP: Optional[float] = Field(None, description="Pressure drop ratio")
    Q_dot: Optional[float] = Field(None, description="heat flow rate into (positive) or out of (negative) the air")
    area: Optional[float] = Field(None, description="Frontal area of component")


class Combustor(EngineElement):
    """
    Combustor component of the engine.

    Attributes
    ----------
    fuel_type : Optional[str]
        Type of fuel used.
    mn : Optional[float]
        Mach number.
    dp_qp : Optional[float]
        Pressure drop ratio.
    """
    statics : Optional[bool] = Field(None, description="If true calculate static properties")
    fuel_type: Optional[str] = Field(None, description="Type of fuel used")
    mn: Optional[float] = Field(None, description="Mach number")
    dp_qp: Optional[float] = Field(None, description="Pressure drop ratio")
    FAR: Optional[float] = Field(None, description="Fuel-air ratio")
    area: Optional[float] = Field(None, description="Frontal area of component")


class Turbine(EngineElement):
    """
    Turbine component of the engine.

    Attributes
    ----------
    mn : Optional[float]
        Mach number.
    map_data : Optional[str]
        Map data for the turbine.
    bleed_names : Optional[List[str]]
        Names of the bleed ports.
    map_extrap : Optional[bool]
        Flag to indicate if map extrapolation is used.
    pr_des : Optional[float]
        Design condition pressure ratio
    effDes : Optional[float]
        Design condition efficeincy
    """
    statics : Optional[bool] = Field(None, description="If true calculate static properties")
    mn: Optional[float] = Field(None, description="Mach number")
    map_data: Optional[str] = Field(None, description="Map data for the turbine")
    bleed_names: Optional[List[str]] = Field(None, description="Names of the bleed ports")
    map_extrap: Optional[bool] = Field(None, description="Flag to indicate if map extrapolation is used")
    map_interp_method: Optional[str] = Field(None, description="Method to use for map interpolation.")
    alpha_map: Optional[str] = Field(None, description="Alpha Map")
    bleed_names: Optional[List[str]] = Field(None, description="Names of the bleed ports")
    pr_des : Optional[float] = Field(None, description="Design condition pressure ratio")
    eff_des : Optional[float] = Field(None, description="Design condition efficeincy")
    area: Optional[float] = Field(None, description="Frontal area of component")


class Nozzle(EngineElement):
    """
    Nozzle component of the engine.

    Attributes
    ----------
    nozz_type : Optional[str]
        Type of nozzle.
    loss_coef : Optional[str]
        Loss coefficient.
    cv : Optional[float]
        Discharge coefficient.
    """
    statics : Optional[bool] = Field(None, description="If true calculate static properties")
    mn: Optional[float] = Field(None, description="Mach number")
    nozz_type: Optional[str] = Field(None, description="Type of nozzle")
    loss_coef: Optional[str] = Field(None, description="Loss coefficient")
    cv: Optional[float] = Field(None, description="Discharge coefficient")
    area: Optional[float] = Field(None, description="Frontal area of component")





class Performance(EngineElement):
    """
    Performance metrics of the engine.

    Attributes
    ----------
    num_nozzles : Optional[int]
        Number of nozzles.
    num_burners : Optional[int]
        Number of burners.
    pt2 : Optional[float]
        Total pressure at station 2.
    pt3 : Optional[float]
        Total pressure at station 3.
    wfuel_0 : Optional[float]
        Fuel flow rate.
    ram_drag : Optional[float]
        Ram drag.
    fg_0 : Optional[float]
        Gross thrust from core nozzle.
    fg_1 : Optional[float]
        Gross thrust from bypass nozzle.
    fn : Optional[float]
        Net thrust.
    opr : Optional[float]
        Overall pressure ratio.
    tsfc : Optional[float]
        Thrust specific fuel consumption.
    """

    num_nozzles: Optional[int] = Field(None, description="Number of nozzles")
    num_burners: Optional[int] = Field(None, description="Number of burners")
    pt2: Optional[float] = Field(None, description="Total pressure at station 2")
    pt3: Optional[float] = Field(None, description="Total pressure at station 3")
    wfuel_0: Optional[float] = Field(None, description="Fuel flow rate")
    ram_drag: Optional[float] = Field(None, description="Ram drag")
    fg_0: Optional[float] = Field(None, description="Gross thrust from core nozzle")
    fg_1: Optional[float] = Field(None, description="Gross thrust from bypass nozzle")
    fn: Optional[float] = Field(None, description="Net thrust")
    opr: Optional[float] = Field(None, description="Overall pressure ratio")
    tsfc: Optional[float] = Field(None, description="Thrust specific fuel consumption")


class PropulsionCycle(CommonBaseModel):
    """
    Represents a complete engine cycle.

    Attributes:
        name (str): The name of the engine cycle.
        design (bool): Whether the engine cycle is in design mode.
        thermo_method (str, optional): The thermodynamic method used in the engine cycle. Defaults to 'CEA'.
        thermo_data (str, optional): The thermodynamic data used in the engine cycle.
        elements (List[EngineElement]): The list of engine elements in the engine cycle.
        balance_components (List[BalanceComponent], optional): The list of balance components in the engine cycle.
        global_connections (dict, optional): The global connections in the engine cycle.
        flow_connections (dict, optional): The flow connections in the engine cycle.
        solver_settings (dict, optional): The solver settings for the engine cycle.
    """

    name: str = Field(..., description="The name of the engine cycle.")
    design: bool = Field(..., description="Whether the engine cycle is in design mode.")
    thermo_method: str = Field("TABULAR", description="The thermodynamic method used in the engine cycle.")
    thermo_data: Optional[str] = Field(None, description="The thermodynamic data used in the engine cycle.")
    throttle_mode: str = Field("T4", description="What quanity should be used to throttle engine for off-design cases.")
    fuel_type: str = Field("FAR", description="Type of fueld considered for the cycle.")
    elements: List[EngineElement] = Field(..., description="The list of engine elements in the engine cycle.")
    balance_components: Optional[List[BalanceComponent]] = Field(
        None, description="The list of balance components in the engine cycle."
    )
    global_connections: Optional[dict] = Field(None, description="The global connections in the engine cycle.")
    flow_connections: Optional[dict] = Field(None, description="The flow connections in the engine cycle.")
    solver_settings: Optional[dict] = Field(None, description="The solver settings for the engine cycle.")

    @field_validator("thermo_method")
    def validate_thermo_method(cls, v):
        allowed_methods = ["CEA", "TABULAR"]
        if v not in allowed_methods:
            raise ValueError(f"Thermodynamic method must be one of {allowed_methods}")
        return v
    
    @field_validator("throttle_mode")
    def validate_throttle_mode(cls, v):
        allowed_methods = ["T4", "percent_throttle"]
        if v not in allowed_methods:
            raise ValueError(f"Throttle mode must be one of {allowed_methods}")
        return v
    
    @field_validator("fuel_type")
    def validate_fuel_type(cls, v):
        allowed_types = ["FAR", "Jet-A(g)"]
        if v not in allowed_types:
            raise ValueError(f"Fuel type must be one of {allowed_types}")
        return v


class MultiPointCycle(CommonBaseModel):
    """
    Represents a multi-point cycle analysis.

    Attributes:
        design_point (PropulsionCycle): The design point engine cycle.
        od_points (List[OffDesignPoint]): The list of off-design points.
        global_des_od_connections (dict, optional): The global design-to-off-design connections.
        design_constants (dict, optional): The design constants for the multi-point cycle analysis.
        seq_points (List[str], optional): The sequence of points in the multi-point cycle analysis.
    """

    design_point: PropulsionCycle = Field(..., description="The design point engine cycle.")
    od_points: List[OffDesignPoint] = Field(..., description="The list of off-design points.")
    global_des_od_connections: Optional[dict] = Field(None, description="The global design-to-off-design connections.")
    design_constants: Optional[dict] = Field(
        None, description="The design constants for the multi-point cycle analysis."
    )
    seq_points: Optional[List[str]] = Field(
        None, description="The sequence of points in the multi-point cycle analysis."
    )
