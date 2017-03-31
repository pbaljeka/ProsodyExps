import sys

def get_line(textgrid, item_num):
    with open(textgrid, 'r') as tg:
        for line_num, line in enumerate(tg):
            line_items=line.strip().split()
            if len(line_items) >1 and line_items[0]=="item" and line_items[1] == "["+str(item_num)+ "]:":
                print line_num, line
                break
    return line_num

def get_phrase(textgrid, word_file, item_num):
    tg=open(textgrid, 'r')
    numbers=[]
    line_num=get_line(textgrid, item_num)
    tg_lines=tg.readlines()
    tg_pron=tg_lines[int(line_num):]
    for line in tg_pron:
        line_items=line.strip().split()
        if len(line_items) >1 and line_items[0]=="xmax":
            numbers.append(float(line_items[2]))
    tg.close()
    pron_number=0
    prev_time=0.0
    with open(syl_file, 'r') as sf:
        for line in sf:
            line_items= line.strip().split()
            #print prev_time, line_items[1], pron_number

            if prev_time < numbers[int(pron_number)] and float(line_items[1]) >= numbers[int(pron_number)]:
                line_items.append(int(1))
                pron_number=min(len(numbers)-1,pron_number+1)
            else:
                line_items.append(int(0))
            #line_items.append(float(numbers[int(pron_number)]))
            prev_time=float(line_items[1])
            new_line=' '.join([str(item) for item in line_items])
            print new_line

def get_point_feats(textgrid, syl_file, item_num=3):
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
    print numbers
    prev_time=0.0
    pron_number=numbers[0]
    with open(syl_file, 'r') as sf:
        for line in sf:
            line_items= line.strip().split()
            if prev_time < pron_number and pron_number<= float(line_items[1]):
                print prev_time, pron_number, line_items[1], 1
                line_items.append(int(1))
            else:
                print prev_time, pron_number, line_items[1], 0
                line_items.append(int(0))
            prev_time=float(line_items[1])
            new_line=' '.join([str(item) for item in line_items])
            if prev_time < numbers[-1]:
                pron_number= [pn for pn in numbers if pn>prev_time][0]
            else:
                pron_number = numbers[-1]
            #print new_line

if __name__ =="__main__":
    tg_file=sys.argv[1]
    syl_file=sys.argv[2]
    get_point_feats(tg_file, syl_file, 6)
    get_point_feats(tg_file, syl_file, 3)
    get_point_feats(tg_file, syl_file, 4)
