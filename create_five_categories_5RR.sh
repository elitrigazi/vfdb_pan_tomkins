#!/bin/bash

#segments_5RR_5_classes.arff
cp vfdb-qrs/segments_5RR.arff vfdb-qrs/segments_5RR_5_classes.arff
sed -i 's/(//g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i 's/\r//g' vfdb-qrs/segments_5RR_5_classes.arff
sed -e 's/,HGEA$/,HGEA-N-NOD-PM-SBR-VER/g' vfdb-qrs/segments_5RR_5_classes.arff | grep HGEA-N-NOD-PM-SBR-VER | wc -l
sed -e 's/,N$/,HGEA-N-NOD-PM-SBR-VER/g'    vfdb-qrs/segments_5RR_5_classes.arff | grep HGEA-N-NOD-PM-SBR-VER | wc -l
sed -e 's/,NOD$/,HGEA-N-NOD-PM-SBR-VER/g'  vfdb-qrs/segments_5RR_5_classes.arff | grep HGEA-N-NOD-PM-SBR-VER | wc -l
sed -e 's/,PM$/,HGEA-N-NOD-PM-SBR-VER/g'   vfdb-qrs/segments_5RR_5_classes.arff | grep HGEA-N-NOD-PM-SBR-VER | wc -l
sed -e 's/,SBR$/,HGEA-N-NOD-PM-SBR-VER/g'  vfdb-qrs/segments_5RR_5_classes.arff | grep HGEA-N-NOD-PM-SBR-VER | wc -l
sed -e 's/,VER$/,HGEA-N-NOD-PM-SBR-VER/g'  vfdb-qrs/segments_5RR_5_classes.arff | grep HGEA-N-NOD-PM-SBR-VER | wc -l

sed -i -e 's/,ASYS$/,B-VT-VF-VFL-ASYS/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,B$/,B-VT-VF-VFL-ASYS/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,VT$/,B-VT-VF-VFL-ASYS/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,VF$/,B-VT-VF-VFL-ASYS/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,VFL$/,B-VT-VF-VFL-ASYS/g' vfdb-qrs/segments_5RR_5_classes.arff

sed -i -e 's/,HGEA$/,HGEA-N-NOD-PM-SBR-VER/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,N$/,HGEA-N-NOD-PM-SBR-VER/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,NOD$/,HGEA-N-NOD-PM-SBR-VER/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,PM$/,HGEA-N-NOD-PM-SBR-VER/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,SBR$/,HGEA-N-NOD-PM-SBR-VER/g' vfdb-qrs/segments_5RR_5_classes.arff
sed -i -e 's/,VER$/,HGEA-N-NOD-PM-SBR-VER/g' vfdb-qrs/segments_5RR_5_classes.arff

ASYS=$(grep ",ASYS$" vfdb-qrs/segments.arff | wc -l)
B=$(grep ",B$" vfdb-qrs/segments.arff | wc -l)
VT=$(grep ",VT$" vfdb-qrs/segments.arff | wc -l)
VF=$(grep ",VF$" vfdb-qrs/segments.arff | wc -l)
VFL=$(grep ",VFL$" vfdb-qrs/segments.arff | wc -l)

echo "---"
res=$(($ASYS + $B + $VT + $VF + $VFL))
echo $res
grep ",B-VT-VF-VFL-ASYS$" vfdb-qrs/segments_5RR_5_classes.arff  | wc -l
echo "---"


HGEA=$(grep ",HGEA$" vfdb-qrs/segments.arff | wc -l)
N=$(grep ",N$" vfdb-qrs/segments.arff | wc -l)
NOD=$(grep ",NOD$" vfdb-qrs/segments.arff | wc -l)
PM=$(grep ",PM$" vfdb-qrs/segments.arff | wc -l)
SBR=$(grep ",SBR$" vfdb-qrs/segments.arff | wc -l)
VER=$(grep ",VER$" vfdb-qrs/segments.arff | wc -l)
echo "---"
echo $HGEA
echo $N
echo $NOD
echo $PM
echo $SBR
echo $VER
echo "---"

res=$(($HGEA + $N + $NOD + $PM + $SBR + $VER))
echo $res
grep ",HGEA-N-NOD-PM-SBR-VER$" vfdb-qrs/segments_5RR_5_classes.arff  | wc -l


