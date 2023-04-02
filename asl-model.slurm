#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=64G
#SBATCH --time=06:00:00
#SBATCH --partition=gpu
#SBATCH --gpus-per-node=1

module load python/anaconda3-2019.10-tensorflowgpu

source activate asl

pip install -U matplotlib
pip install -U scikit-image
pip install -q kaggle
pip install tensorflow==2.9.1

# Create new directory
mkdir -p ~/enel645_final/asl_alphabet/
mkdir -p ~/output_images/

# Download dataset from kaggle
KAGGLE_USERNAME=tysontrail \
  KAGGLE_KEY=29decad2f17556a9de6abf9e5b93dc21 \
  kaggle datasets download -d grassknoted/asl-alphabet
# Unzip and save in newly created directory
unzip -q asl-alphabet.zip -d asl_alphabet/

python ~/enel645_final/asl_classification.py
