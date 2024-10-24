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
import aircraft_data_hierarchy.performanceUtils.propulsion.builder_utils as bu


class PropulsionPerformanceBuilder():
    def __init__(self, ADHInstance):
        self.ADHInstance = ADHInstance

    def getInput(self, type):
        if type == "HBTF":
            cycleData = {
                "cycleInfo" : bu.getCycleInfo(self.ADHInstance),

                "fc" : bu.getFlightConds(self.ADHInstance),

                "inlets" : bu.getInlet(self.ADHInstance),
                "splitters" : bu.getSplitter(self.ADHInstance),
                "duct" : bu.getDuct(self.ADHInstance),
                "comp" : bu.getCompressor(self.ADHInstance),
                "comb" : bu.getCombustor(self.ADHInstance),
                "turb" : bu.getTurbine(self.ADHInstance),
                "nozz" : bu.getNozzle(self.ADHInstance),

                "shafts" : bu.getShaft(self.ADHInstance),
                "bleeds" : bu.getBleed(self.ADHInstance),
                "balance" : bu.getBalance(self.ADHInstance)
            }
            
        return cycleData
    
    def transferData(self):
        pass

    def getOutput(self):
        pass


class pyCycleBuilder(PropulsionPerformanceBuilder):
    
    def getInput(self):
        return super().getInput()

    def transferData(self):
        return super().transferData()
    
    def getOutput(self):
        





        return 
    

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
    print(test.getInput("HBTF"))