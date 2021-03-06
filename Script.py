import pandas as pd
import numpy as np
import math
import scipy.stats as sp
import matplotlib.pyplot as plt

# <codecell>

# Data

Corn = pd.read_csv('HistoricalQuotes_Corn.csv')
Ethanol = pd.read_csv('HistoricalQuotes_Ethanol.csv')

Data_Frame = pd.merge(Corn, Ethanol, on = 'Date', how='inner')

Corn_DF = Data_Frame.iloc[:, 0 : 6]
Ethanol_DF = Data_Frame.iloc[:, 6 :]
Ethanol_DF.insert(0, 'Date', Data_Frame.iloc[:, 0])

Corn_DF.iloc[:, 1] = sp.mstats.winsorize(Corn_DF.iloc[:, 1], 0.001)
Ethanol_DF.iloc[:, 1] = sp.mstats.winsorize(Ethanol_DF.iloc[:, 1], 0.001)


# <codecell>

log_return = []

for i in range (0, len(Corn_DF)-1):
    a = math.log(Corn_DF.iloc[i,1]/Corn_DF.iloc[i+1,1])
    log_return = np.append(log_return, a)

log_return = np.append(log_return, 0)

Corn_DF['log_rendement'] = log_return


log_return = []

for i in range (0, len(Ethanol_DF)-1):
    a = math.log(Ethanol_DF.iloc[i,1]/Ethanol_DF.iloc[i+1,1])
    log_return = np.append(log_return, a)

log_return = np.append(log_return, 0)

Ethanol_DF['log_rendement'] = log_return




# <codecell>

   # 2 - 1 = Volatilite implicite 

def implied_vol(option_obs, call_put, S, K, T, r):
    MAX_ITERATIONS = 100
    PRECISION = 1.0e-5
    
    sigma = 0.5
    for i in range(0, MAX_ITERATIONS):
        price = bs_price(call_put, S, K, T, r, sigma)
        vega = bs_vega(call_put, S, K, T, r, sigma)
        
        price = price
        diff = option_obs - price
        
        if (abs(diff) < PRECISION):
            return sigma
        sigma = sigma + diff/vega
        
    return sigma


n = sp.norm.pdf
N = sp.norm.cdf

def bs_price(cp_flag,S,K,T,r,v, q=0):
    d1 = (np.log(S/K)+(v*v/2.)*T)/(v*np.sqrt(T))
    d2 = d1-v*np.sqrt(T)
    if cp_flag == 'c':
        price = np.exp(-r*T) * (S*N(d1) - K*N(d2))
    else:
        price = K*np.exp(-r*T)*N(-d2)-S*np.exp(-q*T)*N(-d1)
    return price




def bs_vega(cp_flag,S,K,T,r,v):
    d1 = (np.log(S/K)+(r+v*v/2.)*T)/(v*np.sqrt(T))
    return S * np.sqrt(T)*n(d1)


## Corn

F_corn = np.array([3.65, 3.70, 3.75, 3.8, 3.85])
c_corn = np.array([0.171, 0.130, 0.092, 0.063, 0.041])
k_corn = 3.825    
call_put = 'call'
T = 1/12
r = 0.05

corn_sigma = []

for i in range(0, len(F_corn)) :
    corn_sigma = np.append(corn_sigma, implied_vol(c_corn[i], call_put, F_corn[i], k_corn, T, r))


corn_sigma = np.mean(corn_sigma)  

print('')
print('La volatilite implicite du mais est : {:.2f}'.format(corn_sigma))   

## Ethanol

F_ethanol = np.array([1.25, 1.3, 1.35, 1.4, 1.45])
c_ethanol = np.array([0.104, 0.063, 0.033, 0.014, 0.005])
k_ethanol = 1.35

ethanol_sigma = []

for i in range(0, len(F_ethanol)) :
    ethanol_sigma = np.append(ethanol_sigma, implied_vol(c_ethanol[i], call_put, F_ethanol[i], k_ethanol, T, r))


ethanol_sigma = np.mean(ethanol_sigma)

print('La volatilite implicite de lethanol est : {:.2f}'.format(ethanol_sigma))  

# <codecell>

  ## question 2-2

std_mais = np.std(Corn_DF.iloc[0:-1, 6]) * np.sqrt(252)
std_ethanol = np.std(Ethanol_DF.iloc[0:-1, 6]) * np.sqrt(252)

print('la volatilite historique du mais est : {:.2f}'.format(std_mais))
print('La volatilite historique de l ethanolest : {:.2f}'.format(std_ethanol))

# <codecell>

corrcoeff = np.corrcoef(Corn_DF.iloc[0 : -1, 6].values, Ethanol_DF.iloc[0 : -1, 6].values)[0,1]

# division de lechantillon

