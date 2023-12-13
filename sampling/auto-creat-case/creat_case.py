#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import string
import shutil
import re
import json
# import thread
import time

model_dir = "/public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0"

create_scripts_path = "./scripts/create_newcase -case "
create_scripts_args = " -res f09_g16 -compset B1850C5PMBPRP -mach bscc-a6 "
create_scripts_pes  = " -pes_file ./scripts/f09g16_1024_pes_file_bscc-a2.xml"

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def build_case(case_name):
    command = './' + case_name + '.build'
    print("------command:", command)
    #os.system(command)
    os.system('pwd')
    print("------build command done!!!")
    time.sleep(300)



json_data = load_json("./config.json")

for caseConfig in json_data["sampleTimes"]:
    # 判断是否创建case
    if caseConfig["isCreate"] != "True":
        print "isCreadte is configed not True, do not create this cases"
        continue
    
    # 配置预解析
    case_name = caseConfig["caseName"]
    case_path = json_data["casePath"] + case_name
    STOP_N = caseConfig["stopN"]
    STOP_OPTION = caseConfig["stopN-unit"]
    layOut = caseConfig["processLayOut"]
    linkLibFlag  = json_data["libconfig"]["staticLibPath"] + " " + json_data["libconfig"]["staticLibName"] + " "
    linkLibFlag += json_data["libconfig"]["sharedLibPath"] + " " + json_data["libconfig"]["sharedLibName"]
    
    os.chdir(model_dir)
    
    # 创建CASE
    command = create_scripts_path + case_path +  create_scripts_args + create_scripts_pes
    os.system(command)
    
    os.chdir(case_path)
    
    # 设置进程布局，主要是修改这个文件env_mach_pes.xml 
    os.system("./xmlchange -file env_mach_pes.xml -id TOTALPES -val "   + layOut["TOTALPES"])
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_ATM -val " + layOut["ROOTPE_ATM"])
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ATM -val " + layOut["NTASKS_ATM"])
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_LND -val " + layOut["ROOTPE_LND"])
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_LND -val " + layOut["NTASKS_LND"])
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_ICE -val " + layOut["ROOTPE_ICE"])
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ICE -val " + layOut["NTASKS_ICE"])
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_OCN -val " + layOut["ROOTPE_OCN"])
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_OCN -val " + layOut["NTASKS_OCN"])
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_CPL -val " + layOut["ROOTPE_CPL"])
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_CPL -val " + layOut["NTASKS_CPL"])
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_ROF -val " + layOut["ROOTPE_ROF"])
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_ROF -val " + layOut["NTASKS_ROF"])
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_GLC -val " + layOut["ROOTPE_GLC"])
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_GLC -val " + layOut["NTASKS_GLC"])
    os.system("./xmlchange -file env_mach_pes.xml -id ROOTPE_WAV -val " + layOut["ROOTPE_WAV"])
    os.system("./xmlchange -file env_mach_pes.xml -id NTASKS_WAV -val " + layOut["NTASKS_WAV"])
    
    # 备份源码到自己算例中 && env_case.xml
    os.system("mkdir sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/models ./sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/scripts ./sampling")
    os.system("cp -r /public1/home/fio_climate_model/FIO-ESM/fioesm/fioesm2_0/tools ./sampling")
    
    # os.system("./xmlchange -file env_case.xml -id CCSMROOT -val " + case_path + "/sampling")
    os.system("./xmlchange -file env_case.xml -id CCSMROOT -val '$CASEROOT/sampling'")
    os.system("./xmlchange -file env_case.xml -id CCSM_MACHDIR -val '$CCSMROOT/scripts/ccsm_utils/Machines'")
    os.system("cp ./env_case.xml ./LockedFiles/env_case.xml.locked")
    
    #env_build.xml��ģ�͹�������
    os.system("./xmlchange -file env_build.xml -id EXEROOT -val '$CASEROOT/bld'")
    
    #env_run.xml����������
    #STOP_N value: none,never,nsteps,nstep,nseconds,nsecond,nminutes,nminute,nhours,nhour,ndays,nday,nmonths,nmonth,nyears,nyear,date,ifdays0,end (char)
    os.system("./xmlchange -file env_run.xml -id RUNDIR -val '$CASEROOT/run'")
    os.system("./xmlchange -file env_run.xml -id STOP_N -val " + STOP_N)
    os.system("./xmlchange -file env_run.xml -id STOP_OPTION -val " + STOP_OPTION)
    os.system("./xmlchange -file env_run.xml -id DOUT_S_ROOT -val '$CASEROOT/archive'")
    
    #cesm_setup (��Ҫ�ж��Ƿ�setup�ɹ�)

    os.system("./cesm_setup > ./case_setup.log 2>&1") ##* Ӧ��Ϊ./cesm_setup >> ./casename.log 2>&1��casename��Ҫ�ñ�����ָ��һ�£�
    ##* �����˼�������ǽ���Ļ���ȫ�Ž�һ����������Ϊ���ֵ�log�ļ��У��ж��Ƿ�setup��build��run�ɹ���ͨ���Ӹ�log�в�����Ӧ��䣬�Լ��鿴�������̵���Ļ���������Ҫÿһ������һ��log
   
   # ������ �޸�Macros (ĳЩ�������ã����벻��)
    # with open( './Macros', 'r') as macros_old, open('./Macros' + ".new", 'w') as macros_new:
	# 	for line in macros_old:
	# 		if re.match(r'\s*FFLAGS\s*:=', line):
	# 			line = line.strip() + ' -mcmodel=medium \n'
	# 			#line = line
    #         macros_new.write(line)
    #     command = "mv" + ' Macros' + ' Macros' + '.previous'
    #     os.system(command)
    #     command = 'mv' + ' Macros' + '.new' + ' Macros'
    #     os.system(command)
		
    if caseConfig["isInstrument"] == "True":
        # 修改 Macros
        with open( './Macros', 'r') as macros_old, open('./Macros' + ".new", 'w') as macros_new:
            for line in macros_old:
                if re.match(r'\s*FFLAGS\s*:=', line):
                    line = line.strip() + ' -g -finstrument-functions -mcmodel=medium \n'
                    #line = line
                macros_new.write(line)
        command = "mv" + ' Macros' + ' Macros' + '.previous'
        os.system(command)
        command = 'mv' + ' Macros' + '.new' + ' Macros'
        os.system(command)
    
        # 修改 Makefile
        with open( './Tools/Makefile', 'r') as Makefile_old, open('./Tools/Makefile' + ".new", 'w') as Makefile_new:
            for line in Makefile_old:
                if re.search( "\$\(LD\) -o \$\(EXEC_SE\)", line):
                    line = line.rstrip('\n') + ' ' + linkLibFlag + '\n'
                    #print line
                Makefile_new.write(line)
        command = 'mv' + ' ./Tools/Makefile' + ' ./Tools/Makefile' + '.previous'
        os.system(command)
        command = 'mv' + ' ./Tools/Makefile' + '.new' + ' ./Tools/Makefile'
        os.system(command)
        
        
        # 屏蔽 模式中gptl源码接口
        print("we will change below source files")
        print(json_data["modifyGptl"]["item1"])
        print(json_data["modifyGptl"]["item2"])
        print(json_data["modifyGptl"]["item3"])
        print(json_data["modifyGptl"]["item4"])
        command = "sed" + " 's/__cyg/__ban__cyg/g' " + json_data["modifyGptl"]["item1"] + " -i"
        os.system(command)
        command = "sed" + " 's/__cyg/__ban__cyg/g' " + json_data["modifyGptl"]["item2"] + " -i"
        os.system(command)
        command = "sed" + " 's/__cyg/__ban__cyg/g' " + json_data["modifyGptl"]["item3"] + " -i"
        os.system(command)
        command = "sed" + " 's/__cyg/__ban__cyg/g' " + json_data["modifyGptl"]["item4"] + " -i"
        os.system(command)
        
        
        # 创建 export环境变量的脚本
        with open('./setSharedLibEnv.sh', 'w') as setEnv_sh:
            line1 = 'export LD_LIBRARY_PATH='
            line1Letf = json_data["libconfig"]["sharedLibPath"]
            line1 += line1Letf[3:]
            line1 += "\n"
            line2 = 'export LD_LIBRARY_PATH=/public1/soft/intel/2017/compilers_and_libraries/linux/lib/intel64:$LD_LIBRARY_PATH\n'
            setEnv_sh.write(line1)
            setEnv_sh.write(line2)
        command = "chmod +x ./setSharedLibEnv.sh"
        os.system(command)
            
        # 区分模块
        if caseConfig["isDistinguishModules"] == "True":
            libPath = json_data["libconfig"]["staticLibPath"][3:]
            srcsFilePath = libPath + "/" + "distinguishModules/ccsm_comp_mod.template"
            destFilePath = "./sampling/models/drv/driver/ccsm_comp_mod.F90"
            destFilePathBak = "./sampling/models/drv/driver/ccsm_comp_mod.F90.bak"
            command = "mv" + " " + destFilePath + " " + destFilePathBak
            os.system(command)
            command = "cp" + " " + srcsFilePath + " " + destFilePath
            os.system(command)
        
    # ����ģʽ
    # command = './' + case_name + '.build'
    # os.system(command)
    #try:
    #   thread.start_new_thread( build_case, (case_name,) )
    #except:
    #   print "Error: unable to start thread"

