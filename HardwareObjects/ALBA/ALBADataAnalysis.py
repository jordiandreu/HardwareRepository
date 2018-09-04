
import os
import time
import logging

import sys
sys.path.append("/beamlines/bl13/controls/devel/pycharm/ALBAClusterClient")

from PyTango import DeviceProxy

from DataAnalysis import DataAnalysis
from HardwareRepository.TaskUtils import *

from XSDataMXCuBEv1_3 import XSDataResultMXCuBE

root = os.environ['POST_PROCESSING_SCRIPTS_ROOT']

sls_script = os.path.join(root, 'edna-mx/strategy/edna-mx.strategy.sl')

from xaloc import XalocJob

class ALBADataAnalysis(DataAnalysis):

    def init(self):
        DataAnalysis.init(self)

    # used for strategy calculation (characterization) using data analysis cluster
    def run_edna(self, input_file, results_file, edna_directory):
        return self.run(input_file, results_file, edna_directory)

    def run(self, *args):
        input_file, results_file, edna_directory = args

        jobname = os.path.basename(os.path.dirname(edna_directory))

        logging.getLogger("HWR").debug("  XalocJob submiting ")
        logging.getLogger("HWR").debug("      job_name: %s" % jobname)
        logging.getLogger("HWR").debug("      sls_script: %s, " % sls_script)
        logging.getLogger("HWR").debug("      input file: %s" % input_file)
        logging.getLogger("HWR").debug("      results file: %s" % results_file)
        logging.getLogger("HWR").debug("      edna directory: %s" % edna_directory)


        self.job = XalocJob("edna-strategy", jobname, sls_script, input_file, edna_directory)
        self.job.submit()

        logging.getLogger("HWR").debug("  XalocJob submitted %s" % self.job.id)

        self.edna_directory = os.path.dirname(input_file)
        self.input_file = os.path.basename(input_file)
        self.results_file = self.fix_path(results_file)
        logging.getLogger("HWR").debug("      self.results file: %s" % self.results_file)

        state = self.wait_done()

        if state == "COMPLETED": 
            logging.getLogger("HWR").debug("EDNA Job completed") 
            time.sleep(0.5) 
            result = self.get_result()
        else:
            logging.getLogger("HWR").debug("EDNA Job finished without success / state was %s" % (self.job.state))
            result = ""
        
        return result

    def fix_path(self, path):
        outpath = path.replace('PROCESS_DATA', 'PROCESS_DATA/RESULTS')
        #dirname = os.path.dirname(path)
        #basename = os.path.basename(path)
        #outpath = os.path.join(dirname,'RESULTS',basename)
        return outpath

    def wait_done(self):


        logging.getLogger("HWR").debug("Polling for Job state") 
        time.sleep(0.5) 
        logging.getLogger("HWR").debug("Polling for Job state 2") 

        try:
            state = self.job.state
            logging.getLogger("HWR").debug("Job / is %s" % str(state))
        except:
            import traceback
            logging.getLogger("HWR").debug("Polling for Job state 3. exception happened") 
            logging.getLogger("HWR").debug("  %s " % traceback.format_exc())
 
        while state in ["RUNNING", "PENDING"]:
            logging.getLogger("HWR").debug("Job / is %s" % state)
            time.sleep(0.5) 
            state = self.job.state

        logging.getLogger("HWR").debug("Returning") 
        logging.getLogger("HWR").debug("Returning %s" % str(state)) 
        return state

    def get_result(self):

        jobstatus = self.job.status

        #outname = self.input_file.replace("Input", "Output")
        #outfile = os.path.join( self.edna_directory, outname)

        logging.getLogger("HWR").debug("Job / state is COMPLETED")
        logging.getLogger("HWR").debug("  job status dump: %s" % jobstatus)
        logging.getLogger("HWR").debug("  looking for file: %s" % self.results_file)

        if os.path.exists(self.results_file):
            #job_output = open(outfile).read()
            #logging.getLogger("HWR").debug("     EDNA results file found. loading it")
            #open(self.results_file, "w").write(job_output)
            logging.getLogger("HWR").debug("     EDNA results file found 2")
            result = XSDataResultMXCuBE.parseFile(self.results_file)
            logging.getLogger("HWR").debug("     EDNA results file found 3")
            logging.getLogger("HWR").debug("EDNA Result loaded from file / result is=%s" % str(type(result))) 
        else:
            logging.getLogger("HWR").debug("EDNA Job finished without success / cannot find output file ") 
            result = ""

        return result

def test_hwo(hwo):
    ofile = "/tmp/edna/edna_result"
    odir = "/tmp/edna"
    test_input_file = "/beamlines/bl13/projects/cycle2018-I/2018012551-bcalisto/mx2018012551/DATA/20180131/PROCESS_DATA/characterisation_ref-Thrombin-TB-TTI1_A_run1_1/EDNAInput_2004391.xml"
    result = hwo.run_edna(test_input_file,ofile,odir) 
    print result

