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


class PropulsionPerformanceBuilder():
    def __init__(self, ADHInstance):
        self.ADHInstance = ADHInstance

    def getCycleInfo(self):
        cycle = self.ADHInstance.cycle
        cycleInfo = {
            "name" : cycle.name,
            "isDesign": cycle.design, 
            "thermo_method" : cycle.thermo_method, 
            "thermo_data": cycle.thermo_data, 
            "throttle_mode": cycle.throttle_mode, 
            "fuel_type" : cycle.fuel_type, 
            "global_connections" : cycle.global_connections, 
            "flow_connections": cycle.flow_connections, 
            "solver_settings" : cycle.solver_settings
        }
        return cycleInfo


    def getFlightConds(self):
        engineElements = self.ADHInstance.cycle.elements
        for element in engineElements:
            if utils.lenient_isinstance(element, FlightConditions):
                flightConds = {
                    "name" : element.name,
                    "mn" : element.mn, 
                    "alt": element.alt, 
                    "d_ts": element.d_ts
                }
                return flightConds
        
    def getInlet(self):
        engineElements = self.ADHInstance.cycle.elements
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

    def getSplitter(self):
        engineElements = self.ADHInstance.cycle.elements
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

    def getDuct(self):
        engineElements = self.ADHInstance.cycle.elements
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

    def getCompressor(self):
        engineElements = self.ADHInstance.cycle.elements
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

    def getCombustor(self):
        engineElements = self.ADHInstance.cycle.elements
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

    def getTurbine(self):
        engineElements = self.ADHInstance.cycle.elements
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

    def getNozzle(self):
        engineElements = self.ADHInstance.cycle.elements
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

    def getShaft(self):
        engineElements = self.ADHInstance.cycle.elements
        shafts = []
        for element in engineElements:
            if utils.lenient_isinstance(element, Shaft):
                shaftData = {
                    "name" : element.name,
                    "num_ports" : element.num_ports, 
                    "nmech" : element.nmech,
                }
                shafts.append(shaftData)
        return shafts

    def getBleed(self):
        engineElements = self.ADHInstance.cycle.elements
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

    def getBalance(self):
        balanceComps = self.ADHInstance.cycle.balance_components
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

        

    def getInput(self):

        #Get Cycle info
        cycleInfo = self.getCycleInfo()

        #Get flight conds
        fc = self.getFlightConds()

        #HBTF data

        inlets = self.getInlet()
        splitter = self.getSplitter()
        duct = self.getDuct()
        comp = self.getCompressor()
        comb = self.getCombustor()
        turb = self.getTurbine()
        nozz = self.getNozzle()

        shaft = self.getShaft()
        bleeds = self.getBleed()

        balance = self.getBalance()




        return 
    
    def transferData(self):
        pass

    def getOutput(self):
        pass


class pyCycleBuilder(PropulsionPerformanceBuilder):
    
    def getInput(self):
        super().getInput()
    

class NPSSBuilder(PropulsionPerformanceBuilder):
    def __init__(self, ADHInstance):
        raise Exception('NPSS Builder not implemented!')


if __name__ == "__main__":

    #Set-up the ADH Propulsion instance for demo purposes

    metadata = Metadata(key="example_key", value="example_value")

    fc = FlightConditions(name="fc", mn=[0.8], alt=[35000])
    inlet = Inlet(name="inlet")
    fan = Compressor(name="fan")
    splitter = Splitter(name="splitter")
    duct4 = Duct(name="duct4")
    lpc = Compressor(name="lpc")
    duct6 = Duct(name="duct6")
    hpc = Compressor(name="hpc", bleed_names=["cool1", "cool2", "cust"])
    bld3 = Bleed(name="bld3", bleed_names=["cool3", "cool4"])
    burner = Combustor(name="burner")
    hpt = Turbine(name="hpt", bleed_names=["cool3", "cool4"])
    duct11 = Duct(name="duct11")
    lpt = Turbine(name="lpt", bleed_names=["cool1", "cool2"])
    duct13 = Duct(name="duct13")
    core_nozz = Nozzle(name="core_nozzle", nozz_type="CV", loss_coef="Cv")
    byp_bld = Bleed(name="byp_bld", bleed_names=["bypBld"])
    duct15 = Duct(name="duct15")
    byp_nozz = Nozzle(name="byp_nozz", nozz_type="CV", loss_coef="Cv")
    lp_shaft = Shaft(name="lp_shaft", num_ports=3)
    hp_shaft = Shaft(name="hp_shaft", num_ports=2)

    #Set PR and eff
    fan.pr_des = 1.685
    fan.eff_des = 0.8948

    lpc.pr_des = 1.935
    lpc.eff_des = 0.9243

    hpc.pr_des = 9.369
    hpc.eff_des = 0.8707
    
    cycle = PropulsionCycle(
        name="Cycle",
        design=True,
        elements=[
            fc,
            inlet,
            fan,
            splitter,
            duct4,
            lpc,
            duct6,
            hpc,
            bld3,
            burner,
            hpt,
            duct11,
            lpt,
            duct13,
            core_nozz,
            byp_bld,
            duct15,
            byp_nozz,
            lp_shaft,
            hp_shaft,
        ],
        thermo_method="TABULAR",
        throttle_mode="T4",
        fuel_type="FAR",
        balance_components=[],
    )

    file_header = FileHeader(name="engineDeck", author=[Author(name="Safa Bakhshi")])

    ADHInstance = Propulsion(
        name="Engine",
        description="Main engine component",
        requirements=[
            Requirement(
                name="Req1",
                description="Requirement 1",
                priority="High",
                verification_method="Test",
                status="Open",
                acceptance_criteria="Criteria 1",
            )
        ],
        subcomponents=[],
        metadata=metadata,
        cycle=cycle,
        performance=[Discipline(name="Performance1", description="Performance description")],
        temp_behavior=DAVEfunc(file_header=file_header),
    )


    test = PropulsionPerformanceBuilder(ADHInstance)
    test.getInput()