import csv;
import argparse;
import sys;


PROGRAM_DESCRIPTION="""This script implements medical insurance costs project
from code academy's data scientist carerr path. By nwnebel
"""

INPUT_FILE="""Path to the csv fle containing medical insurance data.
This file is supposed to have 7 columns, the first row of
the file should contain columns headers. By default columns should be separated by commas.
The columns are following:
Column 1 -- should have header 'age', data in this column should contain person's age values.
Column 2 -- should have header 'sex', data in this column should contain person's sex ('female'/'male') values.
Column 3 -- should have header 'bmi', data in this column should contain person's body mass index values.
Column 4 -- should have header 'children', data in this column should contain person's children count (integers).
Column 5 -- should have header 'smoker', data in this column should contain person's smoker status ('yes' or 'no').
Column 6 -- should have header 'region', data in this column should contain person's geographical position.
Column 7 -- should have header 'charges', data in this column should contain person's insurance costs (float values).
""";
CSV_SEPARATOR_HELP="""string that separates columns inside the CSV input file. Default value is comma (',')
""";
CSV_SEPARATOR_DEFAULT=",";

AGE_ROUNDING_HELP="To what digit average age should be rounded. Default value is 1";
AGE_ROUNDING_DEFAULT=1;
CHARGES_ROUNDING_HELP="To what digit average charges should be rounded. Default value is 3";
CHARGES_ROUNDING_DEFAULT=3;


def parseCommandLineArguments():
    parser=argparse.ArgumentParser(description=PROGRAM_DESCRIPTION,formatter_class=argparse.RawTextHelpFormatter);
    parser.add_argument("inputFile",help=INPUT_FILE);
    parser.add_argument("-s",metavar="csv separator",help=CSV_SEPARATOR_HELP,default=CSV_SEPARATOR_DEFAULT);   
    parser.add_argument("-ar",metavar="digits",help=AGE_ROUNDING_HELP,default=AGE_ROUNDING_DEFAULT);
    parser.add_argument("-cr",metavar="digits",help=CHARGES_ROUNDING_HELP,default=CHARGES_ROUNDING_DEFAULT);
    args=parser.parse_args();
    return args;
    

#Read input csv file and save the results
def iterateFile(filePath): 
    #this flag will tell caller if input file parsed successfully. True - success, False -- error
    result=True;
    #this dictionary will contain all values found in the input file after
    #this function returned
    dataSet=[];
    try:
        with open(filePath,"r",newline='') as csvFile:
            reader=csv.DictReader(csvFile);
            for row in reader: #parsing every row in the input file. row variable -- dictionary               
               #dataSet.append(row);
               dataSet.append(PersonData(row));
    except:
        excp=sys.exc_info()[1];
        print("error iterating input file 'filePath'. Error text:{info}".format(info=str(excp)));       
        result=False;
    
    return (dataSet,result);



#This class structures parameters
#for the filters applied to the
#dataSet
class FilterParameter:    
    def __init__(self,minAge=None,maxAge=None,sex=None,minBmi=None,maxBmi=None,\
                 minChildren=None,maxChildren=None,smoker=None,\
                 region=None,minCharges=None,maxCharges=None):
                 
        self.minAge=minAge;
        self.maxAge=maxAge;
        self.sex=sex;
        self.minBmi=minBmi;
        self.maxBmi=maxBmi;
        self.minChildren=minChildren;
        self.maxChildren=maxChildren;
        self.smoker=smoker;
        self.region=region;
        self.minCharges=minCharges;
        self.maxCharges=maxCharges;
        
    
    def __str__(self):
        string="""age: [{minAge} ... {maxAge}]
sex={sex}
bmi: [{minBmi} ... {maxBmi}]
children: [{minChildren} ... {maxChildren}]
smoker: {smoker}
region: {region}
charges: [{minCharges} ... {maxCharges}]""".format(minAge=self.minAge,\
        maxAge=self.maxAge,sex=self.sex,minBmi=self.minBmi,\
        maxBmi=self.maxBmi,minChildren=self.minChildren,\
        maxChildren=self.maxChildren,smoker=self.smoker,\
        region=self.region,minCharges=self.minCharges,\
        maxCharges=self.maxCharges);
        return string;    
    


