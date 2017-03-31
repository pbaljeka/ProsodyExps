#!/bin/bash
#This gets the prominence from ProsodyTagger in the format for Festival for a single file

praat_exe=/home2/pbaljeka/Prosody_Exps/featureAnnotationforPraat/praat-ft-annot
sourcedir=/home2/pbaljeka/Prosody_Exps/modularProsodyTagger
VOICEDIR=$1
basedir=${VOICEDIR}/wav/
outdir=${VOICEDIR}/prosody_feats/
mkdir -p $outdir

###Get the filelist
##cat $VOICEDIR/etc/txt.done.data|awk '{print $2}' >$VOICEDIR/etc/filelist
##
##for filename in `cat $VOICEDIR/etc/filelist`;
##do
##    #Get textgrid from prosody tagger for rawspeech
##    for mod in `echo 01 02 03 05b 06b`;
##        do
##        $praat_exe ${sourcedir}/mod${mod}.praat ${basedir} ${filename}
##    done
##
##    #Dumpfeats for syls
##    $ESTDIR/../festival/examples/dumpfeats -relation Segment -feats ${VOICEDIR}/featnames_syl ${VOICEDIR}/festival/utts/${filename}.utt |uniq|sed '/0 0/d'>${basedir}/${filename}.syl
##
##    #Dumpfeats for phones
##    $ESTDIR/../festival/examples/dumpfeats -relation Segment -feats ${VOICEDIR}/featnames_phone ${VOICEDIR}/festival/utts/${filename}.utt |uniq|sed '/0 0/d'>${basedir}/${filename}.phone
##done
##
###Dumpfeats in bracjeted form by reading the relevant portions of the textgrid file
python dump_prosody_feats.py $VOICEDIR/etc/filelist ${basedir} ${outdir}  
#Annotate the syls in the dumpfeats files
./bin/do_clustergen add_syl_feats
./bin/do_clustergen add_phone_feats

./bin/do_clustergen cluster etc/txt.done.data.train
$FESTVOXDIR/src/clustergen/cg_test resynth cgp_all >mcd-prosody.out
