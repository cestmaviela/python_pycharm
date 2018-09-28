#!/bin/python
import os
import sys

#support flag of this script
support_vsu_dat=0
support_upgrade=1

# you can edit this segment as neeeded
def_upload_log_dir      = '/POAP_LOG/'
def_upload_status_dir   = '/POAP_STATUS/'
def_upload_startup_dir  = '/POAP_STARTUP/'
def_download_cfg_dir    = '/POAP_CFG/'
def_download_image_dir  = '/POAP_IMAGE/'
def_cfg_suffix          = '.cfg'
def_startup_suffix      = '.POAP'
def_params_suffix       = '.params'

# if no file [sn].params on tftp-server, set no_params_file = True
no_params_file          = False
# if no_params_file == True, you can indicate image-name here
image_name              = ''
# if option 66 is not configured on DCHP-server, you can indicate tftp-server-ip here
tftp_ip                 = ''
# if uploading file to tftp server is forbidden, set file_upload_forbiden = True
file_upload_forbiden    = True

# edit this segment carefully
sn_path='/tmp/dm/.dev_sn'
loclog_file='/tmp/sn.log'
zam_file='/etc/zam.txt'
log_file_path = '/data/'
cli_result_log='/tmp/vsd/0/oam/zam/zam_cli.log'
tftp_ip_file = '/etc/zam_tftp_ip.txt'
zam_second_run_file_name = 'zam_script_exec.text'
check_reload_file_name = 'zam_script_reload.flag'
zam_second_run_file = '/data/' + zam_second_run_file_name
check_reload_file = '/data/' + check_reload_file_name
SELF_PID=os.getpid()

sn_val=''
port_type='MGMT'
log_file=''
def_image_name=''

def clear_all_file():
    try:
        if os.path.exists('/etc/zam.txt'):
            os.remove('/etc/zam.txt')
        if os.path.exists('/data/'+sn_val+ def_cfg_suffix):
            os.remove('/data/'+sn_val+ def_cfg_suffix)
        if os.path.exists('/data/'+sn_val+ def_startup_suffix):
            os.remove('/data/'+sn_val+ def_startup_suffix)
        if os.path.exists('/data/'+sn_val+ def_params_suffix):
            os.remove('/data/'+sn_val+ def_params_suffix)
        if os.path.exists('/data/'+sn_val+'.ok'):
            os.remove('/data/'+sn_val+'.ok')
        if os.path.exists('/data/'+sn_val+'.error'):
            os.remove('/data/'+sn_val+'.error')
        if os.path.exists(log_file):
            os.remove(log_file)
    except BaseException as e:
        print("zam.py clear_file:%",e)

def clear_file():
    try:
        if os.path.exists('/data/'+sn_val+ def_cfg_suffix):
            os.remove('/data/'+sn_val+ def_cfg_suffix)
        if os.path.exists('/data/'+sn_val+ def_startup_suffix):
            os.remove('/data/'+sn_val+ def_startup_suffix)
        if os.path.exists('/data/'+sn_val+ def_params_suffix):
            os.remove('/data/'+sn_val+ def_params_suffix)
        if os.path.exists('/data/'+sn_val+'.ok'):
            os.remove('/data/'+sn_val+'.ok')
        if os.path.exists('/data/'+sn_val+'.error'):
            os.remove('/data/'+sn_val+'.error')
    except BaseException as e:
        print("zam.py clear_file:%",e)
        
def del_cli_file():
    try:
        if os.path.exists(cli_result_log):
            os.remove(cli_result_log)
    except BaseException as e:
        print("zam.py clear_file:%",e)
        
def check_self_pid():
    if os.path.exists(zam_file):
        fileHandle=open(zam_file,'r')
        tmp_pid=fileHandle.readline()
        fileHandle.close()
    write_file(zam_file,str(SELF_PID))

def print_console(val):
    fileHandle=open('/dev/ttyS0','w')
    fileHandle.write(val)
    fileHandle.write('\r\n')
    fileHandle.close()

