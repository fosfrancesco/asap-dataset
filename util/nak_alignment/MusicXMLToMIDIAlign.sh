#! /bin/bash

if [ $# -ne 2 ]; then
echo "Error in usage: $./align.sh ref(.xml) align(.mid)"
exit 1
fi

I1=$1
I2=$2

ProgramFolder="./util/nak_alignment/Programs"
RelCurrentFolder="."

$ProgramFolder/midi2pianoroll 0 $RelCurrentFolder/${I2}

$ProgramFolder/MusicXMLToHMM $RelCurrentFolder/${I1}.musicxml $RelCurrentFolder/${I1}_hmm.txt
$ProgramFolder/MusicXMLToFmt3x $RelCurrentFolder/${I1}.musicxml $RelCurrentFolder/${I1}_fmt3x.txt

$ProgramFolder/ScorePerfmMatcher $RelCurrentFolder/${I1}_hmm.txt $RelCurrentFolder/${I2}_spr.txt $RelCurrentFolder/${I2}_pre_match.txt 0.01
$ProgramFolder/ErrorDetection $RelCurrentFolder/${I1}_fmt3x.txt $RelCurrentFolder/${I1}_hmm.txt $RelCurrentFolder/${I2}_pre_match.txt $RelCurrentFolder/${I2}_err_match.txt 0
$ProgramFolder/RealignmentMOHMM $RelCurrentFolder/${I1}_fmt3x.txt $RelCurrentFolder/${I1}_hmm.txt $RelCurrentFolder/${I2}_err_match.txt $RelCurrentFolder/${I2}_realigned_match.txt 0.3

cp $RelCurrentFolder/${I2}_realigned_match.txt $RelCurrentFolder/${I2}_match.txt

rm $RelCurrentFolder/${I2}_realigned_match.txt
rm $RelCurrentFolder/${I2}_err_match.txt
rm $RelCurrentFolder/${I2}_pre_match.txt

rm $RelCurrentFolder/${I2}_spr.txt
rm $RelCurrentFolder/${I1}_fmt3x.txt
rm $RelCurrentFolder/${I1}_hmm.txt
