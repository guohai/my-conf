#! /usr/bin/env python

# " " this is a little program\
#  written by Hai Guo to backup his blog\
#  http://guoh.org/lifelog/\
#  mail-tool is mailx, you can install it by command\
#  'yum -y install mail'
# " "

import os
import sys
import datetime

def nameGenerator(prefix, postfix):
    filename = prefix + str(datetime.datetime.utcnow().strftime("%Y%m%d%H%MZ")) + postfix
    return filename

def checkFileSize(fileName):
    statinfo = os.stat(fileName)
    return statinfo.st_size

sqlDataName = nameGenerator('wp_guoh_db_', '.sql')
wpAppName = nameGenerator('wp_', '.tar.gz')

# 1. dump the sql data
os.system('mysqldump -h localhost -u wp_guoh_user -p\"MY_PASSWD\" --databases wp_guoh_db > ' + sqlDataName)

# check if data-dump has been performed successfully
sqlFileSize = checkFileSize(sqlDataName)

if sqlFileSize < 1024L * 1024 * 5: # threshold we use to roughly tell if file is okay
# send a mail to me and quit this program
# tell admin to handle this issue and clear unused files by hand
    os.system('mailx -s "WP_Backup_{0} failed. IMPORTANT!" MY_MAIL_BOX'.format(wpAppName[3:-7]))
    sys.exit(0)

# 2. compress the sql data quitely, for debug purpose you can add 'v' option
os.system('tar -zcf {0} {1}'.format(sqlDataName[0:-4] + '.tar.gz', sqlDataName)) #[0:-4] means cutting off '.sql'

# 3. compress the blog program quitely, for debug purpose you can add 'v' option
os.system('tar -zcf {0} {1}'.format(wpAppName, 'guoh.org/'))

# 4. send data to my mail box
os.system('mailx -s "WP_Backup_{0}" -a {1} -a {2} MY_GMAIL@gmail.com'.format(wpAppName[3:-7], wpAppName, sqlDataName[0:-4] + '.tar.gz'))

# 5. clear unused files
os.system('rm {0}'.format(sqlDataName))

