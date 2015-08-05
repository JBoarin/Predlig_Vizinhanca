'''
Created on Jun 16, 2015

@author: cptullio
'''
import numpy
from formating.dblp.Formating import Formating
from datetime import datetime
from networkx.classes.function import neighbors
from formating.FormatingDataSets import FormatingDataSets
from calculating.VariableSelection import VariableSelection

class Calculate(object):
	
	
	def reading_calculateLine(self, line):
		calcs = []
		cols = line.split('\t')
		for indice in range(len(cols) -2 ):
			calcs.append(float(line.split('\t')[indice].split(':')[1].replace('}','').strip()) )
		return [calcs, cols[len(cols)-2], cols[len(cols)-1].replace('\n', '')  ] 
		
	
	
	
	def printProgressofEvents(self, element, length, message):
		print message, str((float(element)/float(length))*float(100)) + '%', datetime.today()
		
	#after calculating we making the ordering.  This work depends on the quantity of feature
	def orderingCalculate(self):
		print "Starting Ordering the Calculating File", datetime.today()
		
		fResult = open(self.filepathResult, 'r')
		fcontentMaxMin = open(self.filepathMaxMinCalculated, 'r')
		line = fcontentMaxMin.readline().replace('\n', '')
		data = line.split('\t')
		qtyDataCalculated = int(data[0])
		minValuesCalculated = eval(data[1])
		maxValuesCalculated = eval(data[2])
		fcontentMaxMin.close()
		result = []
		orderedResult = None
		if len(self.preparedParameter.featuresChoice) > 1:
			element = 0
			for resultLine in fResult:
				element = element+1
				self.printProgressofEvents(element, qtyDataCalculated, "Normalizing Calculations: ")
				itemcalculations = self.reading_calculateLine(resultLine)
				
				newValues = []
				for indice in range(len(itemcalculations[0])):
					xnormalize = (itemcalculations[0][indice] - minValuesCalculated[indice])/(maxValuesCalculated[indice] - minValuesCalculated[indice])
					#print xnormalize, item, minvalueofCalculate, maxvalueofCalculate
					newValues.append(xnormalize)
				result.append( [numpy.sum(newValues), newValues, itemcalculations[0], itemcalculations[1],itemcalculations[2]  ] )
				
			orderedResult = sorted(result, key=lambda sum_value: sum_value[0], reverse=True)
			
			with open(self.filePathOrdered, 'w') as myfile:
				element = 0
				for item in orderedResult:
					element = element + 1
					self.printProgressofEvents(element, qtyDataCalculated, "Saving data ordered: ")
					myfile.write(str(item[0]) +  '\t' + str(item[1]) +  '\t' +str(item[2]) +  '\t' +str(item[3]) + '\t' +str(item[4]) +'\n')
			
		else:
			element = 0
			for resultLine in fResult:
				element = element+1
				self.printProgressofEvents(element, qtyDataCalculated, "Reading Calculations: ")
				itemcalculations = self.reading_calculateLine(resultLine)
				result.append( [itemcalculations[0][0], itemcalculations[1],itemcalculations[2]  ] )
			orderedResult = sorted(result, key=lambda sum_value: sum_value[0], reverse=True)
			
			with open(self.filePathOrdered, 'w') as myfile:
				element = 0
				for item in orderedResult:
					element = element + 1
					self.printProgressofEvents(element, qtyDataCalculated, "Saving data ordered: ")
					myfile.write(str(item[0]) +  '\t' + str(item[1]) +  '\t' +str(item[2]) +  '\r\n')
		
		print "Ordering the Calculating File finished", datetime.today()
				
		

	
	
	def __init__(self, preparedParameter, filepathNodesNotLinked, filepathResult, filePathOrdered, filepathMaxMinCalculated):
		print "Starting Calculating Nodes not linked", datetime.today()
		
		self.preparedParameter = preparedParameter
		self.filePathOrdered = Formating.get_abs_file_path(filePathOrdered)
		self.filepathMaxMinCalculated = Formating.get_abs_file_path(filepathMaxMinCalculated)
		self.filepathResult = Formating.get_abs_file_path(filepathResult)
		self.filepathNodesNotLinked = Formating.get_abs_file_path(filepathNodesNotLinked)
		#for each links that is not linked all the calculates is done.
		element = 0
		qtyofResults = FormatingDataSets.getTotalLineNumbers(self.filepathNodesNotLinked)
		fcontentNodesNotLinked = open(self.filepathNodesNotLinked, 'r')
		fcontentCalcResult = open(self.filepathResult, 'w')
		
		self.minValueCalculated = list(99999 for x in self.preparedParameter.featuresChoice)
		self.maxValueCalculated = list(0 for x in self.preparedParameter.featuresChoice)
		
		qtyFeatures = len(self.preparedParameter.featuresChoice)
		qtyNodesCalculated = 0
		for lineofFile in fcontentNodesNotLinked:
			element = element+1
			self.printProgressofEvents(element, qtyofResults, "Calculating features for nodes not liked: ")
			item = VariableSelection.getItemFromLine(lineofFile)
			
			for neighbor_node in item[1]:
				qtyNodesCalculated = qtyNodesCalculated + 1
				item_result = []
				#executing the calculation for each features chosen at parameter
				for index_features in range(qtyFeatures):
					self.preparedParameter.featuresChoice[index_features][0].parameter = preparedParameter
					valueCalculated = self.preparedParameter.featuresChoice[index_features][0].execute(item[0],neighbor_node) * self.preparedParameter.featuresChoice[index_features][1]
					if valueCalculated < self.minValueCalculated[index_features]:
						self.minValueCalculated[index_features] = valueCalculated
					if valueCalculated > self.maxValueCalculated[index_features]:
						self.maxValueCalculated[index_features] = valueCalculated
						
					item_result.append(valueCalculated)
					
				#generating a vetor with the name of the feature and the result of the calculate
				for indice in range(qtyFeatures):
					fcontentCalcResult.write( str({str(self.preparedParameter.featuresChoice[indice]):item_result[indice]}) )
					fcontentCalcResult.write('\t')
				fcontentCalcResult.write(str(item[0]) + '\t' + str(neighbor_node)  + '\n'  )
				
		fcontentCalcResult.flush()
		fcontentCalcResult.close()
		fcontentNodesNotLinked.close()
		fcontentMaxMin = open(self.filepathMaxMinCalculated, 'w')
		fcontentMaxMin.write(str(qtyNodesCalculated) + '\t' + repr(self.minValueCalculated) + '\t' + repr(self.maxValueCalculated) )
		fcontentMaxMin.close()
		print "Calculating Nodes not linked finished", datetime.today()
		
		