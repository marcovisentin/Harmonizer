#!/bin/bash
#PBS -l walltime=00:05:00
#PBS -l select=1:ncpus=4:mem=24gb:ngpus=1:gpu_type=RTX6000
  
module load anaconda3/personal
source activate harmonizer
  
# Copy input file to $TMPDIR
# mkdir $TMPDIR/data/
# cp -r $HOME/ProtoPNets/vanilla/datasets/stanford_cars $TMPDIR/data/stanford_cars
# echo("Inputs copied in working directory")
  
# Check gpu status 
nvidia-smi

# Run application. As we have not changed directory, currently location is $TMPDIR
python $HOME/projects/ARvertise/ARvertise_Harmonizer/main.py --harmonize_iterations 10 \
--save_dir "./output" \
--is_single_image True\
--image_path "./my_assets/test_composite_image.png" \
--mask_path "./my_assets/test_composite_mask.png" \
--foreground_prompt "bottle dim" \
--background_prompt "bottle warm" \
--pretrained_diffusion_path "stabilityai/stable-diffusion-2-base" \
--use_edge_map True

