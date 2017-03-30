# 
#user;db
#ct1tst800;ct1tst800
#ct2tst800;ct2tst800
#ct5tst800;ct5tst800

#ct3tst;ct3tst800
#ct4dev;ct4dev800
#ct6tst;ct6tst800
#ct4tst;ct4tst800
#
for j in ct1tst ct2tst ct3tst ct4tst ct5tst ct6tst ct4dev
do
	export PGPASSWORD=${j}800
	database=${PGPASSWORD}
	echo ${PGPASSWORD}
	#
	#if [ ${j} =~ "ct1"  ] || [ ${j} =~ "ct2" ] || [ ${j} =~ "ct5" ] ;  then   
	echo "====================================="
	echo ${j}
	if [[ $j =~ [1-2,5] ]]; then
 		user=${j}800
	else
		user=$j
	fi	
	echo "====================================="
	echo " user set to : ${user}"

	echo "psql -U ${j} -h mucctlwtv01 -p 5432 -d ${database} -c \"select datname from pg_database where datname like '${j}%'\""
	x=`psql -U ${user} -h mucctlwtv01 -p 5432 -d ${database} -c "select datname from pg_database where datname like '${j}%'" | grep ${database}_1`
	#
	for i in ${x}
	do
	  echo "psql -U ${user} -h mucctlwtv01 -p 5432 -d ${database} -c /"drop database $i/"" 
	  psql -U ${user} -h mucctlwtv01 -p 5432 -d ${database} -c "drop database $i"
	done
done
