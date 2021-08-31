def generate(numbers):
    """Generates all possible products of the supplied numbers"""
    if len(numbers) == 1:
        return numbers
    
    # shallow copying to avoid any interference between the generated numbers and the utilised ones
    ans = [] + numbers
    for i in range(len(numbers)-1):
        for num in generate(numbers[i+1:]):
            ans.append(numbers[i]*num)

    return ans

def reformat(number):
    """Converts a product of the below primes into the assosciated index of the bunnies"""
    primes = [2,3,5,7,11]
    ans = []
    for i in range(5):
        if not number % primes[i]:
            ans.append(i)
            number /= primes[i]
    return ans

def findMin(a1, a2):
    """Returns the array with the lowest lexicographical order"""
    for i in range(len(a1)):
        if a2[i] < a1[i]:
            return a2
    return a1

def solution(times, times_limit):
    """
    Description:
        We are given 'times' locations with the 0th and nth locations representing the start 
        and the blockhead respectively. The intermediate locations are the zones where we can
        pick up a bunny from.

        Our goal is to pick up as many bunnies as possible within the time limit, if multiple
        solutions of the same order are possible then we favor the one with the lowest 
        lexicographical order.

        Negative cycles may be present.

    Interpretation:
        Although len(times) <= 7, i.e. there are at most 7 locations, we have to expand the 
        graph to include the state of our "hero", the individual carrying the bunnies, in order
        to preserve knowledge of which bunnies we are carrying at any given location.

        Instead of labeling each state as a pair of <location, list of currently held bunnies> we
        can instead assign each bunny a prime number, the start 1, and the bulkhead -1. This in turn
        allows for simplicity in generating transitions and ensures uniqueness under the fundamental 
        theorem of arithemitic.
    
    Method:
        1.  Generate the possible states as the product of the first len(times) - 2 primes.

        2.  Generate the dictionairy assosciating each prime with its index for use in indexing 'times'

        3.  Generate the adjacency list:

            a.  Loop through each state.

            b.  For each state loop through each of the primes, if a prime divides 
                that state, then the state may occur at the location assosciated
                with that prime (the state indicates we are carrying the bunny from
                that location).

            c.  Generate the edges by looping through the other poisitions and 
                multiplying the current state by the prime of that position 
                (equivalent to picking up a bunny), if it does not already divide 
                the current state - in which case we use the same state.
                
            d.  repeat steps b and c specifically for -1.


        4.  Due to the possible presence of negative cycles, Bellman-Ford is implemented 
            instead of Dijkstra's or a BFS. The current implementation has not been enhanced 
            to exit if no changes to the graph are made.

        5.  Reformat the output back into the assosciated indices for each bunny.

    Complexity Analysis (Unsure, please provide feedback):

        In the expansion of the graph we go from n initial locations to:

        -   2^(n-2) states for both the start and bulkhead.

        -   2^(n-3) states for each of the bunnies.

        with each location having at most n edges.

        Therefore, the space complexity for our adjacency list data structure 
        should be O(n*2^n).

        Finally, Bellman-Ford runs in O(|V||E|), which in the case of our expanded graph
        results in a time complexity of O(n*4^n).

    """
    n = len(times)

    positions = [1,2,3,5,7,11][:n-1] + [-1]
    states = [1] + sorted(generate(positions[1:-1]))
    indices = {positions[i]: i for i in range(n)}

    # generating adjacency list
    d= {}
    for state in states:
        for i in positions[:-1]:
            if not state % i:
                d[(i,state)] = [[(pos, pos*state) if state % pos else (pos, state) for pos in positions[:-1] if pos != i] + [(-1,-state)], float('inf'), None]
        d[(-1,-state)] = [[(pos, state*pos) if state % pos else (pos, state) for pos in positions[:-1]], float('inf'), None]
    
    
    ## Bellman-Ford Implementation (rudimentary)
    
    # setting source distance to 0
    d[(1,1)][1] = 0

    # We must examine each in the graph once for every node
    reps = len(d)
    while reps:
        for v in d:
            for transition in d[v][0]:
                if d[transition][1] > d[v][1] + times[indices[v[0]]][indices[transition[0]]]:
                    d[transition][1] = d[v][1] + times[indices[v[0]]][indices[transition[0]]]
                    d[transition][2] = v
                    
        reps-=1
    
    # checking for the presence of negative cycle
    for v in d:
        for transition in d[v][0]:
            if d[transition][1] > d[v][1] + times[indices[v[0]]][indices[transition[0]]]: return [0,1,2,3,4][:n-2]

    # finding the solution and reformatting the encoded values
    ans = []
    for k in d:
        if k[0] == -1 and d[k][1] <= times_limit and len(reformat(k[1])) >= len(ans):
            
            t = reformat(k[1])
            if len(t) == len(ans) and len(ans):
                ans = findMin(ans, t)
            else:
                ans = t

    return ans
    

