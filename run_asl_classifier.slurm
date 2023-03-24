#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
#SBATCH --time=06:00:00
#SBATCH --partition=gpu
#SBATCH --gpus-per-node=1


module load python/anaconda3-2018.12

source activate pytorch-2023
pip install -U scikit-image
pip install -q kaggle
mkdir /enel645_final/.kaggle
echo '{"username":"tysontrail","key":"29decad2f17556a9de6abf9e5b93dc21"}' > ~/.kaggle/kaggle.json #write kaggle API credentials to kaggle.json
chmod 600 ~/.kaggle # Change the permissions of the file
mkdir asl_alphabet # Create new directory
kaggle datasets download -d grassknoted/asl-alphabet # Download dataset from kaggle
unzip -q asl-alphabet.zip -d asl_alphabet/ # Unzip and save in newly created directory


python /enel645_final/asl_classification.py
# python /enel645_final/asl_classification.py --best_model_path /enel645_final/asl_net.pth --images_path /enel645_final/images/ --transfer-learning True

# scp vladyslav.timofyeyev@talc.ucalgary.ca /mnt/c/Users/Vlad Timofyeyev/Desktop

conda deactivate
