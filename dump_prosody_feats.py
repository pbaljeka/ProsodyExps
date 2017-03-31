import sys
from operator import itemgetter
import numpy as np

def get_line(textgrid, item_num):
    with open(textgrid, 'r') as tg:
        for line_num, line in enumerate(tg):
            line_items=line.strip().split()
            if len(line_items) >1 and line_items[0]=="item" and line_items[1] == "["+str(item_num)+ "]:":
    #            print line_num, line
                break
    return line_num
def get_interval_feats(textgrid, word_file, item_num, feat_name, outfile):
    tg=open(textgrid, 'r')
    numbers=[]
    start_line_num=get_line(textgrid, item_num)
    end_line_num=get_line(textgrid, item_num + 1)
    tg_lines=tg.readlines()
    tg_pron=tg_lines[int(start_line_num): int(end_line_num)]
    for line in tg_pron:
        line_items=line.strip().split()
        if len(line_items) >1 and line_items[0]=="xmax":
            numbers.append(float(line_items[2]))
    tg.close()
    if len(numbers) == 0:
        numbers.append(0)
    else:
        numbers=numbers[1:]
    print numbers
    wf = open(word_file, 'r')
    wf_lines=wf.readlines()
    wf.close()
    min_indices=[]
    for number in numbers:
        wf21=[abs(float(number)-float(items.strip().split()[1])) for items in wf_lines]
        min_indices.append(min(enumerate(wf21), key=itemgetter(1))[0])
    for line_num in range(len(wf_lines)):
        if line_num in min_indices:
            feat_value=1
        else:
            feat_value=0
        new_line="(" + feat_name + " " + str(feat_value) +")"
        with open(outfile, 'a+') as f:
             f.write(new_line + " ")

def get_point_feats(textgrid, syl_file, item_num, feat_name, outfile):
    tg=open(textgrid, 'r')
    numbers=[]
    start_line_num=get_line(textgrid, item_num)
    if item_num < 6:
        end_line_num=get_line(textgrid, item_num + 1)
    tg_lines=tg.readlines()
    if item_num < 6:
        tg_pron=tg_lines[int(start_line_num): int(end_line_num)]
    else:
        tg_pron=tg_lines[int(start_line_num):]
    for line in tg_pron:
        line_items=line.strip().split()
        if len(line_items) >1 and line_items[0]=="number":
            numbers.append(float(line_items[2]))
    tg.close()
    prev_time=0.0
    if len(numbers) == 0:
        numbers.append(0)
    pron_number=numbers[0]
    with open(syl_file, 'r') as sf:
        for line in sf:
            line_items= line.strip().split()
            if prev_time < pron_number and pron_number<= float(line_items[1]):
                feat_value=1
            else:
                feat_value=0
            prev_time=float(line_items[1])
            new_line="(" + feat_name + " " + str(feat_value) +")"
            if prev_time < numbers[-1]:
                pron_number= [pn for pn in numbers if pn>prev_time][0]
            else:
                pron_number = numbers[-1]
            with open(outfile, 'a+') as f:
                f.write(new_line + " ")

def extract_feats(filelist, indir, outdir):
    with open(filelist, 'r') as f:
        for filename in f:
            print filename
            full_file=indir + filename.strip()
            outfile= outdir + filename.strip()
            get_interval_feats(full_file + '_result.TextGrid', full_file + '.word', 5, "pt_break", outfile+ '.break')
            get_point_feats(full_file + '_result.TextGrid', full_file + '.syl', 6, "pt_prom", outfile+ '.prom')
            get_point_feats(full_file +'_result.TextGrid', full_file + '.phone', 3, "pt_Ipeak", outfile + '.Ipeak')
            get_point_feats(full_file + '_result.TextGrid', full_file + '.phone', 4, "pt_Ivalley", outfile + '.Ivalley')


if __name__ =="__main__":
    filelist=sys.argv[1]
    indir=sys.argv[2]
    outdir=sys.argv[3]
    extract_feats(filelist, indir, outdir)
