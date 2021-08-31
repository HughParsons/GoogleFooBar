def generate(numbers):
    if len(numbers) == 1:
        return numbers
    ans = [] + numbers
    for i in range(len(numbers)-1):
        for num in generate(numbers[i+1:]):
            ans.append(numbers[i]*num)

    return ans

def reformat(number):
    primes = [2,3,5,7,11]
    ans = []
    for i in range(5):
        if not number % primes[i]:
            ans.append(i)
            number /= primes[i]
    return ans

def findMin(a1, a2):
    for i in range(len(a1)):
        if a2[i] < a1[i]:
            return a2
    return a1

def solution(times, times_limit):
    """
    Method:
    
        construct an adjacency list of the form:
        
        position_i: {
            state_0 : [transitions], predicesor, cost
            state_1 : 
        }
        
        each bunny is assigned a prime number from [2,3,5,7,11] while the initial position is given 1
        the final position will be assigned 4 for now.
        
        each state at each position is the product of the bunnies currently held by the target, P(b)
        thus a transition is pos_old[state_old] -> pos_new[state_old*new if state_old % new]
        
        we adjust the above behaviour if we are at the bulkhead/ final position (-1 might work + negative indexing)
        
        This will mean that we arrive at a graph with 2**(n-1) + (n-2)*2**(n-3) states, or an O(2**n) space
        complexity?
        
        Since there may be negative weights we can't use dijkstras - will try Bellman-Ford
        Assuming that we have a complete graph/digraph if there is a negative cycle then we return [1,2,3,4,5]
        ^ (haven't checked validity)
        
        Adhering to the minimum indexing output should be possible based on the prime factors then reformatting
        since the number of states increases, time complexity will also be around O(2**n) (or 4**n?)

    special thanks to Nujabes
    """
    n = len(times)

    positions = [1,2,3,5,7,11][:n-1] + [-1]
    states = [1] + sorted(generate(positions[1:-1]))
    indices = {positions[i]: i for i in range(n)}
    # generating adjacency list
    d= {}
    for n in states:
        for i in positions[:-1]:
            if  not n % i:
                d[(i,n)] = [[(pos, pos*n) if n % pos else (pos, n) for pos in positions[:-1] if pos != i] + [(-1,-n)], float('inf'), None]
        d[(-1,-n)] = [[(pos, n*pos) if n % pos else (pos, n) for pos in positions[:-1]], float('inf'), None]
    
    

    # setting source distance to 0
    d[(1,1)][1] = 0

    # for k in d:
    #     for l in d[k]:
    #         print(f"{l}:\t{d[k][l]}")
    #     print("\n\n")

    # Bellman-Ford time???
    reps = len(d)
    while reps:
        for v in d:
            for transition in d[v][0]:
                if d[transition][1] > d[v][1] + times[indices[v[0]]][indices[transition[0]]]:
                    d[transition][1] = d[v][1] + times[indices[v[0]]][indices[transition[0]]]
                    d[transition][2] = v
                    

        reps-=1
    for v in d:
        for transition in d[v][0]:
            if d[transition][1] > d[v][1] + times[indices[v[0]]][indices[transition[0]]]: return [0,1,2,3,4][:n-2]

    # q = [(1,1)]
    # negative_cycle = False
    # while q:
    #     current = q.pop(0)
    #     for transition in d[current][0]:
    #         if d[transition][1] > d[current][1] + times[indices[current[0]]][indices[transition[0]]]:
    #             d[transition][1] = d[current][1] + times[indices[current[0]]][indices[transition[0]]]
    #             d[transition][2] = current
    #             q.append(transition)
            
    # TODO: add negative cycle detection

    # for k in d:
    #     for l in d[k]:
    #         print(f"{l}:\t{d[k][l]}")
    #     print("\n\n")

    ans = []
    for k in d:
        if k[0] != -1: 
            continue
        if d[k][1] <= times_limit and len(reformat(k[1])) >= len(ans):
            t = reformat(k[1])
            # print(t, ans)
            if len(t) == len(ans) and len(ans):
                ans = findMin(ans, t)
            else:
                ans = t

    return ans
    



if __name__ == "__main__":
    # print(sorted(generate([2,3,5,7,11])))
    print(solution([
        [0,2,2,2,-1],
        [9,0,2,2,-1],
        [9,3,0,2,-1],
        [9,3,2,0,-1],
        [9,3,2,2,0]], 1))

    print(solution([
        [0,1,1,1,1],
        [1,0,1,1,1],
        [1,1,0,1,1],
        [1,1,1,0,1],
        [1,1,1,1,0]], 4))
    
    print(solution([
        [0,1,1,1,1,1],
        [1,0,1,1,1,1],
        [1,1,0,1,1,1],
        [1,1,1,0,1,1],
        [1,1,1,1,0,1],
        [1,1,1,1,1,0]], 3))
    
    print(solution([
        [0, 1, 1, 1, 1, -3],
        [4, 0, 1, 1, 6, 6],
        [6, 4, 0, 6, -2, 9],
        [7, 5, 2, 0, 6, 9],
        [7, 7, 4, 4, 0, 1],
        [7, 6, -1, 6, 7, 0]], 4))
    # print(solution([
    #     [1,1,1,1,1,1,1],
    #     [1,1,1,1,1,1,1],
    #     [1,1,1,1,1,1,1],
    #     [1,1,1,1,1,1,1],
    #     [1,1,1,1,1,1,1],
    #     [1,1,1,1,1,1,1],
    #     [1,1,1,1,1,1,1]
    # ],1))
    pass