import pandas as pd
import numpy as np


def df_to_Boolean(df, RowCol, FactorCol):
    # Loads a csv with two columns into a 
    # Used to Generate User-Permissions Matrix & User-Roles Matrix

    # If String - use as filepath
    if isinstance(df,str):
        df = pd.read_csv(df)

    factors = [RowCol,FactorCol]
    df = df[factors]
    df = df.drop_duplicates()
    df.fillna('Unknown',inplace=True)

    df = df.assign(value = 1).set_index(factors)
    df = df.reindex(pd.MultiIndex.from_product(df.index.levels, names=df.index.names))

    df = (df.assign(value=df['value'].fillna(0).astype(int))
            .groupby(level=0).apply(lambda x: x.ffill().bfill())
            .reset_index())

    df = df.pivot(index=RowCol,columns=FactorCol, values = 'value')
    return df

def FastMiner(UP):
    
# Remove Empty sets/no permission users
    UP = np.unique(np.array(UP), axis=0).tolist()
    UP = [x for x in UP if x != [0] * len(x)]

    # Initialize lists
    InitRoles = []
    GenRoles = []
    OrigCount = []
    GenCount = []
    Contributors = []

    for user in UP:

        if sum([user == x for x in InitRoles]) == 0:
            OrigCount.append(1)
            InitRoles.append(user)
        else:
            pos = [i for i, x in enumerate([user == x for x in InitRoles]) if x][0]
            OrigCount[pos] += 1

    InitRoles_iter = InitRoles
    
    for InitRole in InitRoles_iter:

        #Remove role from InitRoles
        #InitRoles_iter = [x for x in InitRoles if x != InitRole]

        for CandRole in InitRoles_iter:
            # New Role = InitRole ∩ CandRole (intersect Init Role with remaining roles)
            #NewRole = [x for x in CandRole if x == InitRole]

            NewRole = np.logical_and(list(map(bool,CandRole)),list(map(bool,InitRole))).astype(np.int).tolist()

            if sum([NewRole == x for x in GenRoles]) == 0:
                GenCount.append(
                    OrigCount[[i for i, x in enumerate([InitRole == x for x in InitRoles]) if x][0]]
                     + OrigCount[[i for i, x in enumerate([CandRole == x for x in InitRoles]) if x][0]]
                )

                Contributors.append([CandRole, InitRole])
                GenRoles.append(NewRole)
                
    return np.array(GenRoles)



def Basic_RMP(UP,CandRoles, MaxRoles = 100):
    cols = UP.columns
    UP = np.array(UP)
    Constraints = np.ones([UP.shape[1],CandRoles.shape[0]], dtype=int)
    OptRoles = []
    iters = 0
    UP_Remain = UP.copy()
    EntitlementCount = []
    
    for i in range(CandRoles.shape[0]):
        for j in range(UP_Remain.shape[0]):
        # Boolean logic: We check to see if Candidate Role is fully in the User 
        # This can be modeled by all elements of the subtraction being less than 1   
            Constraints[j,i] = (CandRoles[i,:] - UP_Remain[j,:] < 1).all()
    
    while len(OptRoles) < MaxRoles and iters < MaxRoles and np.sum(UP_Remain) > 0:
        #print(np.sum(UP_Remain))
        # Determine the Constraints that can be set to zero
        # TODO: Rewrite more Pythonic using list comp
        #       Update Basic Key algorithm to not recalc 0 for columns removed
        iters += 1
        
        # Calculate Basic Keys
        BasicKeys = []
        i = 0
        for Keys in Constraints.T:
            count = 0
            
            for C in range(UP_Remain.shape[0]):
                count += Keys[C] * np.sum(np.logical_and(CandRoles[i,:],UP_Remain[C,:])) * (CandRoles[i,:] - UP[C,:] < 1).all()
            BasicKeys.append(count)
            i += 1

        # Add Role with highest Basic Key to OptRoles
        # Break ties by picking with lowest index
        BestRole = CandRoles[np.argmax(BasicKeys)]
        OptRoles.append(BestRole)

        # Delete Constraints from User Permissions
        for i in range(UP_Remain.shape[0]):
            if (UP[i,:] - BestRole > -1).all():
                UP_Remain[i,:] = UP_Remain[i,:] - BestRole
                
                # Map negative numbers to zero (these represent roles captured more than once, which is ok)
                UP_Remain[i,:][UP_Remain[i,:] < 0] = 0
                
        # Set Constraints in Best Role to zero
        Constraints[:,np.argmax(BasicKeys)] = 0
        EntitlementCount.append(sum(BestRole))

    # return New Rules as DF
    OptRoles = pd.DataFrame(data = OptRoles, columns = cols)

    return OptRoles, EntitlementCount