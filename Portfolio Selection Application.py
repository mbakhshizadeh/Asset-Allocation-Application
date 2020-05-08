import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib as mpl # optional (here)
import matplotlib.pyplot as plt
import seaborn as sns # Optional, will 
from ipywidgets import widgets, interactive
from tkinter.filedialog import askopenfilename

####################################################################################################################################################   
####################################################################################################################################################   
####################################################################################################################################################   
class MyWindow:
            
    def __init__(self, parent): 

        self.parent = parent

        
        self.text = tk.Text(self.parent,bg='#BBB6B3')
        self.text.pack(fill=tk.BOTH,side = "top")
        

        #####################################
        # Buttons
        self.label2 = tk.Label(self.parent,  text=" Step 1: Insert Risk-Free Rate in Percent: Like -->  2",fg="#CF5506",font=("Times New Roman", 10))
        self.label2.pack(side = 'top')
        self.entry1 = tk.Entry (self.parent,bd=3) 
        self.entry1.pack(side='top')
        
        #####################################
        self.b2 = tk.Button(self.parent, text='Step 2: LOAD DATA', command=self.load, fg='red',font=("Times New Roman", 10))
        self.b2.pack(side="left")
        
        #####################################
        self.b5= tk.Button(self.parent, text='Step 3: Start', command=self.display_simulated, fg='blue',font=("Times New Roman", 10))
        self.b5.pack(side="left")
        
        #####################################
        self.b4 = tk.Button(self.parent, text='Step 4: Graph', command=self.plot, fg='green',font=("Times New Roman", 10))
        self.b4.pack(side="left")


        #####################################
        self.widget_box = tk.Text(self.parent, fg='#000000',bg='#BBB6B3')                     
        self.widget_box.place(height=215,width=980,x=300, y=435)
        self.widget_box.insert(tk.END, '\t\t\t\t\t\t\t'+str("Asset Allocation")+ "\n ")  
        self.widget_box.insert(tk.END, str("Asset classes would be divided into equity, fix-income, cash and alternative investment such as commodity futures and options contracts).This application receives asset classes’ returns and then applies resampling method to generates asset weights for a million times. Using these weights, the efficient frontier will be plotted and then by considering appropriate risk-free interest rate and those weights that end up the highest sharp ratio, tangency point (optimal point=) will be selected as the best portfolio.")+'\n\n')       
        self.widget_box.insert(tk.END, str("Instruction:")+'\n') 
        self.widget_box.insert(tk.END, '\t'+str("1-      Assign appropriate risk-free interest rate.")+'\n')
        self.widget_box.insert(tk.END, '\t'+str("2-	Click “Load Data” to input data as an excel file (CSV, XLSX, XLS).")+'\n')
        self.widget_box.insert(tk.END, '\t\t'+str("In the excel, put each asset return in each column (column name should be defined).")+'\n') 
        self.widget_box.insert(tk.END, '\t'+str("3-	Click “Start” to run the code. The outcome will appear on the above text widget.")+'\n')
        self.widget_box.insert(tk.END, '\t'+str("4-	Click “Graph” to generate efficient frontier on an external window. You can save the graph.")+'\n')

 ####################################################################################################################################################   
    def load(self):

        data_name = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])
        if data_name:
            if data_name.endswith('.csv'):
                self.df = pd.read_csv(data_name)

            else:
                self.df = pd.read_excel(data_name)


            self.filename = data_name
            
    #####################################        
    def plot (self):

        fig = plt.figure(figsize=(10, 7))
        plt.scatter((self.results[0,:]*100),(self.results[1,:]*100),c=self.results[2,:],cmap='YlGnBu', marker='o', s=10, alpha=0.3)
        plt.colorbar()
        plt.scatter((self.sdp*100),(self.rp*100),marker="X",color='r',s=100, label='Maximum Sharpe ratio')

        plt.title('Efficient Frontier')
        plt.xlabel('Volatility %')
        plt.ylabel('Returns %')
        plt.legend(labelspacing=0.8)
        
        canvas = FigureCanvasTkAgg(fig, master=self.parent)
        #canvas.get_tk_widget().pack(side="left")
        canvas.draw()


    #####################################
    def var_cov_mean(self,data):
        data=data
        self.cov_matrix=pd.DataFrame(data.cov())
        self.mean=pd.DataFrame(data.mean())
        return(self.cov_matrix, self.mean)
        
    #####################################
    def portfolio_performance(self,weights,mean_returns, cov_matrix, data):
         weights_1= pd.DataFrame(weights)
         mean_returns_1= mean_returns
         cov_matrix_1= cov_matrix
         #self.df=data
         self.returns = np.sum(np.array(mean_returns_1)*np.array(weights_1))
    
         tem_sum_1=0
         for i in range(len(cov_matrix_1)):
             tem_sum_1=tem_sum_1 + (cov_matrix_1.iloc[i,i]*weights_1.iloc[i]*weights_1.iloc[i])
     
         tem_sum_2=0 
         for j in range(len(cov_matrix_1)):
             for k in range(j+1,len(cov_matrix_1.columns)):
                 tem_sum_2= tem_sum_2+ (2*cov_matrix_1.iloc[j,k]*weights_1.iloc[j]*weights_1.iloc[k])
                   
         self.std = np.sqrt(tem_sum_1 + tem_sum_2)
         return(self.std ,self.returns)
    
    
    #####################################
    def random_portfolios(self,num_portfolios, data,risk_free_rate):
        data=pd.DataFrame(data)
        cov_matrix_1, mean_returns= self.var_cov_mean(data)
        num_portfolios=num_portfolios
        risk_free_rate_1=risk_free_rate
        self.results = np.zeros((3,num_portfolios))
        self.weights_record = []
        for i in range(num_portfolios): 
            weights = np.random.random(len(mean_returns))
            weights = weights/np.sum(weights)
            self.weights_record.append(weights)
            portfolio_std_dev, portfolio_return = self.portfolio_performance(pd.DataFrame(weights), mean_returns, cov_matrix_1, data)
            self.results[0,i] = portfolio_std_dev
            self.results[1,i] = (portfolio_return)
            self.results[2,i] = (portfolio_return - risk_free_rate_1) / portfolio_std_dev
            
        return(self.results, self.weights_record)

    #####################################
    def display_simulated(self):
        self.text.delete('1.0', tk.END) # Clear content after clicking again on "Start".
        results_1, weights_record_1 = self.random_portfolios(1000, self.df, float(self.entry1.get())/100)
        max_sharpe_idx = np.argmax(results_1[2])
        self.sdp, self.rp = self.results[0,max_sharpe_idx], self.results[1,max_sharpe_idx]
        max_sharpe_allocation = pd.DataFrame(weights_record_1[max_sharpe_idx])
        max_sharpe_allocation.index=list(self.df.columns)
        max_sharpe_allocation.columns=["Allocations: %"]
        max_sharpe_allocation = max_sharpe_allocation.T
        self.text.insert(tk.END, str('Risk Free Interest Rate:' + str(self.entry1.get())+ str('%') )+ '\n\n') 
        self.text.insert(tk.END, str(round(max_sharpe_allocation*100,2)) + '\n\n') 
        self.text.insert(tk.END, str('Portfolio Return:%'+ str(round(self.rp*100,2))) +'\n') 
        self.text.insert(tk.END, str('Portfolio Risk: %'+ str(round(self.sdp*100,2))) +'\n') 
        


####################################################################################################################################################    
root = tk.Tk()
top = MyWindow(root)
root.title('Asset Allocation')
root['bg'] = '#504C49'

root.mainloop()   
    
    


        

  
    
    


        

  