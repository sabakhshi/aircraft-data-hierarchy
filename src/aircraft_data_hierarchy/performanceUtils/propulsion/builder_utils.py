import numpy as np
from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic.v1 import utils
from aircraft_data_hierarchy.common_base_model import CommonBaseModel, Metadata
from aircraft_data_hierarchy.behavior import Behavior, DAVEfunc, FileHeader, Author
from aircraft_data_hierarchy.requirements import Requirement
from aircraft_data_hierarchy.performance import Discipline
from aircraft_data_hierarchy.work_breakdown_structure.propulsion import (
    Propulsion,
    PropulsionCycle,
    FlightConditions,
    Inlet,
    Compressor,
    Splitter,
    Duct,
    Compressor,
    Turbine,
    Bleed,
    Nozzle,
    Shaft,
    Combustor,
    BalanceComponent,
)

def getCycleInfo(ADHInstance):
    cycle = ADHInstance.cycle
    cycleInfo = {
        "name" : cycle.name,
        "design": cycle.design, 
        "thermo_method" : cycle.thermo_method, 
        "thermo_data": cycle.thermo_data, 
        "throttle_mode": cycle.throttle_mode, 
        "fuel_type" : cycle.fuel_type, 
        "global_connections" : cycle.global_connections, 
        "flow_connections": cycle.flow_connections, 
        "solver_settings" : cycle.solver_settings
    }
    return cycleInfo


def getFlightConds(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    for element in engineElements:
        if utils.lenient_isinstance(element, FlightConditions):
            flightConds = {
                "name" : element.name,
                "mn" : element.mn, 
                "alt": element.alt, 
                "d_ts": element.d_ts
            }
            return flightConds
    
def getInlet(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    for element in engineElements:
        if utils.lenient_isinstance(element, Inlet):
            inletData = {
                "name" : element.name,
                "statics" : element.statics, 
                "mn": element.mn, 
                "ram_recovery": element.ram_recovery,
                "area": element.area
            }
            return inletData

def getSplitter(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    splitters = []
    for element in engineElements:
        if utils.lenient_isinstance(element, Splitter):
            splitterData = {
                "name" : element.name,
                "statics" : element.statics, 
                "bpr" : element.bpr, 
                "mn1": element.mn1, 
                "mn2": element.mn2, 
                "area1": element.area1,
                "area2": element.area2
            }
            splitters.append(splitterData)
    return splitters

def getDuct(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    ducts = []
    for element in engineElements:
        if utils.lenient_isinstance(element, Duct):
            ductData = {
                "name" : element.name,
                "statics" : element.statics, 
                "dPqP" : element.dPqP, 
                "mn": element.mn, 
                "Q_dot": element.Q_dot,
                "area" : element.area
            }
            ducts.append(ductData)
    return ducts

def getCompressor(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    compressors = []
    for element in engineElements:
        if utils.lenient_isinstance(element, Compressor):
            compData = {
                "name" : element.name,
                "statics" : element.statics, 
                "map_data" : element.map_data, 
                "map_extrap": element.map_extrap, 
                "map_interp_method" : element.map_interp_method,
                "alpha_map" : element.alpha_map,
                "bleed_names": element.bleed_names,
                "pr_des": element.pr_des,
                "eff_des": element.eff_des,
                "area" : element.area,
                "mn" : element.mn
            }
            compressors.append(compData)
    return compressors

def getCombustor(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    combustors = []
    for element in engineElements:
        if utils.lenient_isinstance(element, Combustor):
            combData = {
                "name" : element.name,
                "statics" : element.statics, 
                "dp_qp" : element.dp_qp, 
                "FAR" : element.FAR, 
                "area" : element.area,
                "mn" : element.mn
            }
            combustors.append(combData)
    return combustors

def getTurbine(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    turbines = []
    for element in engineElements:
        if utils.lenient_isinstance(element, Turbine):
            turbData = {
                "name" : element.name,
                "statics" : element.statics, 
                "map_data" : element.map_data, 
                "map_extrap": element.map_extrap, 
                "map_interp_method" : element.map_interp_method,
                "alpha_map" : element.alpha_map,
                "pr_des": element.pr_des,
                "eff_des": element.eff_des,
                "bleed_names": element.bleed_names,
                "area" : element.area,
                "mn" : element.mn
            }
            turbines.append(turbData)
    return turbines

def getNozzle(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    nozzles = []
    for element in engineElements:
        if utils.lenient_isinstance(element, Nozzle):
            nozzData = {
                "name" : element.name,
                "statics" : element.statics, 
                "nozzType" : element.nozz_type,
                "lossCoef": element.loss_coef,
                "cv": element.cv,
                "area" : element.area,
                "mn" : element.mn
            }
            nozzles.append(nozzData)
    return nozzles

def getShaft(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    shafts = []
    for element in engineElements:
        if utils.lenient_isinstance(element, Shaft):
            shaftData = {
                "name" : element.name,
                "num_ports" : element.num_ports, 
                "nmech" : element.nmech,
                "nemch_type" : element.nmech_type
            }
            shafts.append(shaftData)
    return shafts

def getBleed(ADHInstance):
    engineElements = ADHInstance.cycle.elements
    bleeds = []
    for element in engineElements:
        if utils.lenient_isinstance(element, Bleed):
            bleedData = {
                "name" : element.name,
                "statics" : element.statics, 
                "bleed_names" : element.bleed_names, 
            }
            bleeds.append(bleedData)
    return bleeds

def getBalance(ADHInstance):
    balanceComps = ADHInstance.cycle.balance_components
    balances = []
    for comp in balanceComps:
        if utils.lenient_isinstance(comp, BalanceComponent):
            balanceData = {
                "name" : comp.balance_name,
                "units" : comp.units, 
                "eq_units" : comp.eq_units, 
                "lower" : comp.lower, 
                "upper" : comp.upper, 
                "lhs_name" : comp.lhs_name,
                "rhs_name" : comp.rhs_name,
                "rhs_val" : comp.rhs_val,
                "mult_val" : comp.mult_val,
                "use_mult" : comp.use_mult
            }
            balances.append(balanceData)
    return balances
