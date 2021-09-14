"""
   +===================+========-========*========-========+===================+
   ||                               pdf_txt_2_df.py$                          ||
   ||                      by Abigail Miller (8/30/2021)                      ||
   ||                       American Institutes for Research                  ||
   ||                          CARES_Web_Scraping                             ||
   ||                                                                         ||
   || Description:                                                            ||
   || Takes in output from pdf_2_txt.py and copies information to dataframe   ||
   ||                                                                         ||
   ||                                                                         ||
   || Language:  Python 3.8.8                                                 ||
   || Graphics:  None                                                         ||
   || Downloads: None                                                         ||
   || Run time:  Approx. XX seconds                                           ||
   +===========================================================================+
   +===============+==========-==========*==========-==========+===============+
                                   CHANGE LOGS
                          DATA || CHANGE || SECTION || USER
    [1] (8/30/2021) Initial construction of script by A. Miller
   +===============+==========-==========*==========-==========+===============+
"""

#%%

""" Set up """

import pandas as pd

df = pd.DataFrame(columns=['line'], dtype='string')

#txt_file_path = "./text_versions/HEERF Quarterly Budget and Expenditure Reporting - V1_3_1.txt"
txt_file_path = "./text_versions/HEERF_Quarterly_Budget_and_Expenditure_Public_Posting_FINAL_accessible.txt"

#%%

""" find the line where 'Institution Name:' exists """
fp = open(txt_file_path, 'r', encoding='UTF-8')
lines = fp.readlines()
for item in lines: 
    if ("Institution Name:" in item):
        idx = lines.index(item)

#%%
def extractLines(txtfile):    
    #lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()
    for item in lines:
        if ((not (u"\u00A0" in item)) & (":" in item) & (not("http" in item))):
            idx = lines.index(item)
            #df_idx = idx - 163
            df.loc[idx,'line']=item
            df.loc[idx,'line2']=item.strip()
    #df.reset_index()
    fp.close()

df2 = pd.DataFrame(columns=['line'], dtype='string')

def extractLines2(txtfile):    
    #lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()
#    idx_list = []
    for item in lines:
        if ("Institution Name:" in item):
            start_idx = lines.index(item)
    for item in lines:
        if (lines.index(item) >= start_idx):
            idx = lines.index(item)
            df2.loc[idx,'line']=item
            df2.loc[idx,'line2']=item.strip()
    fp.close()

extractLines(txt_file_path)
extractLines2(txt_file_path)

df.index = pd.RangeIndex(len(df.index))
df2.index=pd.RangeIndex(len(df2.index))

#%%
for item in df['line2']:
    idx = list(df['line2']).index(item)
    splitList = item.split(':')
    ans = splitList[-1].strip()
    #question = splitList[0].strip()+":"+splitList[1].strip
    question = item.replace(ans,'')
    df.loc[idx,'question'] = question
    df.loc[idx,'answer'] = ans

#%%
""" -----------------------------------------------------------------"""

import os
import glob
import pandas as pd

#%%
""" setup dataframe """

