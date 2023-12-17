#the first of use could be necessary install the following library
#pip install customtkinter

#define libraries
import numpy as np
from tkinter import *
import tkinter
import customtkinter

#define a theme for the app
customtkinter.set_appearance_mode("dark")

#define root window
root = customtkinter.CTk()
root.title("Energetic Spam Model")
root.geometry("1000x1000")

#define calculations

def results():
    #define variables
    T = input1.get() 
    Ei1 = input2.get()
    ETS1 = input3.get()
    Ei2 = input4.get()
    ETS2 = input5.get()
    Ei3 = input6.get()
    ETS3 = input7.get()
    Ei4 = input8.get()
    ETS4 = input9.get()
    conEi1 = input10.get()
    conEi2 = input11.get()
    conEi3 = input12.get()
    conEi4 = input13.get()
    conEts1 = input14.get()
    conEts2 = input15.get()
    conEts3 = input16.get()
    conEts4 = input17.get()
    
    #define constants
    Kbh = 20836643994
    Kbcal = 0.001987207
    
    #calculate TOF
    A = np.array([[float(Ei1),float(ETS1)],[float(Ei2),float(ETS2)],[float(Ei3),float(ETS3)],[float(Ei4),float(ETS4)]])
    n_filas = A.shape[0]#define the len of the array
    Grx = A[n_filas-1,0] - A[0,0] #Calculate the difference of energy in the catalytic cycle
    term_exp = np.exp(-Grx / (Kbcal * float(T))) - 1 #calculate the exponential term in the numerator of TOF eq.
    Delta = float(T) * Kbh * term_exp #calculate the delta term in the equation of TOF.
    
    results = np.zeros((n_filas-1,n_filas-1))#This is an array filled with zeros to storage results
    
    for j in range(n_filas-1):# the range run from 0 to 3
        valor_Ets = A[j,1]#obtain values from the array
        
        for i in range(n_filas-1):#apply from 0 to 3 inside the other cycle
            valor_Ei = A[i,0]#obtain values from the array
            if j>=i:#run the calculations over the condition
                result = np.exp((valor_Ets-valor_Ei-Grx) / (Kbcal*float(T)))
            else:
                result = np.exp((valor_Ets-valor_Ei) / (Kbcal*float(T)))
            results[j,i] = result
    M = np.sum(results)#Calculate the sum over the result and filled the array
    
    TOF = round(Delta/M,10) #Calculate TOF
    Label10 = Label(root, text = f"{TOF}", font=("Arial", 15), bd=5,foreground="green")
    Label10.grid(row=7, column=4, padx=10, pady=10)#print the TOF result in the screen
    
    #Calculate xi and xts
    I = np.sum(results, axis=0)
    TS = np.sum(results, axis=1)
    xi = np.round(I/M,2)    
    xts = np.round(TS/M,2)
    data = np.column_stack((xi, xts))#put the data into columns
    pos_max_col1 = np.argmax(datos[:, 0])#gets the index of the maximum value in the array
    pos_max_col2 = np.argmax(datos[:, 1])
    valor_col1_A = A[pos_max_col1, 0]#obtain the value of the max value position in A
    valor_col2_A = A[pos_max_col2, 1]

    #Calculate TOF using ESM
    if valor_col2_A >= valor_col1_A:
        Resultado_TOF = float(T) * Kbh * np.exp((-1) * (valor_col2_A - valor_col1_A) / (Kbcal * float(T)))
        ESM = valor_col2_A - valor_col1_A
    else:
        Resultado_TOF = float(T) * Kbh * np.exp((-1) * (valor_col2_A - valor_col1_A + Grx) / (Kbcal * float(T)))
        ESM = valor_col2_A - valor_col1_A + Grx

    
    #calculate TOF taking into account the concentration
    conc = np.array([[float(conEi1),float(conEts1)],[float(conEi2),float(conEts2)],[float(conEi3),float(conEts3)],[float(conEi4),float(conEts4)]])
    
    p1=pos_max_col1
    p2=pos_max_col2
    
    Values_Pro = CON[p1:p2 + 1, :]#give the values in that position on conc array
    
    productoria = np.prod(Values_Pro[:, 0] / Values_Pro[:, 1])
    TOF_CON = Resultado_TOF * productoria
    
    
    Label11 = Label(root, text = f"{xi[0]}", font=("Arial", 15), foreground="green")
    Label11.grid(row=3, column=3, padx=10, pady=10)
    
    Label12 = Label(root, text = f"{xi[1]}", font=("Arial", 15), foreground="green")
    Label12.grid(row=4, column=3, padx=10, pady=10)
    
    Label13 = Label(root, text = f"{xi[2]}", font=("Arial", 15), foreground="green")
    Label13.grid(row=5, column=3, padx=10, pady=10)
    
    Label14 = Label(root, text = f"{xts[0]}", font=("Arial", 15), foreground="green")
    Label14.grid(row=3, column=4, padx=10, pady=10)
    
    Label15 = Label(root, text = f"{xts[1]}", font=("Arial", 15), foreground="green")
    Label15.grid(row=4, column=4, padx=10, pady=10)
    
    Label16 = Label(root, text = f"{xi[2]}", font=("Arial", 15), foreground="green")
    Label16.grid(row=5, column=4, padx=10, pady=10)
    
    Label17 = Label(root, text = f"{Grx}", font=("Arial", 15), foreground="green")
    Label17.grid(row=8, column=4, padx=10, pady=10)
    

