

def generate(numbers, k):
    if k == 1: return [[num] for num in numbers]
    ans = []
    for i in range(len(numbers)-k+1):
        for number in generate(numbers[i+1:],k-1):
            ans.append([numbers[i]] + number)
    return ans
    

def solution(num_buns, num_required):
    """
        return the lexicographically smallest description of the keys 
        for each bunny such that any num_required bunnies will be
        able to open the lock
        
        we dont know which combination of keys is required
        so every combination must be producible using any 
        num_req bunnies??? - check this
        
        ^ as in no single bunnie can produce every combination?
        
        1 <= bunnies <= 9, 0 <= num_required <= 9?
        ^ check
        
        First thoughts:
            kind of looks like shamirs secret sharing in that 
            we are given n keys and m bunnies
            
            
            code packing?
            
            by pigeonhole, each key must be represented 
            num_bunnies - num_required + 1 times
            such that no num_required bunnies do not have a key
            
            num combinations is num_bun choose num_req?
            union(any num_required bunnies) == set(0,1...n)
         
        sol(n,0): []  
        sol(n,1): [[0]]*n
        sol(n,n): [[0],[1],...[n]]
        
        sol(3,2): [[0,1],[0,2],[1,2]]
        sol(3,3): [[0],[1],[2]]
        
        sol(4,2): 
        [[0,1,2],[0,1,3],[0,2,3],[1,2,3]]???
        
        sol(4,3):
        [[0,1],[0,2],[1,3],[2,3]]
        
        sol(a,b): general form? = ans[:a-b+1][0] = 0, ans[:a-b][1] = 1
        
        sol(5,3)
        [
            [0,1,2,3,4,5], = [012,013,014,023,024,034]
            [0,1,2,6,7,8], = [012,013,014,123,124,134]
            [0,3,4,6,7,9], = [012,023,024,123,124,234]
            [1,3,5,6,8,9], = [012,023,034,123,134,234]
            [2,4,5,7,8,9]
        ]
        one bunny can use multiple keys :(
        ^ but how can they turn them simultaneously??
        -- MAGIC BUNNIES
        
        we need some number of keys, K, such that K can be split
        between num_bunnies groups but only the union of ANY
        num_required will form the complete set {0,1,...,k}
        
        Observations:
            k(n, 0) = 0
            k(n, 1) = 1
            k(n, n) = n
            k(5, 3) = 10
            
        lol it's k(n, m) = n C (m-1) -- but why?
            any key in {0,1...k} must be repeated
            n+1 - k times (pigeonhole)
            but we have to have enough keys such that not
            fewer than m bunnies can unlock?
            ^ thus how many ways can we choose m-1 bunnies that 
              cannot unlock the doors
            then each bunny in this combination is assigned the
            index of that combination
                YESSSSSSSS!!!!!!!!!!!!!!
    012,013,014,023,024,034, 123,124,134, 234
    0,1,2,3,4
    """
    
    ans = {i:[] for i in range(num_buns)}

    combinations = generate([i for i in range(num_buns)], num_buns - num_required + 1)
    for i in range(len(combinations)):
        # print(combinations[i])
        for n in combinations[i]:
            ans[n].append(i)

    
    return [ans[l] for l in ans]

if __name__ == "__main__":
    # print(generate([0,1,2,3], ))
    print(solution(4, 0))