# define dictionary where columns for dataframe correspond to necessary boxes in report
d = {
    'Institution Name':'INST',
    'Date of Report':'DATE',
    'Covering Quarter Ending':'QTREND',
    'Total Amount of Funds Awarded Section a1 Institutional Portion':'TOP_a1',
    'Section a2':'TOP_a2',
    'Section a3':'TOP_a3',
    'Final Report':'FINAL',
    'Amount in a1 institutional dollarsProviding additional emergency financial aid grants to students1':'R1C1',
    'Amount in a2 dollars if applicableProviding additional emergency financial aid grants to students1':'R1C2',
    'Amount in a3 dollars if applicableProviding additional emergency financial aid grants to students1':'R1C3',
    'Explanatory NotesProviding additional emergency financial aid grants to students1':'R1C4',
    'Amount in a1 institutional dollarsProviding reimbursements for tuition housing room and board or other fee refunds':'R2C1',
    'Amount in a2 dollars if applicableProviding reimbursements for tuition housing room and board or other fee refunds':'R2C2',
    'Amount in a3 dollars if applicableProviding reimbursements for tuition housing room and board or other fee refunds':'R2C3',
    'Explanatory NotesProviding reimbursements for tuition housing room and board or other fee refunds':'R2C4',
    'Amount in a2 dollars if applicableProviding tuition discounts':'R3C2',
    'Amount in a3 dollars if applicableProviding tuition discounts':'R3C3',
    'Explanatory NotesProviding tuition discounts':'R3C4',
    'Amount in a1 institutional dollarsCovering the cost of providing additional technology hardware to students such as laptops or tablets or covering the added cost of technology fees':'R4C1',
    'Amount in a2 dollars if applicableCovering the cost of providing additional technology hardware to students such as laptops or tablets or covering the added cost of technology fees':'R4C2',
    'Amount in a3 dollars if applicableCovering the cost of providing additional technology hardware to students such as laptops or tablets or covering the added cost of technology fee':'R4C3',
    'Explanatory NotesCovering the cost of providing additional technology hardware to students such as laptops or tablets or covering the added cost of technology fees':'R4C4',
    'Amount in a1 institutional dollarsProviding or subsidizing the costs of highspeed internet to students or faculty to transition to an online environment':'R5C1',
    'Amount in a2 dollars if applicableProviding or subsidizing the costs of highspeed internet to students or faculty to transition to an online environment':'R5C2',
    'Amount in a3 dollars if applicableProviding or subsidizing the costs of highspeed internet to students or faculty to transition to an online environment':'R5C3',
    'Explanatory NotesProviding or subsidizing the costs of highspeed internet to students or faculty to transition to an online environment':'R5C4',
    'Amount in a1 institutional dollarsSubsidizing offcampus housing costs due to dormitory closures or decisions to limit housing to one student per room subsidizing housing costs to reduce housing density paying for hotels or other offcampus housing for students who need to be isolated paying travel expenses for students who need to leave campus early due to coronavirus infections or campus interruptions':'R6C1',
    'Amount in a2 dollars if applicableSubsidizing offcampus housing costs due to dormitory closures or decisions to limit housing to one student per room subsidizing housing costs to reduce housing density paying for hotels or other offcampus housing for students who need to be isolated paying travel expenses for students who need to leave campus early due to coronavirus infections or campus interruptions':'R6C2',
    'Amount in a3 dollars if applicableSubsidizing offcampus housing costs due to dormitory closures or decisions to limit housing to one student per room subsidizing housing costs to reduce housing density paying for hotels or other offcampus housing for students who need to be isolated paying travel expenses for students who need to leave campus early due to coronavirus infections or campus interruptions':'R6C3',
    'Explanatory NotesSubsidizing offcampus housing costs due to dormitory closures or decisions to limit housing to one student per room subsidizing housing costs to reduce housing density paying for hotels or other offcampus housing for students who need to be isolated paying travel expenses for students who need to leave campus early due to coronavirus infections or campus interruptions':'R6C4',
    'Amount in a1 institutional dollarsSubsidizing food service to reduce density in eating facilities to provide prepackaged meals or to add hours to food service operations to accommodate social distancing':'R7C1',
    'Amount in a2 dollars if applicableSubsidizing food service to reduce density in eating facilities to provide prepackaged meals or to add hours to food service operations to accommodate social distancing':'R7C2',
    'Amount in a3 dollars if applicableSubsidizing food service to reduce density in eating facilities to provide prepackaged meals or to add hours to food service operations to accommodate social distancing':'R7C3',
    'Explanatory NotesSubsidizing food service to reduce density in eating facilities to provide prepackaged meals or to add hours to food service operations to accommodate social distancing':'R7C4',
    'Amount in a1 institutional dollarsCosts related to operating additional class sections to enable social distancing such as those for hiring more instructors and increasing campus hours of operations':'R8C1',
    'Amount in a2 dollars if applicableCosts related to operating additional class sections to enable social distancing such as those for hiring more instructors and increasing campus hours of operations':'R8C2',
    'Amount in a3 dollars if applicableCosts related to operating additional class sections to enable social distancing such as those for hiring more instructors and increasing campus hours of operations':'R8C3',
    'Explanatory NotesCosts related to operating additional class sections to enable social distancing such as those for hiring more instructors and increasing campus hours of operations':'R8C4',
    'Amount in a1 institutional dollarsCampus safety and operations2':'R9C1',
    'Amount in a2 dollars if applicableCampus safety and operations2':'R9C2',
    'Amount in a3 dollars if applicableCampus safety and operations2':'R9C3',
    'Explanatory NotesCampus safety and operations2':'R9C4',
    'Amount in a1 institutional dollarsPurchasing leasing or renting additional instructional equipment and supplies such as laboratory equipment or computers to reduce the number of students sharing equipment or supplies during a single class period and to provide time for disinfection between uses':'R10C1',
    'Amount in a2 dollars if applicablePurchasing leasing or renting additional instructional equipment and supplies such as laboratory equipment or computers to reduce the number of students sharing equipment or supplies during a single class period and to provide time for disinfection between uses':'R10C2',
    'Amount in a3 dollars if applicablePurchasing leasing or renting additional instructional equipment and supplies such as laboratory equipment or computers to reduce the number of students sharing equipment or supplies during a single class period and to provide time for disinfection between uses':'R10C3',
    'Explanatory NotesPurchasing leasing or renting additional instructional equipment and supplies such as laboratory equipment or computers to reduce the number of students sharing equipment or supplies during a single class period and to provide time for disinfection between uses':'R10C4',
    'Amount in a2 dollars if applicableReplacing lost revenue due to reduced enrollment':'R11C2',
    'Amount in a3 dollars if applicableReplacing lost revenue due to reduced enrollment':'R11C3',
    'Explanatory NotesReplacing lost revenue due to reduced enrollment':'R11C4',
    'Amount in a2 dollars if applicableReplacing lost revenue from nontuition sources ie cancelled ancillary events disruption of food service dorms childcare or other facilities cancellation of use of campus venues by other organizations lost parking revenue etc3':'R12C2',
    'Amount in a3 dollars if applicableReplacing lost revenue from nontuition sources ie cancelled ancillary events disruption of food service dorms childcare or other facilities cancellation of use of campus venues by other organizations lost parking revenue etc3':'R12C3',
    'Explanatory NotesReplacing lost revenue from nontuition sources ie cancelled ancillary events disruption of food service dorms childcare or other facilities cancellation of use of campus venues by other organizations lost parking revenue etc3':'R12C4',
    'Amount in a1 institutional dollarsPurchasing faculty and staff training in online instruction or paying additional funds to staff who are providing training in addition to their regular job responsibilities':'R13C1',
    'Amount in a2 dollars if applicablePurchasing faculty and staff training in online instruction or paying additional funds to staff who are providing training in addition to their regular job responsibilities':'R13C2',
    'Amount in a3 dollars if applicablePurchasing faculty and staff training in online instruction or paying additional funds to staff who are providing training in addition to their regular job responsibilities':'R13C3',
    'Explanatory NotesPurchasing faculty and staff training in online instruction or paying additional funds to staff who are providing training in addition to their regular job responsibilities':'R13C4',
    'Amount in a1 institutional dollarsPurchasing leasing or renting additional equipment or software to enable distance learning or upgrading campus wifi access or extending open networks to parking lots or public spaces etc':'R14C1',
    'Amount in a2 dollars if applicablePurchasing leasing or renting additional equipment or software to enable distance learning or upgrading campus wifi access or extending open networks to parking lots or public spaces etc':'R14C2',
    'Amount in a3 dollars if applicablePurchasing leasing or renting additional equipment or software to enable distance learning or upgrading campus wifi access or extending open networks to parking lots or public spaces etc':'R14C3',
    'Explanatory NotesPurchasing leasing or renting additional equipment or software to enable distance learning or upgrading campus wifi access or extending open networks to parking lots or public spaces etc':'R14C4',
    'Amount in a1 institutional dollarsOther Uses of a1 Institutional Portion funds4':'R15C1',
    'Explanatory NotesOther Uses of a1 Institutional Portion funds4':'R15C4',
    'Amount in a2 dollars if applicableOther Uses of a2 or a3 funds if applicable5':'R16C2',
    'Amount in a3 dollars if applicableOther Uses of a2 or a3 funds if applicable5':'R16C3',
    'Explanatory NotesOther Uses of a2 or a3 funds if applicable5':'R16C4',
    'Amount in a1 institutional dollarsQuarterly Expenditures for each Program':'R17C1',
    'Amount in a2 dollars if applicableQuarterly Expenditures for each Program':'R17C2',
    'Amount in a3 dollars if applicableQuarterly Expenditures for each Program':'R17C3',
    'Total of Quarterly Expenditures':'TOTQTREXP'
    # 'Amount in a3 dollars if applicableProviding or subsidizing the costs of highspeed internet to students or faculty to transition to an online environment: 32
    # 'Amount in a2 dollars if applicableProviding or subsidizing the costs of highspeed internet to students or faculty to transition to an online environment: 3
    # 'Amount in a1 institutional dollarsSubsidizing offcampus housing costs due to dormitory closures or decisions to limit housing to one student per room subsidizing housing costs to reduce housing density paying for hotels or other offcampus housing for students who need to be isolated paying travel expenses for students who need to leave campus early due to coronavirus infections or campus interruptions: 0
    # 'Amount in a2 dollars if applicableSubsidizing offcampus housing costs due to dormitory closures or decisions to limit housing to one student per room subsidizing housing costs to reduce housing density paying for hotels or other offcampus housing for students who need to be isolated paying travel expenses for students who need to leave campus early due to coronavirus infections or campus interruptions: 2
    # 'Amount in a3 dollars if applicableSubsidizing offcampus housing costs due to dormitory closures or decisions to limit housing to one student per room subsidizing housing costs to reduce housing density paying for hotels or other offcampus housing for students who need to be isolated paying travel expenses for students who need to leave campus early due to coronavirus infections or campus interruptions: 43
    # 'Amount in a1 institutional dollarsPurchasing leasing or renting additional instructional equipment and supplies such as laboratory equipment or computers to reduce the number of students sharing equipment or supplies during a single class period and to provide time for disinfection between uses: 0
    # 'Amount in a2 dollars if applicablePurchasing leasing or renting additional instructional equipment and supplies such as laboratory equipment or computers to reduce the number of students sharing equipment or supplies during a single class period and to provide time for disinfection between uses: 321
    # 'Amount in a3 dollars if applicablePurchasing leasing or renting additional instructional equipment and supplies such as laboratory equipment or computers to reduce the number of students sharing equipment or supplies during a single class period and to provide time for disinfection between uses: 44
    }