corn_ap, corn_av= Corn_DF.iloc[0 : int((len(Corn_DF))/2), :], Corn_DF.iloc[int((len(Corn_DF))/2) :, :]
ethanol_ap, ethanol_av= Ethanol_DF.iloc[0 : int((len(Ethanol_DF))/2), :], Ethanol_DF.iloc[int((len(Ethanol_DF))/2) :, :]


corrcoeff_ap = np.corrcoef(corn_ap.iloc[:, 6].values, ethanol_ap.iloc[:, 6].values)[0,1]
corrcoeff_av = np.corrcoef(corn_av.iloc[0:-1, 6].values, ethanol_av.iloc[0:-1, 6].values)[0,1]

print('')
print('La coefficient de correlation entre le mais et l ethanol est : {:.2f}'.format(corrcoeff))
print('La coefficient de correlation entre le mais et l ethanol sur la premiere partie de l echantillon est : {:.2f}'.format(corrcoeff_ap))
print('La coefficient de correlation entre le mais et l ethanol sur la deuxieme partie de l echantillon est : {:.2f}'.format(corrcoeff_av))



# <codecell>

# 1 = mais        (std_mais (hist) / corn_sigma (implicite))
# 2 = Ethanol     (std_ethanol / ethanol_sigma)
# x = ethanol
# y = mais
# Volatilite implicite = corn_sigma et ethanol_sigma
# Volatilite historique = std_mais et std_ethanol

### C'est ici que l'on change la volatilite historique ou implicite

sigma_1 = std_mais
sigma_2 = std_ethanol
rho = corrcoeff

# Question 3 - 1

h = 3
p = 0.6
K = h*p
Y=3.8125
X=1.35*3
R=0.05

sigma_mais =sigma_2
sigma_ethanol = sigma_1
kho = corrcoeff
T = 1/12

def Firm_value(h,p,K,Y,X,R,sigma_mais, sigma_ethanol, kho) :

    sigma_x = sigma_mais
    sigma_y = sigma_ethanol
    Entreprise_value=0
    for i in range (1,121):
        A = Y*np.exp(R*T*i) + K
        B = (Y*np.exp(R*T*i))/A
        Sigma = np.sqrt(sigma_x**2+B**2*sigma_y**2-2*B*sigma_x*sigma_y*kho)
        d1 = (np.log(X/A)+ (R+((sigma_x**2) * 0.5)-B*sigma_x*sigma_y*kho+((B**2*sigma_y**2)*0.5))*T*i)/(Sigma*np.sqrt(T*i))
        d2 = (np.log(X/A)+ (R-((sigma_x**2) * 0.5)+sigma_x*sigma_y*kho+B**2*sigma_y**2*0.5-B*sigma_y**2)*T*i)/(Sigma*np.sqrt(T*i))
        d3 = (np.log(X/A)+(R-sigma_x**2*0.5+B**2*sigma_y**2*0.5)*(T*i))/ (Sigma*np.sqrt(T*i))
        Call = X*N(d1) - Y*N(d2) - K*np.exp(-R*T*i)*N(d3)
        Call = Call * 1000000
        if Call > 0 :
            Entreprise_value = Entreprise_value + Call
        
    return Entreprise_value / 1000000

PV__ = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)

print('La valeur de lentreprise : {:.2f}'.format(PV__))

# Question 3 - 2

vector_vol = np.linspace(0, 1, 101)
value_mais = []
value_ethanol = []
value_corrcoeff = []

for i in vector_vol :
    value_mais = np.append(value_mais, Firm_value(h,p,K,Y,X,R,i, sigma_ethanol, kho))
    value_ethanol = np.append(value_ethanol, Firm_value(h,p,K,Y,X,R,sigma_mais, i, kho))
    value_corrcoeff = np.append(value_corrcoeff, Firm_value(h,p,K,Y,X,R,sigma_mais, sigma_ethanol, i))
 
df=pd.DataFrame({'x': vector_vol, 'y1': value_mais, 'y2': value_ethanol, 'y3': value_corrcoeff})

# multiple line plot
plt.plot( 'x', 'y1', data=df, marker='',color='grey', linewidth=2, label = 'Mais')
plt.plot( 'x', 'y2', data=df, marker='', color='black', linewidth=2, label = 'Ethanol')
plt.plot( 'x', 'y3', data=df, marker='', color='green', linewidth=2, label="Coefficient de correlation")
plt.title("Variation de la valeur de l'entreprise en fonction des volatilite")
plt.xlabel('Volatilite')
plt.ylabel("Valeur de l'entreprise")
plt.legend()
plt.savefig("Variation de la valeur de l'entreprise en fonction des volatilite")


# <codecell>

# Question 4


t = 1
r = 0.05

y1 = 0
y2 = 0

u1 = np.exp(1.1 * sigma_1 * np.sqrt(t))
u2 = np.exp(1.1 * sigma_2 * np.sqrt(t))