#Auxiliary class for computing region average charges
class RegionStat:

    def __init__(self,roundingDigits):
        self.sumCharges=0; #additive charges
        self.numEntries=1; 
        self.region="";
        self.roundingDigits=roundingDigits;
        
                
    def GetAverageCharges(self):
        ret=None;
        if(self.numEntries != 0):
            ret=self.sumCharges/self.numEntries;
        return ret;
        
    def __str__(self):
        string="{region} has average charges {charges}".\
        format(region=self.region,charges=round(self.GetAverageCharges(),self.roundingDigits));
        return string;
        

#This class represents Person's data found in the each row of the 
#input file
class PersonData:
       
    def GetSmokerStatus(self):
        if(self.smoker == "yes"):
            ret="smoker";
        else:
            ret="non-smoker";
            
        return ret;
    
    def GetInsuranceCost(self):
        #ret=self.charges.replace(".",""); #remove thousands separator
        ret=self.charges;
        return ret;
    
    def __init__(self,row):  
        self.age=int(row['age']);
        self.sex=row['sex'];
        self.bmi=row['bmi'];
        self.children=row['children'];
        self.smoker=row['smoker'];
        self.region=row['region'];
        self.charges=float(row['charges']);
        
    def __str__(self):
        ret="""
This person is {age} years old, {sex}, have bmi of {bmi}, 
have {children} children, {smoker}, lives in {region} region, 
pays for the insurance {cost} dollars""".format(age=self.age,sex=self.sex,\
bmi=self.bmi,children=self.children,smoker=self.GetSmokerStatus(),\
region=self.region,cost=self.GetInsuranceCost());
        return ret;
        
        
#Class combines functions for analyzing data 
#from the input file
class DataAnalyzer:
    
                   
    def PrintDataset(self,dataSet):     
        for person in dataSet:
            print(person);

#Finds average age of males and females 
#inside the input files
    def FindAverageAge(self,dataSet,roundingCount):
        malesAge=[person.age for person in dataSet if person.sex == "male"];
        femalesAge=[person.age for person in dataSet if person.sex == "female"];
        malesAverageAge=round(sum(malesAge)/len(malesAge),roundingCount);
        femalesAverageAge=round(sum(femalesAge)/len(femalesAge),roundingCount);
        return (malesAverageAge,femalesAverageAge);
    

