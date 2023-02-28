from nasa.exception import SensorException
from nasa.logger import logging
import pandas as pd

class Nasadata():
    def __init__(self):
        pass
    def export_raw_data_as_dataframe(self, raw_data_dir):
        logging.info(f"Start of reading raw data file")
        columns = ['unit_number','time_in_cycles','set_1','set_2','set_3','sen_1','sen_2','sen_3','sen_4','sen_5','sen_6','sen_7','sen_8','sen_9','sen_10','sen_11','sen_12','sen_13','sen_14','sen_15','sen_16','sen_17','sen_18','sen_19','sen_20','sen_21']
        df = pd.read_csv(raw_data_dir +'/'+ "train_FD001.txt",sep='\s+',header=None,index_col=False, names=columns)
        #columns = ['unit_number','time_in_cycles','set_1','set_2','set-3','sen_1','sen_2','sen_3','sen_4','sen_5','sen_6','sen_7','sen_8','sen_9','sen_10','sen_11','sen_12','sen_13','sen_14','sen_15','sen_16','sen_17','sen_18','sen_19','sen_20','sen_21']
        #df.columns = columns
        
        logging.info(f"End of reading raw data file")
        return df