import pandas as pd
import numpy as np

A = r'Survey in .xlsx Format'
# put the location of the Deviation Document in the above string
file_location = A

class Deviation():
    def __init__(self,well_name):
        self.well_name = well_name
        self.get_data()
        self.prep_data()

    def __repr__(self):
        return "Devation(well_name = {})".format(self.well_name)

    def get_data(self):
        dev = pd.read_excel(file_location, sheet_name=0, header=1)
        dev_data = dev.iloc[4:, :]
        elev = pd.read_excel(file_location, sheet_name=0, header=1, nrows=3, index_col=0)
        elev = elev.to_dict('index')
        self.data = dev_data
        self.data_elev = elev

    def prep_data(self):
        new_dev = self.data.copy()
        new_elev = self.data_elev.copy()
        new_dev['{} MDss'.format(self.well_name)] = np.array(new_dev[('{} MD'.format(self.well_name))])- new_elev[('DF Ref')]['{} MD'.format(self.well_name)]
        new_dev['{} TVDss'.format(self.well_name)] = np.array(new_dev[('{} TVD'.format(self.well_name))]) - new_elev[('DF Ref')]['{} MD'.format(self.well_name)]
        new_dev['{} WLM'.format(self.well_name)] = np.array(new_dev[('{} MD'.format(self.well_name))]) - (new_elev[('DF Ref')]['{} MD'.format(self.well_name)]-new_elev[('THS')]['{} MD'.format(self.well_name)])
        self.data = new_dev

    def get_unit(self,value,from_unit,to_unit):
        self.prep_data()
        self.data1 = self.data.copy()
        self.value = value
        self.from_unit = from_unit
        self.to_unit = to_unit

        if (value < min(self.data1['{} {}'.format(self.well_name,self.from_unit)].to_list())):
            print('Value given is less than minimum data set')

        elif ((value > min(self.data1['{} {}'.format(self.well_name,self.from_unit)].to_list())) & (value < max(self.data1['{} {}'.format(self.well_name,self.from_unit)].to_list()))):
            mask_lower_position_from = self.data1['{} {}'.format(self.well_name,self.from_unit)] < value
            lower_position_from = max(self.data1['{} {}'.format(self.well_name,self.from_unit)].loc[mask_lower_position_from])
            mask_upper_position_from = self.data1['{} {}'.format(self.well_name,self.from_unit)] > value
            upper_position_from = min(self.data1['{} {}'.format(self.well_name,self.from_unit)].loc[mask_upper_position_from])

            index_lower_position_from = self.data1['{} {}'.format(self.well_name,self.from_unit)].to_list().index(lower_position_from)
            index_upper_position_from = self.data1['{} {}'.format(self.well_name,self.from_unit)].to_list().index(upper_position_from)

            lower_position_to = self.data1['{} {}'.format(self.well_name,self.to_unit)].iloc[index_lower_position_from]
            upper_position_to = self.data1['{} {}'.format(self.well_name,self.to_unit)].iloc[index_upper_position_from]

            y = (upper_position_to-lower_position_to)
            x = (upper_position_from - lower_position_from)
            slope = y/x
            intercept = upper_position_to - (slope*upper_position_from)

            return ((slope*self.value) + intercept)



        elif (value > max(self.data1['{} {}'.format(self.well_name,self.from_unit)].to_list())):
            upper_position_from = (self.data1['{} {}'.format(self.well_name,self.from_unit)]).dropna().to_list()[-1]
            lower_position_from = (self.data1['{} {}'.format(self.well_name,self.from_unit)]).dropna().to_list()[0]
            upper_position_to = (self.data1['{} {}'.format(self.well_name,self.to_unit)]).dropna().to_list()[-1]
            lower_position_to = (self.data1['{} {}'.format(self.well_name,self.to_unit)]).dropna().to_list()[0]

            y = (upper_position_to-lower_position_to)
            x = (upper_position_from - lower_position_from)
            slope = y/x
            intercept = upper_position_to - (slope*upper_position_from)

            return ('You are converting a depth beyond the survey via Extrapolation {}'.format((slope*self.value) + intercept))

#----------------------------------------
Ans = Deviation(well_name=input('Well name: Choose from Well_1 Well_2 Well_3+...+Well_4? '))
#----------------------------------------
# choose well name from below list
#Well_1 Well_2 Well_3+...+Well_4
#----------------------------------------
print(Ans.get_unit(float(input('Depth to convert')),input('Unit you have: WLM, MD, TVD, TVDss or MDss? '),input('Unit you want: WLM, MD, TVD, TVDss or MDss? ')))
#----------------------------------------
#number you want to convert
# unit you have
# unit you want