def write_file(path,val):
    fileHandle=open(path,'w')
    fileHandle.write(val)
    fileHandle.close()
    
def write_log(path,val):
    if os.path.exists(path):
       fileHandle=open(path,'a')
    else:
       fileHandle=open(path,'w') 
    fileHandle.write(str(val))
    fileHandle.write('\r\n')
    fileHandle.close()
    print_console(str(val))
    
def read_file_oneline(filepath):
    try:
        if os.path.exists(filepath):
            fileHandle=open(filepath,'r')
            tmpval=fileHandle.readline().strip()
            tmpval=tmpval.replace(' ', '')
            tmpval=tmpval.replace('\0', '')
            fileHandle.close()
            return tmpval
        else:
            print_console('file '+str(filepath)+ ' is not exist')
            err_deal()
    except Exception as info:
        print_console(str(info))
        err_deal()

def err_deal():
    del_cli_file()
    file_up('flash:',str(sn_val)+'.LOG',tftp_ip, def_upload_log_dir)
    del_cli_file()
    write_file('/data/'+str(sn_val)+'.error','')
    file_up('flash:',str(sn_val)+'.error',tftp_ip, def_upload_status_dir)
    write_file(zam_file,'0')
    clear_file()
    sys.exit()

#only when config.text exists reload-checking needed
def check_reload_flag():
    # you create, you remove
    if os.path.exists(zam_second_run_file):
        os.remove(zam_second_run_file)
        tmp = 'zam_cli.elf \"exec\" \"delete sw1_flash:%s\"' % zam_second_run_file_name
        os.system(tmp)
        tmp = 'zam_cli.elf \"exec\" \"delete sw2_flash:%s\"' % zam_second_run_file_name
        os.system(tmp)
    if os.path.exists('/data/config.text') and os.path.exists(check_reload_file):
        os.remove(check_reload_file)
        tmp = 'zam_cli.elf \"exec\" \"delete sw1_flash:%s\"' % check_reload_file
        os.system(tmp)
        tmp = 'zam_cli.elf \"exec\" \"delete sw2_flash:%s\"' % check_reload_file
        os.system(tmp)
        os.system('sync')
        write_log(log_file, 'will reload device secondly.')
        write_file(zam_file,'1')
        sys.exit()
    #if config.text doesn't exist, remove check_reload_file
    if os.path.exists(check_reload_file):
        os.remove(check_reload_file)

def check_cfg_need_second_reload():
    try:
        if os.path.exists('/data/config.text'):
            # check config.text contain "split interface" or "switch virtual domain" ,and set reload flag
            file_object=open('/data/config.text','r')
            all_text=file_object.read()
            ret = str(all_text).find(str('split interface'))
            ret2 = str(all_text).find(str('switch virtual domain'))
            if ret!=-1 and ret2 != -1:
                write_log(log_file, 'device will reload two times.')
                write_file(zam_second_run_file, '1')
                write_file(check_reload_file, '1')
    except Exception as info:
        return -1

def succ_deal():
    del_cli_file()
    file_up('flash:',str(sn_val)+'.LOG',tftp_ip, def_upload_log_dir)
    del_cli_file()
    write_file('/data/'+str(sn_val)+'.ok','')
    file_up('flash:',str(sn_val)+'.ok',tftp_ip, def_upload_status_dir)
    if os.path.exists('/data/config.text'):
        write_file(zam_file,'1')
    else:
        write_log(log_file, 'config.text is no exitst')
        write_file(zam_file,'0')
    clear_file()
    sys.exit()