#Count how many persons lives in every region and in which region
#lives most persons
    def CountByRegion(self,dataSet):
    
        regions={};    
        for person in dataSet:
            if person.region not in regions:
                regions[person.region]=0;
            regions[person.region]+=1;

        maxRegion="";
        maxCount=0;
        for (region,count) in regions.items():
            if(count > maxCount):
                maxRegion=region;
                maxCount=count;
            
        return (regions,maxRegion,maxCount);
                          
    #filter dataSet by age, returns records
    #for persons whose  minAge <= age <= maxAge
    def FilterByAge(self,minAge,maxAge,dataSet):        
        ret=[person for person in dataSet if person.age >= minAge and person.age <= maxAge];
        return ret;
                
    #filter dataSet by sex, return recods for
    #persons whos sex is equal to the requested
    def FilterBySex(self,sex, dataSet):
        ret=[person for person in dataSet if person.sex == sex];
        return ret;
        
    #filter dataSet by number of children, returns
    #persons whos number of children lies inside the
    #interval [minChildren,maxChildren]
    def FilterByChildren(self,minChildren,maxChildren):
        ret=[person for person in dataSet if person.children >= minChildren and person.children <= maxChildren];
        return ret;
        
    #filter dataSet by smoker status, returns
    #persons whos smoking status equals requested 
    #smoker status
    def FileterBySmoker(self,smokerStatus,dataSet):
        ret=[person for person in dataSet if person.smoker == smokerStatus];
        return ret;
        
    #filter dataSet by region, returns persons
    #who lives in the requested region
    def FilterByRegion(self,region,dataSet):
        ret=[person for person in dataSet if person.region == region];
        return ret;
    
    #filter dataSet by charges, returns persons
    #whos insurange charges lies inside the interval
    #[minCharge ... maxCharge]
    def FilterByCharges(self,minCharges,maxCharges,dataSet):
        ret=[person for person in dataSet if person.charges >= minCharges and person.charges <= maxCharges];
        return ret;
    
    #filter dataSet by bmi, returns persons
    #whos bmi lies inside the interval 
    #[minBmi ... maxBmi]
    def FilterByBMI(self,minBmi,maxBmi):
        ret=[person for person in dataSet if person.bmi >= minBmi and person.bmi <= maxBmi];
        return ret;
    
  
    #returns average insurance charges for the
    #dataSet
    def FindAverageCharges(self,dataSet,chargesRoundingDigit):
        charges=[person.charges for person in dataSet];
        ret=None;
        if(len(charges) > 0):
            ret=sum(charges);
            ret=round(ret/len(charges),chargesRoundingDigit);
        else:
            print("DataSet length is 0, can't compute average charges");
        return ret;
        
    
    #filter dataset based on provided FilterData object,
    #returns filtered dataSet
    def FilterDataSet(self,dataSet,filterParams):
        ret=dataSet;
        if(filterParams.minAge != None and filterParams.maxAge != None):
            ret=self.FilterByAge(filterParams.minAge,filterParams.maxAge,ret);            
        if(filterParams.sex != None):
            ret=self.FilterBySex(filterParams.sex,ret);
        if(filterParams.minBmi != None and filterParams.maxBmi != None):
            ret=self.FilterByBMI(filterParams.minBmi,filterParams.maxBm,ret);
        if(filterParams.minChildren != None and filterParams.maxChildren != None):
            ret=self.FilterByChildren(filterParams.minChildren,filterParams.maxChildren,ret);
        if(filterParams.smoker != None):
            ret=self.FileterBySmoker(filterParams.smoker,ret);
        if(filterParams.region != None):
            ret=self.FilterByRegion(filterParams.region,ret);
        if(filterParams.minCharges != None and filterParams.maxCharges != None):
            ret=self.FilterByCharges(filterParams.minCharges,filterParams.maxCharges,ret);
        return ret;
        
               
  

    
    
def findMalesAndFemalesAverageAge(analyzer,dataSet,ageRoundingDigit):

    #we don't wan't to apply any filters, we wan't to
    #analyze entire dataSet
    filterParams=FilterParameter();    
    filteredData=analyzer.FilterDataSet(dataSet,filterParams);
    
    (malesAverageAge,femalesAverageAge)=analyzer.FindAverageAge(filteredData,ageRoundingDigit);
    print("malesAverageAge={ma}; femalesAverageAge={fa}".format(ma=malesAverageAge,\
    fa=femalesAverageAge));
    

def findRegionWithMaxPersons(analyzer,dataSet):

    #we don't wan't to apply any filters, we wan't to
    #analyze entire dataSet
    filterParams=FilterParameter();  
    (regions,maxRegion,maxCount)=analyzer.CountByRegion(dataSet);
    print("most persons ({maxCount}) lives in the {maxRegion} region".\
    format(maxCount=maxCount,maxRegion=maxRegion));
 


