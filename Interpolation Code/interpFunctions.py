"""

A series of generalized functions we've created for this project. Be sure that 
any fuctions you add are not dependent on variables not created or passed into
the function, or any prior code not in the function. -AM

"""

# A linear interpolation that can handle '-' as an input
def linearInterp(x, slope, yIntercept): 
    '''
    Parameters
    ----------
    x: float
        dependent varible
    slope : float
        First coeffient(for highest power term).
    yIntercept : float
        Last coeffient(for 0th power term).

    Returns
    -------
    y: float or string
        Returns linear estimation. Assigned as '-' if input is '-'.
    '''
    
    if x == '-': #Writes '-' if the mass is not applicable
        y = '-'   
        
    else:
        x = slope*float(x) + yIntercept # Lin Interp
        
    return y




def assignValue(df):
    """
    Needs to do:
        Take in some dataset(a Pandas dataframe), and a series of 
        parameters. Then run some function to take input data and turn it into
        new data. This then gets assigned to a given row and col in the 
        dataframe. Outputs the altered dataframe. 
    
    Ideas:
        1) Turn this into a 'for' loop that runs against some array instead
            of a generalized funtion.
        2) Since the use of a specialized function is required, maybe pass this
            into the function as a parameter instead.
        3) Alter input parameters such that instead of "a = 1, b = 2, ..." the
            parameters exist in an array that the specialized funtion can handle.
        4) To make using the input and out col. assignment easier, ideas 1 and 2
            can be combined. The for loops works along the various coloums while
            the function gets passed the paramets for the for loop, and then 
            assigns them using "df.iat[]."
            
    Notes: 
        This function currently depends on the output columns to have been 
        initialized prior to this funciton being ran. The issue with initializing
        these columns in the function is that they may have differing amounts 
        and names. Perhaps this could be fixed by another array input?
        
        Currently the function is heavily specialized, I inclued a partial
        sampe of what the code looked like from ti_interpolation.py (assignMass()). 
        To generalize this function would most definetly need a complete rewrite 
        of the code and the logic, and would possibly need an altercation of 
        any codes that this funtion may be end up using (Although I think it 
        should be avoidable).
        
        -AM
    """
    for x in range(len(df)):
        row = x
        
        ## Example of code from ti_interpolation.py
        a = hd_fit[0]
        b = hd_fit[1]

        HeMass = df.iat[row, 7] #WD 1 min
        df.iat[row, 11] = linearInterp(HeMass, a, b)

        HeMass = df.iat[row, 8] #WD 2 min
        df.iat[row, 12] = linearInterp(HeMass, a, b)

        HeMass = df.iat[row, 9] #WD 1 max
        df.iat[row, 13] = linearInterp(HeMass, a, b)
    
        HeMass = df.iat[row, 10] #WD 2 max
        df.iat[row, 14] = linearInterp(HeMass, a, b)   
                
    return df
