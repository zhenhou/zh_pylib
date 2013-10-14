import ConfigParser
import numpy as np

__all__ = ['ConfigNewdat']

class ConfigNewdat:

    def __init__(self, inifile):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(inifile)
        
        self.has_ndf1 = False
        self.ndf2_done = False
        self.ndf1_lines = [' ']
        self.ndf2_lines = [' ']
        self.num_bands  = [0,0,0,0,0,0]
        
    def get_lmin(self):
        return self.config.getint('newdat', 'lmin')

    def get_lmax(self):
        return self.config.getint('newdat', 'lmax')

    def get_newdat(self):
        newdat_input = self.config.get('newdat', 'newdat_original')
        with open (newdat_input, "r") as ndf:
            self.ndf1_lines = ndf.readlines()
            self.has_ndf1 = True
            self.ndf2_lines = self.ndf1_lines
            self.num_bands = [int(i) for i in self.ndf1_lines[1].split()]

    def get_bp_table(self):
        if (not self.has_ndf1):
            self.get_newdat()
        
        type_list = ['TT','EE','BB','EB','TE','TB']
        nlines = len(self.ndf1_lines)

        bp_table = {}
        itype = 0

        for i in range(0,nlines):
            if any(self.ndf1_lines[i].strip() in s for s in type_list):
                tp_type = self.ndf1_lines[i].strip()
                print "reading " + tp_type

                #num_bands = self.num_bands[type_list.index(tp_type)]
                num_bands = self.num_bands[itype]
                bp_info = np.zeros((num_bands,8))

                for iline in range(0,num_bands):
                    bp_info[iline,0:8] = [float(j) for j in self.ndf1_lines[i+1+iline].split()]

                bp_table[tp_type] = bp_info

                itype += 1

        return bp_table
                
#bp_matrix = 

    def alter_newdat(self):
        ndf_lines[0] = 'windows_tophat/window_'+'\n'
#if ndf_lines[2].strip() != 'BAND_SELECTION\n'
            
