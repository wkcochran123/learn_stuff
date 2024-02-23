URL="https://www.littlegolem.net/jsp/info/player_game_list_txt.jsp?plid=${1}&gtid=connect6"
curl -o${1}.tmp "${URL}"


grep FF ${1}.tmp > ${1}.data
rm ${1}.tmp
