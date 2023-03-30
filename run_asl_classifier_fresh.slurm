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
pip install tensorflow

#conda install -c conda-forge cudatoolkit=11.8.0
#python3 -m pip install nvidia-cudnn-cu11==8.6.0.163 tensorflow==2.12.*
#CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/:$CUDNN_PATH/lib
# Verify install:
#python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

export KAGGLE_USERNAME=tysontrail
export KAGGLE_KEY=29decad2f17556a9de6abf9e5b93dc21

mkdir -p ~/enel645_final/asl_alphabet/ # Create new directory
mkdir -p ~/output_images/

# uncomment for larger dataset
kaggle datasets download -d grassknoted/asl-alphabet # Download dataset from kaggle
unzip -q asl-alphabet.zip -d asl_alphabet/ # Unzip and save in newly created directory

# uncomment for smaller dataset
# kaggle datasets download -d danrasband/asl-alphabet-test # Download dataset from kaggle
# unzip -q asl-alphabet-test.zip -d asl_alphabet/ # Unzip and save in newly created directory
# rm -r asl_alphabet/asl-alphabet-test # Remove additional unneccessary duplicate library

python ~/enel645_final/asl_classification.py