def init_def_image_name():
    global def_image_name
    try:
        del_cli_file()
        tmp = 'zam_cli.elf \"exec\" \"show version\"'
        rst = os.system(tmp)
        if rst!=0:
            write_log(log_file, 'exec cmd ' +str(tmp)+' fail')
        else:
            file = open(cli_result_log,'r')
            for line in file:
                line = line.strip()
                if line.startswith('System software version'):
                    def_image_name = str(line.split(':')[1].split(',')[0].replace(" ",""))
                    pos = line.find('Release(')
                    if (pos > 0):
                        release_num = line[pos:].split('(')[1].split(')')[0]
                        def_image_name += '_'
                        def_image_name += release_num
                    def_image_name += "_install.bin"
                    break
            file.close()
            write_log(log_file,'current version image name:'+ str(def_image_name))
    except Exception as info:
        def_image_name = ''
        write_log(log_file, 'initial current version image name' +str(tmp)+' exception')
        write_log(log_file, info)

def get_dev_param():
    global tftp_ip
    global port_type
    
    try:
        del_cli_file()
        tmp = 'zam_cli.elf \"exec\" \"show zam\"'
        rst = os.system(tmp)
        if rst!=0:
            write_log(log_file, 'exec cmd ' +str(tmp)+' fail')
            err_deal()
        else:
            if not os.path.exists(cli_result_log):
                write_log(log_file, 'exec cmd show zam info fail, zam_cli log file is not existed')
                err_deal()
            file_object=open(cli_result_log,'r')
            for line in file_object:
                if line.strip().startswith('Interface name'):
                    port_name= str(line.split(':')[1].strip())
                    if str(port_name) == 'NULL':
                        write_log(log_file, 'get dev param Interface name null')
                        err_deal() 
                if line.strip().startswith('Interface type'):
                    port_type= str(line.split(':')[1].strip())
                if line.strip().startswith('Server ip'):
                    tftp_ip= str(line.split(':')[1].strip())
                    if str(tftp_ip) == 'NULL':
                        write_log(log_file, 'get dev param server ip error')
                        err_deal()
    except Exception as info:
        write_log(log_file, 'get dev param exception')
        write_log(log_file, info)
        err_deal()

def init_params():
    global sn_val
    global tftp_ip
    global log_file
    sn_val=read_file_oneline(str(sn_path))
    log_file=str(log_file_path)+str(sn_val)+'.LOG'
    if os.path.exists(tftp_ip_file):
        tftp_ip=read_file_oneline(str(tftp_ip_file))
    clear_all_file()
    check_self_pid()

def find_keyword(find_str, notuse):
    file_object=open(cli_result_log,'r')
    try:
        all_text=file_object.read()
        write_log(log_file, str(all_text))
        ret = str(all_text).find(str(find_str))
        if ret==-1:
            write_file(zam_file,'0')
            return -1
        else:
            return 0
    except Exception as info:
        write_log(log_file, 'find keyword '+str(find_str)+ ' exception')
        write_log(log_file, info)
        return -1

def file_up(locpath,filename,ip,dstpath):
    if file_upload_forbiden:
        return 0;
    try:
        del_cli_file()
        if  port_type == 'MGMT':
            tmp = 'zam_cli.elf \"exec\" \"copy %s%s oob_tftp://%s%s%s\"' % (locpath, filename, ip, dstpath, filename)
        else:
            tmp = 'zam_cli.elf \"exec\" \"copy %s%s tftp://%s%s%s\"' % (locpath, filename, ip, dstpath, filename)

        rst = os.system(tmp)
        if rst != 0:
            write_log(log_file, 'upload ' +str(tmp)+' fail')
            return -1
        write_log(log_file, 'upload ' +str(tmp)+' succ') 
        return 0
    except Exception as info:
        write_log(log_file, 'upload' +str(tmp)+' exception')
        write_log(log_file, info)
        return -1
        
