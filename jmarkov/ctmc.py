import numpy as np
from scipy import linalg
from scipy import sparse
from .markov_chain import markov_chain

class ctmc(markov_chain):

    # number of states in string array form
    n_states:int=1

    # states in string array form
    states:np.array = np.array([1])

    # generator matrix as 2d numpy array
    generator:np.array
    
    # empty initializer 
    # chain with a single state
    def __init__(self):
        self.n_states = 1
        self.generator = np.array([0])

    def __init__(self,n:int):
        self.n_states = n
        self.generator = np.eye(2, dtype=float)

    # initializer with a transition matrix
    def __init__(self,generator:np.array):
        if not self._check_generator_matrix(generator):#Lets check if transition matrix is logical (i.e the rows sum 0)
            raise ValueError("the rows of transition matrix do not sum 0 or the diagonal has non negative values")
        self.n_states=generator.shape[0]
        self.generator = generator
    def _check_generator_matrix(self,M:np.ndarray):
        #Check if a given transition matrix has the condition that for every row the sum of all elements is equal to 0
        vector = np.isclose(np.sum(M, axis = 1),0,1e-5) == True
        # Check if a given transition matrix has all diagonal elements non positive
        if vector.all() and np.all(np.diag(M)<0):
            return True
        else:
            return False


    def steady_state(self):
        # computes the steady state distribution
        if self.generator.any():
            # sets A to be Q and replace first column with ones for the normalizing equation
            A = self.generator.copy()
            A[:, 0] =  1
            # sets b as the right hand vector with a 1 for the normalizing equation
            b = np.zeros(self.n_states, dtype=float)
            b[0] = 1
            # solves transposed system as pi is a row vector
            res = linalg.solve(A,b,transposed=True)
            return res
        else:    
            print("Empty generator matrix")
        return 0
    def transient_probabilities(self,t:float,alpha:np.ndarray):
        shape=alpha.shape#lets get the shape of alpha vector
        if shape[0]!=self.n_states:
            raise ValueError("The dimensions of alpha vector are incorrect. It must be a vector 1xn_states")
        P=linalg.expm(self.generator*t)#exponentiate the diferential generator following the method of Mohy et al (https://eprints.maths.manchester.ac.uk/1300/1/alhi09a.pdf)
        probas=alpha@P
        return probas


    def first_passage_time(self, target:str):
        #The transition matrix and the number of states are brought
        e=self.n_states 
        q=self.transition_matrix.copy()
        
        # Matrix of ones with n-1 rows is created
        u=np.full([e-1,1],1)

        #The column and row corresponding to the target state are eliminated from the transition matrix 
        m=np.delete(q,target, axis=0)
        m=np.delete(m,target, axis=1)


        t=np.matmul(np.linalg.inv(-m),u)
        return t

    def occupation_time(self, nsteps:int):
        #TODO computes the expected occupation time matrix in nsteps steps
        print("TODO")
        return 0

    def is_ergodic(self):
        # the finite case: we check if the chain is irreducible
        Q = np.copy(self.generator)
        np.fill_diagonal(Q,0)
        if sparse.csgraph.connected_components(Q, directed=True,connection='strong',return_labels=False)==1:
            return True
        else:
            return False