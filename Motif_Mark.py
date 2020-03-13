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


amg_motif_dict = {'y':('c','t'),
                  'Y':('C', 'T')}

def parse_ambig_motif(list):
    adj_ambig_list=[]
    #adj_ambig_list.append(list)
    for motif in list:
        if 'y' in motif:
            for replace_y in amg_motif_dict['y']:
                #print(replace_y)
                replacement_y = motif.replace('y', replace_y)
                #print(replacement_y)
                list.append(replacement_y)
                #print(adj_ambig_list)
        if 'Y' in motif:
            for replace_Y in amg_motif_dict['Y']:
                replacement_Y = motif.replace('Y', replace_Y)
                #print(replacement_Y)
                list.append(replacement_Y)
                #print(adj_ambig_list)

    return(list)


m_list = parse_motif_file(m)
print(m_list)

parse_motif_file(m)

surface = cairo.SVGSurface("motif_plot.svg", 1000, 500)
context = cairo.Context(surface)
context.set_line_width(20)
context.move_to(50,25)
context.line_to(100,25)
context.set_source_rgb(1, 0, 0)
context.show_text(m_list[0])
context.stroke()
context = cairo.Context(surface)
context.set_line_width(20)
context.move_to(50,50)
context.line_to(100,50)
context.set_source_rgb(.32, .60, 0.1)
context.show_text(m_list[1])
context.stroke()
context = cairo.Context(surface)
context.set_line_width(20)
context.move_to(50,75)
context.line_to(100,75)
context.set_source_rgb(.5, .2, .1)
context.show_text(m_list[3])
context.stroke()
context = cairo.Context(surface)
context.set_line_width(20)
context.move_to(50,100)
context.line_to(100,100)
context.set_source_rgb(.2,.5,.6)
context.show_text(m_list[2])
context.stroke()

with open(f, "rt") as file_handle:
        header_list = []
        header_pos = 150
        seq_y_coord = 175
        exon_y_coord = 170
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
                context.move_to(50, seq_y_coord)
                context.line_to(seq_length, seq_y_coord)
                context.stroke()
                seq_y_coord += 75
                #draw vertical line when motif is found
                if re.search('[A-Z]', line):
                    #find the location (span) of the capitilized exon, using regex
                    exon = re.search('[A-Z]+', line).span()
                    x = re.findall('[A-Z]+', line)
                    print(x)
                    print(exon)
                    exon_start = exon[0]
                    exon_end = (exon[1])
                    context.set_line_width(3)
                    context.set_source_rgb(0,0,0)
                    context.rectangle(exon_start,exon_y_coord,exon_end - exon_start,10)
                    context.stroke()
                    exon_y_coord += 75


        for header in header_list:
        #print(header)
            context.set_source_rgb(0, 0, 0)
            context.move_to(50, header_pos)
            context.show_text(header)
            #context.stroke()
            header_pos += 75



    #print(header_list)

#parse_ambig_motif(m_list)

surface.finish()
