import numpy as np

import openmdao.api as om
import pycycle.api as pyc


class HBTFBuilder(pyc.Cycle):
    '''
    Builder class that creates a single-point pyCycle HBTF model using data from the ADH instance as input. 
    This builder class is based on the pyCycle HBTF example. It sets critical cycle parameters then searches 
    the ADH data for each component of the engine and then adds the appropriate pyCycle class to the OpenMDAO 
    model with associated settings. In then connects the components in the OpenMDAO model using the ADH data.

    TODO:
    - The Balance component connections are still hard coded in this script. Implementing them in the ADH will require some thought
    - The Solver settings are still hard coded in the script
    - Initial guesses and other necessary information for the solver to run still needs to be implemented in the ADH 
    '''

    


    '''COMPONENTS: Class methods used by the builder class to add pyCycle components to the OpenMDAO model'''

    #Add engine elements to model

    def add_compressors(self,compressors):
        for comp in compressors:
            if comp["map_data"] == "FanMap":
                md = pyc.FanMap
                prom_nmech = 'LP_Nmech'
            elif comp["map_data"] == "LPCMap":
                md = pyc.LPCMap
                prom_nmech = 'LP_Nmech'
            elif comp["map_data"] == "HPCMap":
                md = pyc.HPCMap
                prom_nmech = 'HP_Nmech'
            self.add_subsystem(comp["name"], pyc.Compressor(map_data=md, bleed_names=comp["bleed_names"], 
                                                            map_extrap=comp["bleed_names"], promotes_inputs=[('Nmech', prom_nmech)]))

    def add_turbines(self,turbines):
        for turb in turbines:
            if turb["map_data"] == "LPTMap":
                md = pyc.LPTMap
                prom_nmech = 'LP_Nmech'
            elif turb["map_data"] == "HPTMap":
                md = pyc.HPTMap
                prom_nmech = 'HP_Nmech'
            self.add_subsystem(turb["name"], pyc.Compressor(map_data=md, bleed_names=turb["bleed_names"], 
                                                            map_extrap=turb["bleed_names"], promotes_inputs=[('Nmech', prom_nmech)]))

    def add_combustors(self,combustors):
        for comb in combustors:
            self.add_subsystem(comb["name"], pyc.Combustor(fuel_type=comb["fuel_type"]))

    def add_shafts(self,shafts):
        for shaft in shafts: 
            self.add_subsystem(shaft["name"], pyc.Shaft(num_ports=shaft["num_ports"]), promotes_inputs=[('Nmech','{}_Nmech'.format(shaft["nmech_type"]))])

    def add_bleeds(self,bleeds):
        for bleed in bleeds:
            self.add_subsystem(bleed["name"], pyc.BleedOut(bleed_names=bleed["bleed_names"])) 

    def add_flightconditions(self,flightconditions):
        for fc in flightconditions:
            self.add_subsystem(fc["name"], pyc.FlightConditions())

    def add_inlets(self, inlets):
        for inlet in inlets:
            self.add_subsystem(inlet["name"], pyc.Inlet())

    def add_splitters(self, splitters):
        for splitter in splitters:
            self.add_subsystem(splitter["name"], pyc.Splitter())

    def add_ducts(self, ducts):
        for duct in ducts:
            self.add_subsystem(duct["name"], pyc.Duct())

    def add_nozzles(self, nozzles):
        for nozz in nozzles:
            self.add_subsystem(nozz["name"], pyc.Nozzle(nozzType=nozz["nozz_type"],lossCoef=nozz["loss_coef"]))

    #Add balance components to model

    def add_balances(self,balanceComp,balances,design):
        for bal in balances:
            if bal.on_design == design:
                balanceComp.add_balance(bal.balance_name, units=bal.units, eq_units=bal.eq_units,
                                        lower=bal.lower,upper=bal.upper,val=bal.val,use_mult=bal.mult_val)


    '''CONNECTIONS: Class methods used by the builder class to connect pyCycle components in the OpenMDAO model'''

    #Connect the flow between engine elements
    def connect_flow(self, flow_connections):
        for fc in flow_connections:
            self.connect("{}.Fl_O".format(flow_connections[0]),"{}.Fl_I".format(flow_connections[1]))


    #Connect the bleeds flows automatically based on the names specified by the user in the ADH
    #TODO: This is an experiment to see if we can connect components without having the user specify anything other than the names
    #The code is a little bit complicated and will likely be reworked
    def connect_bleeds(self,cycleData):
        #Convert pydantic to a dictionary with the component and bleed information
        componentNames  = set([comp["name"] for comp in cycleData["comps"]] + [turb["name"] for turb in cycleData["turbs"]]  + [bleed["name"] for bleed in cycleData["bleeds"]])
        bleedNames = set([comp["bleed_names"] for comp in cycleData["comps"]] + [turb["bleed_names"] for turb in cycleData["turbs"]]  + [bleed["bleed_names"] for bleed in cycleData["bleeds"]])
        bleedPairs = dict.fromkeys(componentNames, [])
        
        for comp in cycleData["comps"]:
            for bn in comp["bleed_names"]:
                bleedPairs[comp["name"]].append(bn)
        for turb in cycleData["turbs"]:
            for bn in turb["bleed_names"]:
                bleedPairs[turb["name"]].append(bn)
        for bleed in cycleData["bleeds"]:
            for bn in bleed["bleed_names"]:
                bleedPairs[bleed["name"]].append(bn)

        # Go through each bleed, find its components, then connect it in the model
        for bn in bleedNames:
            cWB = [key for key, values in bleedPairs.items() if bn in values]
            self.connect('{}.{}'.format(cWB[0],bn),'{}.{}'.format(cWB[1],bn), connect_stat=False)



    #Connects turbomachinery components to the shafts as specified by the user
    def connect_compturb_to_shafts(self, compturb, shafts, gc):
        for shaft in shafts:
            for i, comp in enumerate(compturb):
                if "{},{}".format(comp["name"],shaft["name"]) in gc:
                    self.connect('{}.trq'.format(comp["name"]),'{}.trq_{}'.format(shaft["name"],str(i)))

    #Connects the nozzle exit conditions to flight condition to get a perfectly expanded nozzle flow
    def connect_nozz_to_fc(self, nozzles, flightconditions):
        for fc in flightconditions:
            for i, nozz in enumerate(nozzles):
                self.connect('{}.Fl_0:stat:P'.format(fc["name"]),'{}.Ps_exhaust'.format(nozz["name"]))


    '''OPENMDAO: Main OpenMDAO setup functions'''

    def initialize(self,cycleData):
        '''May need to be used in this builder class in the future'''
        super().initialize()

    def setup(self,cycleData):
        #Initialize the model here by setting option variables such as a switch for design vs off-des cases. Setup data from ADH

        self.options['throttle_mode'] = cycleData["cycleInfo"]["throttle_mode"]
        design = cycleData["cycleInfo"]["design"]
        
        if cycleData["cycleInfo"]["thermo_method"] == "TABULAR": 
            self.options['thermo_method'] = 'TABULAR'
            self.options['thermo_data'] = pyc.AIR_JETA_TAB_SPEC
        else: 
            self.options['thermo_method'] = 'CEA'
            self.options['thermo_data'] = pyc.species_data.janaf

        #Add all the engine components from the ADH using helper functions
        self.add_flightconditions(cycleData["fc"])
        self.add_inlets(cycleData["inlets"])
        self.add_splitters(cycleData["splitters"])
        self.add_compressors(cycleData["comp"])
        self.add_combustors(cycleData["comb"])
        self.add_turbines(cycleData["turb"])
        self.add_nozzles(cycleData["nozz"])
        self.add_shafts(cycleData["shaft"])
        self.add_bleeds(cycleData["bleeds"])
        self.add_ducts(cycleData["duct"])

        #Hardcode the pyCycle performance group for now until we figure out how to connect this to the ADH
        self.add_subsystem('perf', pyc.Performance(num_nozzles=2, num_burners=1))
        # Now use the explicit connect method to make connections -- connect(<from>, <to>)
        #Connect the inputs to perf group
        self.connect('inlet.Fl_O:tot:P', 'perf.Pt2')
        self.connect('hpc.Fl_O:tot:P', 'perf.Pt3')
        self.connect('burner.Wfuel', 'perf.Wfuel_0')
        self.connect('inlet.F_ram', 'perf.ram_drag')
        self.connect('core_nozz.Fg', 'perf.Fg_0')
        self.connect('byp_nozz.Fg', 'perf.Fg_1')


        #Connect turbo machinery to shafts
        self.connect_compturb_to_shafts(cycleData["comp"],cycleData["shafts"])


        #Ideally expanding flow by conneting flight condition static pressure to nozzle exhaust pressure
        self.connect_nozz_to_fc(cycleData["nozz"], cycleData["fc"])


        ##Add the balance component using the helper function.
        # Balances can be a bit confusing, here's some explanation -
        #   State Variables:
        #           (W)        Inlet mass flow rate to implictly balance thrust
        #                      LHS: perf.Fn  == RHS: Thrust requirement (set when TF is instantiated)
        #
        #           (FAR)      Fuel-air ratio to balance Tt4
        #                      LHS: burner.Fl_O:tot:T  == RHS: Tt4 target (set when TF is instantiated)
        #
        #           (lpt_PR)   LPT press ratio to balance shaft power on the low spool
        #           (hpt_PR)   HPT press ratio to balance shaft power on the high spool
        # Ref: look at the XDSM diagrams in the pyCycle paper and this:
        # http://openmdao.org/twodocs/versions/latest/features/building_blocks/components/balance_comp.html
        if cycleData["balances"] is not None:
            balance = self.add_subsystem('balance', om.BalanceComp())
            self.add_balances(self,balance,cycleData.balances,design)

            self.add_balance(lhs_name="my_)name")



        #TODO: The balance connections are hardcoded here until I can figure out how to implement their specification in the ADH
        if design:
            #balance.add_balance('W', units='lbm/s', eq_units='lbf')
            #Here balance.W is implicit state variable that is the OUTPUT of balance object
            self.connect('balance.W', 'fc.W') #Connect the output of balance to the relevant input
            self.connect('perf.Fn', 'balance.lhs:W')       #This statement makes perf.Fn the LHS of the balance eqn.
            self.promotes('balance', inputs=[('rhs:W', 'Fn_DES')])

            #balance.add_balance('FAR', eq_units='degR', lower=1e-4, val=.017)
            self.connect('balance.FAR', 'burner.Fl_I:FAR')
            self.connect('burner.Fl_O:tot:T', 'balance.lhs:FAR')
            self.promotes('balance', inputs=[('rhs:FAR', 'T4_MAX')])
            
            # Note that for the following two balances the mult val is set to -1 so that the NET torque is zero
            #balance.add_balance('lpt_PR', val=1.5, lower=1.001, upper=8,
                                #eq_units='hp', use_mult=True, mult_val=-1)
            self.connect('balance.lpt_PR', 'lpt.PR')
            self.connect('lp_shaft.pwr_in_real', 'balance.lhs:lpt_PR')
            self.connect('lp_shaft.pwr_out_real', 'balance.rhs:lpt_PR')

            #balance.add_balance('hpt_PR', val=1.5, lower=1.001, upper=8,
                                #eq_units='hp', use_mult=True, mult_val=-1)
            self.connect('balance.hpt_PR', 'hpt.PR')
            self.connect('hp_shaft.pwr_in_real', 'balance.lhs:hpt_PR')
            self.connect('hp_shaft.pwr_out_real', 'balance.rhs:hpt_PR')

        else:
            
            #In OFF-DESIGN mode we need to redefine the balances:
            #   State Variables:
            #           (W)        Inlet mass flow rate to balance core flow area
            #                      LHS: core_nozz.Throat:stat:area == Area from DESIGN calculation 
            #
            #           (FAR)      Fuel-air ratio to balance Thrust req.
            #                      LHS: perf.Fn  == RHS: Thrust requirement (set when TF is instantiated)
            #
            #           (BPR)      Bypass ratio to balance byp. noz. area
            #                      LHS: byp_nozz.Throat:stat:area == Area from DESIGN calculation
            #
            #           (lp_Nmech)   LP spool speed to balance shaft power on the low spool
            #           (hp_Nmech)   HP spool speed to balance shaft power on the high spool

            if self.options['throttle_mode'] == 'T4': 
                #balance.add_balance('FAR', val=0.017, lower=1e-4, eq_units='degR')
                self.connect('balance.FAR', 'burner.Fl_I:FAR')
                self.connect('burner.Fl_O:tot:T', 'balance.lhs:FAR')
                self.promotes('balance', inputs=[('rhs:FAR', 'T4_MAX')])

            elif self.options['throttle_mode'] == 'percent_thrust': 
                #balance.add_balance('FAR', val=0.017, lower=1e-4, eq_units='lbf', use_mult=True)
                self.connect('balance.FAR', 'burner.Fl_I:FAR')
                self.connect('perf.Fn', 'balance.rhs:FAR')
                self.promotes('balance', inputs=[('mult:FAR', 'PC'), ('lhs:FAR', 'Fn_max')])


            #balance.add_balance('W', units='lbm/s', lower=10., upper=1000., eq_units='inch**2')
            self.connect('balance.W', 'fc.W')
            self.connect('core_nozz.Throat:stat:area', 'balance.lhs:W')

            #balance.add_balance('BPR', lower=2., upper=10., eq_units='inch**2')
            self.connect('balance.BPR', 'splitter.BPR')
            self.connect('byp_nozz.Throat:stat:area', 'balance.lhs:BPR')

            # Again for the following two balances the mult val is set to -1 so that the NET torque is zero
            #balance.add_balance('lp_Nmech', val=1.5, units='rpm', lower=500., eq_units='hp', use_mult=True, mult_val=-1)
            self.connect('balance.lp_Nmech', 'LP_Nmech')
            self.connect('lp_shaft.pwr_in_real', 'balance.lhs:lp_Nmech')
            self.connect('lp_shaft.pwr_out_real', 'balance.rhs:lp_Nmech')

            #balance.add_balance('hp_Nmech', val=1.5, units='rpm', lower=500., eq_units='hp', use_mult=True, mult_val=-1)
            self.connect('balance.hp_Nmech', 'HP_Nmech')
            self.connect('hp_shaft.pwr_in_real', 'balance.lhs:hp_Nmech')
            self.connect('hp_shaft.pwr_out_real', 'balance.rhs:hp_Nmech')
            

        # Set up all the engine element flow connections:
        self.connect_flow(cycleData.flow_connections)

        #Bleed flows:
        self.connect_bleeds(cycleData)

        
        #TODO: Specify solver settings which are hardcoded for now:
        newton = self.nonlinear_solver = om.NewtonSolver()
        newton.options['atol'] = 1e-8

        # set this very small, so it never activates and we rely on atol
        newton.options['rtol'] = 1e-99 
        newton.options['iprint'] = 2
        newton.options['maxiter'] = 50
        newton.options['solve_subsystems'] = True
        newton.options['max_sub_solves'] = 1000
        newton.options['reraise_child_analysiserror'] = False
        # ls = newton.linesearch = BoundsEnforceLS()
        ls = newton.linesearch = om.ArmijoGoldsteinLS()
        ls.options['maxiter'] = 3
        ls.options['rho'] = 0.75
        # ls.options['print_bound_enforce'] = True

        self.linear_solver = om.DirectSolver()

        super().setup()