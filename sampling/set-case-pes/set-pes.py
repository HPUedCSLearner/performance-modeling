import json
import os

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

pes_data = load_json("./pes.json")

# print(pes_data['TOTALPES'])

print("./xmlchange -file env_mach_pes.xml -id TOTALPES -val "   + pes_data["TOTALPES"])
print("./xmlchange -file env_mach_pes.xml -id ROOTPE_ATM -val " + pes_data["ROOTPE_ATM"])
print("./xmlchange -file env_mach_pes.xml -id NTASKS_ATM -val " + pes_data["NTASKS_ATM"])
print("./xmlchange -file env_mach_pes.xml -id ROOTPE_LND -val " + pes_data["ROOTPE_LND"])
print("./xmlchange -file env_mach_pes.xml -id NTASKS_LND -val " + pes_data["NTASKS_LND"])
print("./xmlchange -file env_mach_pes.xml -id ROOTPE_ICE -val " + pes_data["ROOTPE_ICE"])
print("./xmlchange -file env_mach_pes.xml -id NTASKS_ICE -val " + pes_data["NTASKS_ICE"])
print("./xmlchange -file env_mach_pes.xml -id ROOTPE_OCN -val " + pes_data["ROOTPE_OCN"])
print("./xmlchange -file env_mach_pes.xml -id NTASKS_OCN -val " + pes_data["NTASKS_OCN"])
print("./xmlchange -file env_mach_pes.xml -id ROOTPE_CPL -val " + pes_data["ROOTPE_CPL"])
print("./xmlchange -file env_mach_pes.xml -id NTASKS_CPL -val " + pes_data["NTASKS_CPL"])
print("./xmlchange -file env_mach_pes.xml -id ROOTPE_ROF -val " + pes_data["ROOTPE_ROF"])
print("./xmlchange -file env_mach_pes.xml -id NTASKS_ROF -val " + pes_data["NTASKS_ROF"])
print("./xmlchange -file env_mach_pes.xml -id ROOTPE_GLC -val " + pes_data["ROOTPE_GLC"])
print("./xmlchange -file env_mach_pes.xml -id NTASKS_GLC -val " + pes_data["NTASKS_GLC"])
print("./xmlchange -file env_mach_pes.xml -id ROOTPE_WAV -val " + pes_data["ROOTPE_WAV"])
print("./xmlchange -file env_mach_pes.xml -id NTASKS_WAV -val " + pes_data["NTASKS_WAV"])

print("./xmlquery STOP_N")
print("./xmlquery STOP_OPTION")

# os.system("./xmlchange -file env_mach_pes.xml -id TOTALPES -val "   + pes_data["TOTALPES"])
# os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_ATM -val " + pes_data["ROOTPE_ATM"])
# os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ATM -val " + pes_data["NTASKS_ATM"])
# os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_LND -val " + pes_data["ROOTPE_LND"])
# os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_LND -val " + pes_data["NTASKS_LND"])
# os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_ICE -val " + pes_data["ROOTPE_ICE"])
# os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ICE -val " + pes_data["NTASKS_ICE"])
# os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_OCN -val " + pes_data["ROOTPE_OCN"])
# os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_OCN -val " + pes_data["NTASKS_OCN"])
# os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_CPL -val " + pes_data["ROOTPE_CPL"])
# os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_CPL -val " + pes_data["NTASKS_CPL"])
# os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_ROF -val " + pes_data["ROOTPE_ROF"])
# os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ROF -val " + pes_data["NTASKS_ROF"])
# os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_GLC -val " + pes_data["ROOTPE_GLC"])
# os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_GLC -val " + pes_data["NTASKS_GLC"])
# os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_WAV -val " + pes_data["ROOTPE_WAV"])
# os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_WAV -val " + pes_data["NTASKS_WAV"])


#  os.system("./xmlquery STOP_N")
#  os.system("./xmlquery STOP_OPTION")
