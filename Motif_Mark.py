#!/usr/bin/env python
# coding: utf-8

# In[172]:


import argparse
import cairo
import re

#fasta_file = "/Users/GioiTran/Documents/shell/Bi624/Motif_Mark/new_Figure_1.fasta"
#motif_file = "/Users/GioiTran/Documents/shell/Bi624/Motif_Mark/Fig_1_motifs.txt"


def get_arguements():
    #```This function handles all argparse agruements i.e, input sequence file (fasta) and ambiguous motif file```
    parser = argparse.ArgumentParser(description="specifies input fasta file and input ambiguous motif file")
    parser.add_argument("-f", "--fasta_file", help="this argument specifies the input fasta file", type =str, required=True)
    parser.add_argument("-m", "--motif_file", help="this argument specifies the input ambiguous motif file", type =str, required=True)
    return parser.parse_args()

args=get_arguements()
f=args.fasta_file
m=args.motif_file



def parse_motif_file(file):
#parse through the motif file, append motifs into a list, account for ambiguous motif, return motif count?
    motif_list = []
    ambig_replacements = ["t","c"]
    with open(file, "rt") as fh:
        for line in fh:
            motif_list.append(line.strip())
        return(motif_list)




def amb_motif( line):
    motif_pos_dict = {}
    y_rgx = re.compile('[cut]gc[cut]', flags=re.IGNORECASE)
    Y10_rgx = re.compile('[CUT]{10}', flags=re.IGNORECASE)
    GCAUG_rgx = re.compile(r'gca[ut]g', flags=re.IGNORECASE)
    catag_rgx = re.compile('catag', flags=re.IGNORECASE)


    for y in y_rgx.finditer(line):
        #print(y.start(), y.end(), y.group())
        y_start_pos = y.start()
        y_end_pos = y.end()
        y_motif_key = y.group()
        motif_pos_dict[(y_start_pos, y_end_pos)] = y_motif_key

    for Y10 in Y10_rgx.finditer(line):
       # print(Y10.start(), Y10.end(), Y10.group())
        Y10_start_pos = Y10.start()
        Y10_end_pos = Y10.end()
        Y10_motif_key = Y10.group()
        motif_pos_dict[(Y10_start_pos, Y10_end_pos)] = Y10_motif_key

    for GCAUG in GCAUG_rgx.finditer(line):
       # print(GCAUG.start(), GCAUG.end(), GCAUG.group())
        GCAUG_start_pos = GCAUG.start()
        GCAUG_end_pos = GCAUG.end()
        GCAUG_motif_key = GCAUG.group()
        motif_pos_dict[(GCAUG_start_pos, GCAUG_end_pos)] = GCAUG_motif_key

    for catag in catag_rgx.finditer(line):
        #print(catag.start(), catag.end(), catag.group())
        catag_start_pos = catag.start()
        catag_end_pos = catag.end()
        catag_motif_key = catag.group()
        motif_pos_dict[(catag_start_pos, catag_end_pos)] = catag_motif_key
    return(motif_pos_dict)


m_list = parse_motif_file(m)


parse_motif_file(m)

surface = cairo.SVGSurface("motif_plot.svg", 800, 500)
context = cairo.Context(surface)
context.move_to(50, 10)
context.show_text("Motif Legend:")
context.set_line_width(20)
context.set_source_rgb(1, .1, .1)
context.move_to(50,25)
context.line_to(100,25)
context.show_text(m_list[0])
context.stroke()
context = cairo.Context(surface)
context.set_line_width(20)
context.set_source_rgb(.32, .60, 0.1)
context.move_to(50,50)
context.line_to(100,50)
context.show_text(m_list[1])
context.stroke()
context = cairo.Context(surface)
context.set_line_width(20)
context.set_source_rgb(0, .51, 3)
context.move_to(50,75)
context.line_to(100,75)
context.show_text(m_list[3])
context.stroke()
context = cairo.Context(surface)
context.set_source_rgb(50,0,221)
context.set_line_width(20)
context.move_to(50,100)
context.line_to(100,100)
context.show_text(m_list[2])
context.stroke()


with open(f, "rt") as file_handle:
    header_list = []
    header_pos = 150
    seq_y_coord = 175
    exon_y_coord = 170
    motif_y_coord = 170
    i = 0
        #get ambig motif list

    for line in file_handle:
        i +=1
            #remove skipped line
        line = line.rstrip()
        #store headers into list
        if ">" in line:
            header_list.append(line)
        if i % 2 == 0 :
                #print(line)
            seq_length = len(line)
            context.set_line_width(3)
            context.set_source_rgb(0, 0, 0)
            context.move_to(5, seq_y_coord)
            context.line_to(seq_length, seq_y_coord)
            context.stroke()
            seq_y_coord += 75
                #draw empty box when exon is found
            if re.search('[A-Z]', line):
                    #find the location (span) of the capitilized exon
                exon = re.search('[A-Z]+', line).span()
                    #x = re.findall('[A-Z]+', line)
                    #print(x)
                    #print(exon)
                exon_start = exon[0]
                exon_end = (exon[1])
                context.set_line_width(3)
                context.set_source_rgb(0,0,0)
                context.rectangle(exon_start +5,exon_y_coord,exon_end - exon_start,10)
                context.stroke()
                exon_y_coord += 75

                    #call ambig parsing function, get dict of motif positions
                    #keys = motif start & end position
                    #values = specifies motif sequence
                motif_pos_dict = amb_motif(line)
                #print(motif_pos_dict)

                    #loop through the values of dictionary to find each motif using re.search, ignore case sensitivity
                for key, value in motif_pos_dict.items():
                    motif_start = key[0]
                    motif_end = key[0]

                        #draw ygcy ticks
                    if re.search('[cut]gc[cut]', value, re.IGNORECASE):
                        context.set_line_width(3)
                        context.set_source_rgb(1, .1, .1)
                        context.rectangle(motif_start +5,motif_y_coord,motif_end - motif_start,10)
                        context.stroke()

                        #draw YYYYYYYYYY ticks
                    if re.search('[CUT]{10}', value, flags=re.IGNORECASE):
                        context.set_line_width(3)
                        context.set_source_rgb(0, .51, 3)
                        context.rectangle(motif_start +5,motif_y_coord,motif_end - motif_start,10)
                        context.stroke()

                        #draw GCAUG ticks
                    if re.search('gca[ut]g', value, flags=re.IGNORECASE):
                        context.set_line_width(3)
                        context.set_source_rgb(.32, .60, 0.1)
                        context.rectangle(motif_start +5,motif_y_coord,motif_end - motif_start,10)
                        context.stroke()

                        #draw catag ticks
                    if re.search('catag', value, flags=re.IGNORECASE):
                        context.set_line_width(3)
                        context.set_source_rgb(50,0,221)
                        context.rectangle(motif_start +5,motif_y_coord,motif_end - motif_start,10)
                        context.stroke()


                motif_y_coord += 75

    for header in header_list:
        #print(header)
        context.set_source_rgb(0, 0, 0)
        context.move_to(5, header_pos)
        context.show_text(header)
            #context.stroke()
        header_pos += 75


surface.finish()