#Find average insurance chareges for males
#and females without considering other factors
def findAverageChargesForMalesFemales(analyzer,dataSet,chargesRoundingDigit):

    filterParamsMales=FilterParameter(sex="male");  
    filterParmsFemales=FilterParameter(sex="female");  
    
    malesData=analyzer.FilterDataSet(dataSet,filterParamsMales);
    femalesData=analyzer.FilterDataSet(dataSet,filterParmsFemales);
    
    malesAverageCharges=analyzer.FindAverageCharges(malesData,chargesRoundingDigit);
    femalesAverageCharges=analyzer.FindAverageCharges(femalesData,chargesRoundingDigit);
    
    print("males total average charges: {malesCharges}; females total average chareges: {femaleCharges}".\
    format(malesCharges=malesAverageCharges,femaleCharges=femalesAverageCharges));
    

#Compare charges payed by smokers and non-smokers, both males and females
def compareSmokerAndNonSmokerStatusForMalesAndFemales(analyzer,dataSet,chargesRoundingDigit):

    filterParamsMalesSmoker=FilterParameter(sex="male",smoker="yes");
    filterParamsMalesNonSmoker=FilterParameter(sex="male",smoker="no");
    filterParamsFemalesSmoker=FilterParameter(sex="female",smoker="yes");
    filterParamsFemalesNonSmoker=FilterParameter(sex="female",smoker="no");
        
    malesSmokerData=analyzer.FilterDataSet(dataSet,filterParamsMalesSmoker);
    malesNonSmokerData=analyzer.FilterDataSet(dataSet,filterParamsMalesNonSmoker);
    femalesSmokerData=analyzer.FilterDataSet(dataSet,filterParamsFemalesSmoker);
    femalesNonSmokerData=analyzer.FilterDataSet(dataSet,filterParamsFemalesNonSmoker);
        
    malesSmokerAvgCharges=analyzer.FindAverageCharges(malesSmokerData,chargesRoundingDigit);
    malesNonSmokerAvgCharges=analyzer.FindAverageCharges(malesNonSmokerData,chargesRoundingDigit);
    femalesSmokerAvgCharges=analyzer.FindAverageCharges(femalesSmokerData,chargesRoundingDigit);
    femalesNonSmokerAvgCharges=analyzer.FindAverageCharges(femalesNonSmokerData,chargesRoundingDigit);
        
    print("males smoker average charges: {malesSmokerCharges}; males non-smoker average charges: \
{malesNonSmokerCharges}".format(malesSmokerCharges=malesSmokerAvgCharges,\
malesNonSmokerCharges=malesNonSmokerAvgCharges));

    print("females smoker average charges: {femalesSmokerCharges}; females non-smoker average charges: \
{femalesNonSmokerCharges}".format(femalesSmokerCharges=femalesSmokerAvgCharges,\
femalesNonSmokerCharges=femalesNonSmokerAvgCharges));
        


#find region with highest charges payed
def findRegionWithHighesCharges(dataSet,chargesRoundingDigit):

    chargesByRegion={};
    for person in dataSet:
        if(person.region not in chargesByRegion):
            chargesByRegion[person.region]=RegionStat(chargesRoundingDigit);
            chargesByRegion[person.region].region=person.region;
            
        chargesByRegion[person.region].sumCharges+=person.charges;
        chargesByRegion[person.region].numEntries+=1;
        
    maxCostRegion=RegionStat(chargesRoundingDigit);
    for region in chargesByRegion.values():
        if(region.GetAverageCharges() > maxCostRegion.GetAverageCharges()):
            maxCostRegion=region;
            
    print("Region with highest charges:",maxCostRegion);
        

def main():
    args=parseCommandLineArguments();    
    (dataSet,result)=iterateFile(args.inputFile);    
    if(result):
        #input file has been parsed successfully        
        analyzer=DataAnalyzer();
        findMalesAndFemalesAverageAge(analyzer,dataSet,args.ar);
        findRegionWithMaxPersons(analyzer,dataSet);       
        findAverageChargesForMalesFemales(analyzer,dataSet,args.cr);
        compareSmokerAndNonSmokerStatusForMalesAndFemales(analyzer,dataSet,args.cr);
        findRegionWithHighesCharges(dataSet,args.cr);
        
main();