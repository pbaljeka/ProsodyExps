#!/bin/bash
#This gets the prominence from ProsodyTagger in the format for Festival for a single file

praat_exe=/home2/pbaljeka/Prosody_Exps/featureAnnotationforPraat/praat-ft-annot
sourcedir=/home2/pbaljeka/Prosody_Exps/modularProsodyTagger
basedir=wav/
outdir=prosody_feats/
mkdir -p $outdir

###Get the filelist
cat etc/txt.done.data|awk '{print $2}' > etc/filelist
for filename in `cat  etc/filelist`;
do
    #Get textgrid from prosody tagger for rawspeech
    for mod in `echo 01 02 03 05b 06b`;
        do
        $praat_exe ${sourcedir}/mod${mod}.praat ${basedir} ${filename}
    done
  
    #Dumpfeats for words
    $ESTDIR/../festival/examples/dumpfeats -relation Segment -feats festival/clunits/featnames_words festival/utts/${filename}.utt |uniq|sed '/0 0/d'>${basedir}/${filename}.word


    #Dumpfeats for syls
    $ESTDIR/../festival/examples/dumpfeats -relation Segment -feats festival/clunits/featnames_syl festival/utts/${filename}.utt |uniq|sed '/0 0/d'>${basedir}/${filename}.syl

    #Dumpfeats for phones
  $ESTDIR/../festival/examples/dumpfeats -relation Segment -feats festival/clunits/featnames_phone ${VOICEDIR}/festival/utts/${filename}.utt |uniq|sed '/0 0/d'>${basedir}/${filename}.phone
done

###Dumpfeats in bracjeted form by reading the relevant portions of the textgrid file
python ./bin/dump_prosody_feats.py etc/filelist wav/ ${outdir}  
#Annotate the syls in the dumpfeats files
./bin/do_clustergen add_word_feats
./bin/do_clustergen add_syl_feats
./bin/do_clustergen add_phone_feats

mv festival/clunits/mcep.desc festival/clunits/mcep_org.desc
mv festival/clunits/mcep_prosody.desc festival/clunits/mcep.desc
./bin/do_clustergen parallel cluster etc/txt.done.data.train
$FESTVOXDIR/src/clustergen/cg_test resynth cgp_prosody >mcd-prosody.out
