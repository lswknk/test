from core.Device import *


class WindGenerator(Device):
    """
        Define a class of WindGenerator.
    """

    def __init__(self, name):
        super().__init__(name)
        self.input_variables = []
        self.output_variables = ['elec']

        self.maxCap = 1500  # 切出功率
        self.minCap = 200  # 切入功率
        self.pAbandoning = 100.0
        self.pStartup = 0
        self.pShutDn = 0
        self.pMaintenance = 0

    def run(self):
        print_4s('# device: ' + self.name)
        self.declareBasicVars(self.input_variables, self.output_variables)
        self.declareOnOffVars()
        self.modelConstraints()
        print('')

    def modelConstraints(self):
        # maximum and minimum capacity
        print_4s('for i in range(t_num):')
        print_8s('prob += ' + self.nameElecOut + '[i] - ' + self.nameFlag + '[i] * ' + str(
            self.maxCap) + ' <= 0')
        print_8s('prob += ' + self.nameElecOut + '[i] - ' + self.nameFlag + '[i] * ' + str(
            self.minCap) + ' >= 0')