d1 = np.exp(-(1.1 * sigma_1 * np.sqrt(t)))
d2 = np.exp(-(1.1 * sigma_2 * np.sqrt(t)))

M1 = np.exp((r - y1) * (t))
M2 = np.exp((r - y2) * (t))

V1 = M1**2 * (np.exp(sigma_1**2 * t) - 1)
V2 = M2**2 * (np.exp(sigma_2**2 * t) - 1)

R = M1 * M2 * np.exp(rho * sigma_1 * sigma_2 * t)

f1 = ((V1 + M1**2 - M1) * u1 - (M1 - 1)) / ((u1-1)*(u1**2 - 1))
f2 = ((V2 + M2**2 - M2) * u2 - (M2 - 1)) / ((u2-1)*(u2**2 - 1))

g1 = (u1**2 * (V1 + M1**2 - M1) - u1**3 * (M1 - 1)) / ((u1-1)*(u1**2 - 1))
g2 = (u2**2 * (V2 + M2**2 - M2) - u2**3 * (M2 - 1)) / ((u2-1)*(u2**2 - 1))


## Probabilite

p1 = (u1*u2*(R-1) - f1 * (u1**2 - 1) - f2 * (u2**2 - 1) + (f1 + f2)*(u1*u2-1)) / ((u1**2 - 1) * (u2**2 - 1))
p2 = (f1*(u1**2 - 1)*u2**2 + f2 * (u2**2 - 1) - (f1 + g2) * (u1*u2 - 1) - u1 * u2 * (R - 1)) / ((u1**2 - 1) * (u2**2 - 1))
p3 = (u1 * u2 * (R - 1) - f1 * (u1**2 - 1) * u2**2 + g2 * (u2**2 - 1) * u1**2 + (f1 + g2) * (u1*u2 - u2**2)) / ((u1**2 - 1) * (u2**2 - 1))
p4 = (f1 * (u1**2 - 1) + f2 * (u2**2 - 1)*u1**2 - (f1 + g2)*(u1 * u2 - 1) - u1 * u2*(R-1)) / ((u1**2 - 1) * (u2**2 - 1))
p5 = 1 - p1 - p2 - p3 - p4


n=5
I = 100
T = 1



###############################################################################
    

def arbre_price_pentanomial(PV, m1,m2,m3,m4, n) :
    s = (n*2+1, n*2+1)
    arbre = np.zeros(s)
    arbre[n, n] = PV
    for i in range (1, n+1) :
        arbre[n+i, n+i] = PV * m2**i
        arbre[n-i, n+i] = PV * m1**i
        for j in range (1, n-i+1) :
            arbre[n+j-i, n+j+i] = arbre[n+j-i-1, n+j+i-1] * m2
    for i in range (1, n+1) :
        arbre[n-i, n-i] = PV * m2 ** i
        arbre[n-i, n+i] = PV * m1 ** i
        for j in range (1, n-i+1) :
            arbre[n-j-i, n-j+i] = arbre[n-j-i+1, n-j+i+1] * m4
    for i in range (1, n+1) :
        arbre[n-i, n-i] = PV * m4**i
        arbre[n+i, n-i] = PV * m3**i
        for j in range (1, n-i+1) :
            arbre[n+j-i, n-j-i] = arbre[n+j-i-1, n-j-i+1] * m3
    for i in range (1, n+1) :
        for j in range (1, n-i+1) :
            arbre[n+j+i, n-j+i] = arbre[n+j+i-1, n-j+i+1] * m3
    return arbre


####
    
arbre_mais = arbre_price_pentanomial(3.8125, u1, u1, d1, d1, n)
arbre_ethanol = arbre_price_pentanomial(1.35*3, u2, d2, d2, u2, n)



A = round(pd.DataFrame(arbre_mais), 2)
B = round(pd.DataFrame(arbre_ethanol), 2)
Prix_commod = A.astype('str') +' - '+ B.astype('str')




###############################################################################



