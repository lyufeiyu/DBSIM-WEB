for ((i=1; i<=1; i++))
do
    cd /home/lgh/result/output_data/car_retails;
    mkdir $i;
    cd /home/lgh/DBSim/src;
    # echo -e "\n----------------output_data/property/$i------------------\n";
    python SPN_experiment.py --dataset CARRETAILS --gen_dir output_data/car_retails/$i;
    # echo -e "\n----------------$i------------------\n";
done
