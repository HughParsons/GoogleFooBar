

def generate(numbers, k):
    """
    Generates combinations of numbers C k, preserves order.
    """
    if k == 1: return [[num] for num in numbers]

    # looping through each number and generating combinations from itself 
    # and the following numbers (preserving order)
    ans = []
    for i in range(len(numbers)-k+1):
        for number in generate(numbers[i+1:],k-1):
            ans.append([numbers[i]] + number)

    return ans
    

def solution(num_buns, num_required):
    """
    Description:
        Given some number of bunnies between 1 and 9, and a minimum required number of bunnies, 
        between 0 and 9 (both inclusive), to open all of the locks, return the distribution of 
        some number of keys in the smallest lexicographical order, such that no fewer than 
        num_required bunnies may open the locks.

    Interpretation:
        Initially I misinterpreted this problem, assuming that each bunny could only turn one key,
        as the problem states that they must be turned simulatneously, and I could not view all the
        test cases at that time. However, this turned out to be false, and instead the problem focuses
        on finding the minimum number of keys, K, such that we can generate (num_buns) sets of keys, with
        only the union of any num_required sets forming the set {0,1,...,K}.

        A few simple deductions can be made:

            1.  By the pigeonhole principle, we must have at least 
                (num_buns - num_required + 1) occurences of each key, 
                otherwise we could chose some num-required bunnies
                without said key.

            2.  In turn, this means that for each key we are choosing
                (num_buns - num_required + 1) bunnies to allocate that
                key, thus K = num_buns C (num_buns - num_required + 1),
                where C represents the binomial coefficient.

            3.  The constraint on lexicographical order means that we
                must generate these groups from smallest to largest.

    Method:
        Deduction 2 under the interpretation section allows us to drastically simplify
        the complexity of our problem to simply generating every combination of
        num_buns C (num_buns - num_required + 1) in lexicographical order, then 
        assigning an index/key to each of these combinations.

        For example, consider 5 C (5 - 3 + 1), (5 choose 3), where we generate the
        following combinations:
            [
                [0, 1, 2], [0, 1, 3], [0, 1, 4], [0, 2, 3], [0, 2, 4], [0, 3, 4], 
                [1, 2, 3], [1, 2, 4], [1, 3, 4], 
                [2, 3, 4]
            ]
        These represent, as ordered sets, every possible choice of 3 numbers from 
        {0, 1, 2, 3, 4}.

        Under the constraint on the number of occurinces for each key, we can assign
        each of the sets their assosciated index in the output array, and because these
        sets are in minimum lexicographical order, so to is our assignment of the keys.

        Thus we simply call generate(numbers, maximum_to_choose) on the sorted list of
        numbers, and then repeat the key assignment process above. The combinations are
        generated using recursion under the assumption that the input array is sorted.


    Complexity Analysis:
        Let n = num_buns, and k = num_required

        Im not too confident with complexity analysis, especially for recursion, but
        we make on the order of k calls, thus arriving at a simple estimate of O(n^k).
    """
    # generating a dict to avoid problems with pointers in multidimensional array generation
    # if you have a fix for this other than using range() multiple times please let me know.
    ans = {i:[] for i in range(num_buns)}

    # generating all combinations and assigning each key
    combinations = generate([i for i in range(num_buns)], num_buns - num_required + 1)
    for i in range(len(combinations)):
        for n in combinations[i]:
            ans[n].append(i)

    # reformatting
    return [ans[l] for l in ans]
