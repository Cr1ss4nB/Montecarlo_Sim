import pruebas.control.average_manage as AM
import pruebas.control.variance_manage as VM
import pruebas.control.chi_manage as CM
import pruebas.control.ks_manage as KM
import pruebas.control.poker_manage as PM


passed_data = []


def do(ri):

    global passed_data

    passed_data.clear()

    AM.fastTest(ri)
    
    VM.fastTest(AM.getPassedData())
    
    CM.fastTest(VM.getPassedData())
    
    KM.fastTest(CM.getPassedData())

    PM.fastTest(KM.getPassedData())

    passed_data = PM.getPassedData()


def getPassedData():
    return passed_data