def file_down(locpath,filename,ip,dstpath):
    try:
        del_cli_file()
        if  port_type == 'MGMT':
            tmp = 'zam_cli.elf \"exec\" \"copy oob_tftp://%s%s%s %s%s\"' % (ip, dstpath, filename, locpath, filename)
        else:
            tmp = 'zam_cli.elf \"exec\" \"copy tftp://%s%s%s %s%s\"' % (ip, dstpath, filename, locpath, filename)

        rst = os.system(tmp)
        if rst != 0:
            write_log(log_file, 'download ' +str(tmp)+' fail')
            return -1
        write_log(log_file, 'download ' +str(tmp)+' succ')
        return 0
    except Exception as info:
        write_log(log_file, 'download ' +str(tmp)+' exception')
        write_log(log_file, str(info))
        return -1

def upload_sn_poap():
    if file_upload_forbiden:
        return 0;
    del_cli_file();
    write_file('/data/'+str(sn_val)+ def_startup_suffix,'')
    ret=file_up('flash:',str(sn_val)+ def_startup_suffix,tftp_ip, def_upload_startup_dir)
    if ret != 0:
        write_log(log_file, 'upload ' +str(sn_val)+ def_startup_suffix + ' fail') 
        clear_file()
        write_file(zam_file,'0')
        sys.exit()
    ret=find_keyword('success', 100)
    if ret!=0:
        write_log(log_file, 'upload sn param find key [success] fail')
        clear_file()
        write_file(zam_file,'0')
        sys.exit()

def download_sn_params():
    retry_num=1
    if no_params_file:
        return 0
    while (retry_num <= 3):
        ret=file_down('flash:',str(sn_val)+ def_params_suffix,tftp_ip, def_download_cfg_dir)
        if ret!= 0:
            write_log(log_file, 'exec file down '+str(sn_val)+ def_params_suffix +' cmd fail')
        ret=os.path.exists('/data/'+str(sn_val)+ def_params_suffix)
        if ret==0:
             retry_num=retry_num+1
             write_log(log_file, 'file down'+str(sn_val)+ def_params_suffix +' fail, retry='+str(retry_num))
        else:
            break
    if retry_num>3:
        err_deal()
    write_log(log_file, 'download sn params' +str(sn_val)+'.param succ'); 
    
def parse_sn_params():
    global image_name
    params = '/data/'+str(sn_val)+ def_params_suffix

    if no_params_file:
        return 0
    try:
        paramsfile = open(params,'r')
        for line in paramsfile:
            if line.startswith('image='):
                image_name = str(line.split('=')[1].strip())
        paramsfile.close()
        write_log(log_file,'parse image_name='+ str(image_name))
        write_log(log_file,'parse params succ')
        
    except Exception as info:
        write_log(log_file, 'parse sn params file exception')
        write_log(log_file, info)
        err_deal()
        
def down_cfg():
    del_cli_file()
    if os.path.exists('/data/'+str(sn_val)+ def_cfg_suffix):
        os.remove('/data/'+str(sn_val)+ def_cfg_suffix)
    ret=file_down('flash:',str(sn_val)+ def_cfg_suffix,tftp_ip, def_download_cfg_dir)
    if ret!=0:
        write_log(log_file,'exec download cmd '+str(sn_val)+ def_cfg_suffix+' fail')
        err_deal()
        
    ret=find_keyword('success', 100)
    if ret!=0:
        write_log(log_file, 'download '+str(sn_val)+ def_cfg_suffix+' fail')
        err_deal()
    
    if support_vsu_dat==1:
        del_cli_file()
        if os.path.exists('/data/'+str(sn_val)+'.VSU'):
            os.remove('/data/'+str(sn_val)+'.VSU')
        ret=file_down('flash:',str(sn_val)+'.VSU',tftp_ip, def_download_cfg_dir)
        if ret!=0:
            write_log(log_file,'exec download cmd '+str(sn_val)+'.VSU fail')
            err_deal()

        ret=find_keyword('success', 500)
        if ret!=0:
            write_log(log_file, 'download '+str(sn_val)+ def_cfg_suffix+' fail')
            err_deal()

    if support_upgrade==1:
        if len(image_name) > 0:
            if image_name == def_image_name:
                write_log(log_file, str(image_name)+' is same as current version')
                return 0
            del_cli_file()
            if os.path.exists('/tmp/vsd/0/'+str(image_name)):
                write_log(log_file,'download '+str(image_name)+' is existed')
                return 0
            ret=file_down('tmp:',image_name,tftp_ip, def_download_image_dir)
            if ret!=0:
                write_log(log_file,'download '+str(image_name)+' fail')
                err_deal()
                
            ret=find_keyword('success', 500)
            if ret!=0:
                write_log(log_file, 'download '+str(image_name)+' fail')
                err_deal()
        
