#!/bin/bash
# Weak Lensing Data Download Script
# Run this script after obtaining necessary credentials

echo "Weak Lensing Data Download Script"
echo "================================="

# Create directories
mkdir -p real_weak_lensing_data/{DES,KiDS,HSC,CFHTLenS}

# KiDS Download (Public Access)
echo "Downloading KiDS-1000 data..."
cd real_weak_lensing_data/KiDS

# Download KiDS catalogs (replace with actual URLs)
# wget http://kids.strw.leidenuniv.nl/DR4/KiDS-1000_shear_catalog.fits
# wget http://kids.strw.leidenuniv.nl/DR4/KiDS-1000_photoz_catalog.fits
# wget http://kids.strw.leidenuniv.nl/DR4/KiDS-1000_masks.fits

echo "KiDS download complete (if URLs were valid)"

# DES Download (Requires Authentication)
echo "\nFor DES data:"
echo "1. Login to https://des.ncsa.illinois.edu/"
echo "2. Get your authentication token"
echo "3. Use: wget --auth-no-challenge --user=YOUR_USER --password=YOUR_PASS URL"

# HSC Download (Requires Registration)
echo "\nFor HSC data:"
echo "1. Register at https://hsc-release.mtk.nao.ac.jp/"
echo "2. Use their download interface or API"

cd ../..
echo "\nDownload script complete. Check individual survey sites for actual data."
