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

        self.has_bp_table = False
        self.bp_table = {}
        
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

        itype = 0

        for i in range(0,nlines):
            if any(self.ndf1_lines[i].strip() in s for s in type_list):
                tp_type = self.ndf1_lines[i].strip()
                print "reading " + tp_type

                num_bands = self.num_bands[type_list.index(tp_type)]
                #num_bands = self.num_bands[itype]
                bp_info = np.zeros((num_bands,8))

                for iline in range(0,num_bands):
                    bp_info[iline,0:8] = [float(j) for j in self.ndf1_lines[i+1+iline].split()]

                self.bp_table[tp_type] = bp_info
                itype += 1
        
        self.has_bp_table = True

    def get_band_range(self, lmin=None, lmax=None):
        if lmin is None: lmin = self.get_lmin()
        if lmax is None: lmax = self.get_lmax()

        if not self.has_bp_table: self.get_bp_table()

        band_range = np.zeros(num_bands,2)
        #for i in range

    def create_tophat_windows(self):
        if not self.has_bp_table: self.get_bp_table()
        
        lmin = 2
        lmax = lmin

        window_order = ['TT','TE','EE','BB']
        type_list = ['TT','EE','BB','EB','TE','TB']

        for s in type_list:
            if self.bp_table.has_key(s):
                lmin = int(min(self.bp_table[s][0:,5].min(), lmin))
                lmax = int(max(self.bp_table[s][0:,6].max(), lmax))
        
        ndf = self.config.get('newdat', 'newdat_original')
        path = ndf[0:ndf.rfind('/')]+'/windows/'
        
        iw = 1 
        for s in type_list:
            if self.bp_table.has_key(s):
                num_bands = self.num_bands[type_list.index(s)]
                for i in range(0,num_bands):
                    with open (path+'window_'+str(iw), "w") as wf:
                        wf_tophat = 1.0/(self.bp_table[s][i,6] - self.bp_table[s][i,5]+1.0)
                        for il in range(lmin, lmax+1):
                            wf_value = [0.0, 0.0, 0.0, 0.0]

                            if il >= int(self.bp_table[s][i,5]) and il <= int(self.bp_table[s][i,6]):
                                wf_value[window_order.index(s)] = wf_tophat*(il+1)/(il+0.5)

                            wf.write("%6d %15.6E %15.6E %15.6E %15.6E\n" % (il, wf_value[0], wf_value[1], wf_value[2], wf_value[3]))
                    iw += 1
                                

    def alter_newdat(self):
        ndf_lines[0] = 'windows_tophat/window_'+'\n'
#if ndf_lines[2].strip() != 'BAND_SELECTION\n'
            
