VOICEDIR=$1
SCRIPTDIR=/home2/pbaljeka/Prosody_Exps/scripts
cp ${SCRIPTDIR}/addfeats.scm $VOICEDIR/festvox/
cp ${SCRIPTDIR}/do_clustergen $VOICEDIR/bin/
cp ${SCRIPTDIR}/get_prosody_feats.sh $VOICEDIR/bin/
cp ${SCRIPTDIR}/dump_prosody_feats.py $VOICEDIR/bin/
cp ${SCRIPTDIR}/featnames* $VOICEDIR/festival/clunits/
cp ${SCRIPTDIR}/mcep_prosody.desc $VOICEDIR/festival/clunits/


