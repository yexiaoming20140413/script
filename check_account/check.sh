#!/bin/bash - 
#===============================================================================
#
#          FILE:  check.sh
# 
#         USAGE:  ./check.sh 
# 
#   DESCRIPTION:  检测交易流水
# 
#       OPTIONS:  ---
#  REQUIREMENTS:  ---
#          BUGS:  ---
#         NOTES:  ---
#        AUTHOR: YOUR NAME (), 
#       COMPANY: 
#       CREATED: 2016年02月20日 11时53分17秒 CST
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
cd  /home/script/check_account/ && /usr/local/bin/python app.py
