#!/bin/bash
mysql() {
            port=($(netstat -tpln | awk -F "[ :]+" '/[m]ysql/' | awk '{print $4}'|awk -F: '{print $2}'))
            printf '{\n'
            printf '\t"data":[\n'
               for key in ${!port[@]}
                   do
                       if [[ "${#port[@]}" -gt 1 && "${key}" -ne "$((${#port[@]}-1))" ]];then
              socket=`ps aux|grep ${port[${key}]}|grep -v grep|awk -F '=' '{print $10}'|cut -d ' ' -f 1`
                          printf '\t {\n'
                          printf "\t\t\t\"{#MYSQLPORT}\":\"${port[${key}]}\"},\n"
                     else [[ "${key}" -eq "((${#port[@]}-1))" ]]
              socket=`ps aux|grep ${port[${key}]}|grep -v grep|awk -F '=' '{print $10}'|cut -d ' ' -f 1`
                          printf '\t {\n'
                          printf "\t\t\t\"{#MYSQLPORT}\":\"${port[${key}]}\"}\n"
                       fi
               done
                          printf '\t ]\n'
                          printf '}\n'
}
$1