def arbre_value_pentanomial(arbre_mais, arbre_ethanol, n, T) :
    s = (n*2+1, n*2+1)
    arbre = np.zeros(s)
    arbre[n, n] = PV__
    for i in range (1, n+1) :
        Y = arbre_mais[n+i, n+i]
        X = arbre_ethanol[n+i, n+i]
        arbre[n+i, n+i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
        Y = arbre_mais[n-i, n+i]
        X = arbre_ethanol[n-i, n+i]
        arbre[n-i, n+i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
        for j in range (1, n-i+1) :
            Y = arbre_mais[n+j-i, n+j+i]
            X = arbre_ethanol[n+j-i, n+j+i]
            arbre[n+j-i, n+j+i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
    for i in range (1, n+1) :
        Y = arbre_mais[n-i, n-i]
        X = arbre_ethanol[n-i, n-i]
        arbre[n-i, n-i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
        Y = arbre_mais[n-i, n+i]
        X = arbre_ethanol[n-i, n+i]
        arbre[n-i, n+i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
        for j in range (1, n-i+1) :
            Y = arbre_mais[n-j-i, n-j+i]
            X = arbre_ethanol[n-j-i, n-j+i]
            arbre[n-j-i, n-j+i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
    for i in range (1, n+1) :
        Y = arbre_mais[n-i, n-i]
        X = arbre_ethanol[n-i, n-i]
        arbre[n-i, n-i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
        Y = arbre_mais[n+i, n-i]
        X = arbre_ethanol[n+i, n-i]
        arbre[n+i, n-i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
        for j in range (1, n-i+1) :
            Y = arbre_mais[n+j-i, n-j-i]
            X = arbre_ethanol[n+j-i, n-j-i]
            arbre[n+j-i, n-j-i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
    for i in range (1, n+1) :
        for j in range (1, n-i+1) :
            Y = arbre_mais[n+j+i, n-j+i]
            X = arbre_ethanol[n+j+i, n-j+i]
            arbre[n+j+i, n-j+i] = Firm_value(h,p,K,Y,X,R, sigma_mais, sigma_ethanol, kho)
    return arbre



###############################################################################
    

h = 3
p = 0.6
K = h*p
Y=3.8125
X=1.35*3
R=0.05

sigma_x =std_ethanol
sigma_y= std_mais
kho = corrcoeff
T = 1/12

arbre_value = arbre_value_pentanomial(arbre_mais, arbre_ethanol, n, 1/12) 

###############################################################################

def call_option_pentanomial(arbre, n, I, r, T) :

    option = arbre.copy()
    option[:, :] = np.maximum(arbre[:, :] - I, 0)

    
    for i in range (1,n) :
        for j in range (0, n+1-i) :
                option[i + j*2, i] = np.maximum(np.maximum((p1 * option[i + j*2 - 1, i + 1] + p2 * option[i + j*2 + 1, i + 1] + p3 * option[i + j*2 + 1, i - 1] + p4 * option[i + j*2 - 1, i-1] + p5 * option[i + j*2, i])/(1+r)**T, arbre[i + j*2, i] - I),0)
                option[i + j*2, n*2-i] = np.maximum(np.maximum((p1 * option[i + j*2 - 1, n*2-i + 1] + p2 * option[i + j*2 + 1, n*2-i + 1] + p3 * option[i + j*2 + 1, n*2-i - 1] + p4 * option[i + j*2 - 1, n*2-i - 1] + p5 * option[i + j*2, n*2 - i])/(1+r)**T, arbre[i + j*2, n*2-i] - I), 0)
                option[i, i + j*2] = np.maximum(np.maximum((p1 * option[i - 1, i + j*2 + 1] + p2 * option[i + 1, i + j*2 + 1] + p3 * option[i + 1, i + j*2 - 1] + p4 * option[i - 1, i + j*2 - 1] + p5 * option[i, i + j*2])/(1+r)**T, arbre[i, i + j*2] - I), 0)
                option[n*2-i, i + j*2] = np.maximum(np.maximum((p1 * option[n*2-i-1, i + j*2+1] + p2 * option[n*2-i + 1, i + j*2 + 1] + p3 * option[n*2-i + 1, i + j*2 - 1] + p4 * option[n*2-i - 1, i + j*2 - 1] + p5 * option[n*2-i, i + j*2])/(1+r)**T, arbre[n*2-i, i + j*2] - I), 0)
    
    option[n,n] = p1 * option[n-1,n+1] + p2 * option[n+1,n+1] + p3 * option[n+1,n-1]  + p4 * option[n-1,n-1] + p5 * option[n,n]
    
    return option

option = call_option_pentanomial(arbre_value, n, 100, r, 1)

print("La valeur du projet en considerant l'option réelle est : {:.2f} millions de dollars".format(option[n,n]))
print("La valeur du projet avec l'approche VAN trditionnelle est : {:.2f} millions de dollars".format(PV__))
print("La valeur ajoutée par l'option est donc de {:.2f} millions de dollars".format(option[n,n] - PV__))
print("La VAN du projet est {:.2f} millions de dollars".format(arbre_value[n,n]-I))

#######################################################################################
#######################################################################################

# Représentation de la frontière d'exercice 


arbre_exercice = pd.DataFrame(np.zeros([n*2+1, n*2+1]))
for i in range(0, n*2+1):
    for j in range (0, n*2+1) :
        if arbre_value[i,j] == 0:
            arbre_exercice.iloc[i,j] = ''
        elif option[i, j] <= arbre_value[i,j] - I :
            arbre_exercice.iloc[i,j] = 'oui'
        elif option[i, j] > arbre_value[i,j] - I :
            arbre_exercice.iloc[i,j] = 'non'