def check_cfg():
    #check cfg file 
    ret=os.path.exists('/data/'+str(sn_val)+ def_cfg_suffix)
    if ret<=0:
        write_log(log_file,'cfg file is not exist')
        err_deal()
    ret=os.path.getsize('/data/'+str(sn_val)+ def_cfg_suffix)
    if ret<=0:
        write_log(log_file,'cfg file size <= 0')
        err_deal()

    #check vsu config
    if support_vsu_dat==1:
        ret=os.path.exists('/data/'+str(sn_val)+'.VSU')
        if ret<=0:
            write_log(log_file,'cfg file is not exist')
            err_deal()
        ret=os.path.getsize('/data/'+str(sn_val)+'.VSU')
        if ret<=0:
            write_log(log_file,'cfg file size <= 0')
            err_deal()
    
    #check image file
    if support_upgrade==1:
        if len(image_name)>0 and os.path.exists('/tmp/vsd/0/'+str(image_name)):
            ret=os.path.getsize('/tmp/vsd/0/'+str(image_name))
            if (ret<=0):
                write_log(log_file,'image file size <= 0')
                err_deal()

def upgrade_bin():
    if support_upgrade != 1:
        return 0
    if len(image_name)>0 and image_name != def_image_name:
        try:
            del_cli_file()
            tmp = 'zam_cli.elf \"exec\" \"upgrade tmp:%s \"' % (image_name)
            rst = os.system(tmp)
            if rst!=0:
                write_log(log_file, 'exec upgrade cmd ' +str(tmp)+' fail')
                err_deal() 
            else:
                write_log(log_file, 'exec upgrade cmd ' +str(tmp)+' succ')
                ret=find_keyword('success', 1000)
                if ret!=0:
                   write_log(log_file, 'upgrade find keyword [success] fail')
                   err_deal()

        except Exception as info:
            write_log(log_file, 'exec cmd ' +str(tmp)+' exception')
            write_log(log_file, info)
            err_deal()
            
def rename_cfg():
    try:
        del_cli_file()
        tmp = 'cd /data \n mv '+str(sn_val)+ def_cfg_suffix+' config.text'
        rst = os.system(str(tmp))
        if rst != 0:
           write_log(log_file, 'exec cmd ' +str(tmp)+' fail')
           err_deal()
        else:
            write_log(log_file, 'exec cmd ' +str(tmp)+' success')
        
        if support_vsu_dat==1:
            if os.path.exists('/data/'+str(sn_val)+'.VSU'):
                tmp = 'mv /data/' + str(sn_val) + '.VSU' + ' /data/config_vsu.dat'
                rst = os.system(str(tmp))
                if rst != 0:
                    write_log(log_file, 'exec cmd ' +str(tmp)+' fail')
                    err_deal()
                else:
                    write_log(log_file, 'exec cmd ' +str(tmp)+' success')

    except Exception as info:
        write_log(log_file, 'rename config file exception')
        write_log(log_file, info)
        err_deal()
    
if __name__ == '__main__':
    init_params()
    check_reload_flag()
    get_dev_param()
# get current version name
    #init_def_image_name()
    upload_sn_poap()
    download_sn_params()
    parse_sn_params()
    down_cfg()
    check_cfg()
    upgrade_bin()
    rename_cfg()
    check_cfg_need_second_reload()
    succ_deal()
