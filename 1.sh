#!/bin/bash 


shopt -s extglob
#input='hostname~web:sit'
input=$(cat  /tmp/response_git_msg.txt)

# echo "${input//@(*~|:*)/}"
#echo "${input//@(*`|`*)/}"


s='<some text> from=someuser@somedomain.com, <some text>'
#grep -oP '(?<=from=).*?(?=,)' <<< "$s"


sed 's/.*```\(.*\)```.*/\1/' <<< "$input"