root_dir = '.'
text_files_dir = os.path.join(root_dir, 'text_versions')

df = pd.DataFrame(columns=list(d),dtype='string',index=range(0,len(os.listdir(text_files_dir))))

#%%

def extractLines(txtfile):    
    #lines_to_read = range(163,232)
    fp = open(txtfile, 'r', encoding='UTF-8')
    lines = fp.readlines()
#    idx_list = []
    for item in lines:
        if ("Institution Name:" in item):
            start_idx = lines.index(item)
    for item in lines:
        if (lines.index(item) >= start_idx):
            idx = lines.index(item)
            df2.loc[idx,'line']=item
            df2.loc[idx,'line2']=item.strip()
    fp.close()

#%%
for folder in os.listdir(text_files_dir):
    print("Working in folder {}".format(folder))
    if folder.startswith('.'):
        print("Skipping folder {}".format(folder))
        continue
    for file in os.listdir(os.path.join(text_files_dir,folder)):
        filename = "{}".format(file)
        print("Working with "+ filename)
        file_path = os.path.join(os.path.join(text_files_dir,folder),filename)
        fp = open(file_path, 'r', encoding='UTF-8')
        lines = fp.readlines()
        for item in lines:
            if ((not (u"\u00A0" in item)) & (":" in item) & (not("http" in item))):
                if item == '':
                    print("item is empty")
                else:
                    print("Working with item "+ item)
                splitList = item.split(':')
                ans = splitList[-1].strip()
                question = item.replace(ans,'')
                for key, value in d.items():
                    if key in lines:
                        df.loc[df.column == key, =ans
        fp.close()