#define labels for the entries and results
Label1 = Label(master=root, text="Input Data", font=("Arial", 18), bd=5)
Label1.grid(row=0, column=1, padx=50, pady=30)

Label2 = Label(root, text="Ei(kcal/mol)", font=("Arial", 15),bd=5)
Label2.grid(row=2, column=0, padx=5, pady=10)

Label3 = Label(root, text="ETS(kcal/mol)", font=("Arial", 15),bd=5)
Label3.grid(row=2, column=1, padx=5, pady=10)

Label4 = Label(root, text="Results" , font=("Arial", 18), bd=5)
Label4.grid(row=0, column=4, padx=50, pady=30)

Label5 = Label(root, text="Xi", font=("Arial", 18), bd=5)
Label5.grid(row=2, column=4, padx=10, pady=10)

Label6 = Label(root, text="Xts", font=("Arial",18), bd=5)
Label6.grid(row=2, column=5, padx=10, pady=10)

Label7 = Label(root, text="TOF (1/s) =", font=("Arial",18), bd=5)
Label7.grid(row=7, column=4, padx=10, pady=10)

Label8 = Label(root,text="dE =" , font=("Arial",15), bd=5)
Label8.grid(row=8, column=4, padx=10, pady=10)

Label18 = Label(root, text="[React]", font=("Arial", 15),bd=5)
Label18.grid(row=2, column=2, padx=5, pady=10)

Label19 = Label(root, text="[Product]", font=("Arial", 15),bd=5)
Label19.grid(row=2, column=3, padx=5, pady=10)

#define entries
input1 = Entry(root,bd=5,foreground="red", width=16)
input1.grid(row=1, column=0, padx=10, pady=10)
input1.insert(0,"Temperature in K")
input1.bind("<Button-1>", lambda e: input1.delete(0, tkinter.END))

input2 = Entry(root,bd=5, foreground="red", width=12)
input2.grid(row=3, column=0, padx=10, pady=10)
input2.insert(0, "Ei1(kcal/mol)")
input2.bind("<Button-1>", lambda e: input2.delete(0, tkinter.END))

input3 = Entry(root, bd=5, foreground="red", width=12)
input3.grid(row=3, column=1, padx=10, pady=10)
input3.insert(0, "ETS1(kcal/mol)")
input3.bind("<Button-1>", lambda e: input3.delete(0, tkinter.END))

input4 = Entry(root, bd=5, foreground="red", width=12)
input4.grid(row=4, column=0, padx=10, pady=10)
input4.insert(0, "Ei2(kcal/mol)")
input4.bind("<Button-1>", lambda e: input4.delete(0, tkinter.END))

input5 = Entry(root, bd=5, foreground="red", width=12)
input5.grid(row=4, column=1, padx=10, pady=10)
input5.insert(0, "ETS2(kcal/mol)")
input5.bind("<Button-1>", lambda e: input5.delete(0, tkinter.END))

input6 = Entry(root, bd=5, foreground="red", width=12)
input6.grid(row=5, column=0, padx=10, pady=10)
input6.insert(0, "Ei3(kcal/mol)")
input6.bind("<Button-1>", lambda e: input6.delete(0, tkinter.END))

input7 = Entry(root, bd=5, foreground="red", width=12)
input7.grid(row=5, column=1, padx=10, pady=10)
input7.insert(0, "ETS3(kcal/mol)")
input7.bind("<Button-1>", lambda e: input7.delete(0, tkinter.END))

input8 = Entry(root, bd=5, foreground="red", width=12)
input8.grid(row=6, column=0, padx=10, pady=10)
input8.insert(0, "Ei4(kcal/mol)")
input8.bind("<Button-1>", lambda e: input8.delete(0, tkinter.END))

input9 = Entry(root, bd=5, foreground="red", width=12)
input9.grid(row=6, column=1, padx=10, pady=10)
input9.insert(0, "ETS4(kcal/mol)")
input9.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))

input10 = Entry(root, bd=5, foreground="red", width=9)
input10.grid(row=3, column=2, padx=10, pady=10)
input10.insert(0, "[1]")
input10.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))

input11 = Entry(root, bd=5, foreground="red", width=9)
input11.grid(row=4, column=2, padx=10, pady=10)
input11.insert(0, "[2]")
input11.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))

input12 = Entry(root, bd=5, foreground="red", width=9)
input12.grid(row=5, column=2, padx=10, pady=10)
input12.insert(0, "[3]")
input12.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))

input13 = Entry(root, bd=5, foreground="red", width=9)
input13.grid(row=6, column=2, padx=10, pady=10)
input13.insert(0, "[4]")
input13.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))

input14 = Entry(root, bd=5, foreground="red", width=9)
input14.grid(row=3, column=3, padx=10, pady=10)
input14.insert(0, "[1]")
input14.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))

input15 = Entry(root, bd=5, foreground="red", width=9)
input15.grid(row=4, column=3, padx=10, pady=10)
input15.insert(0, "[2]")
input15.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))

input16 = Entry(root, bd=5, foreground="red", width=9)
input16.grid(row=5, column=3, padx=10, pady=10)
input16.insert(0, "[3]")
input16.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))

input17 = Entry(root, bd=5, foreground="red", width=9)
input17.grid(row=6, column=3, padx=10, pady=10)
input17.insert(0, "[4]")
input17.bind("<Button-1>", lambda e: input9.delete(0, tkinter.END))


#define botton
boton = customtkinter.CTkButton(master=root, text="Run", width=150, command=results).grid(row=7, column=0, padx=10, pady=10)


root.mainloop()