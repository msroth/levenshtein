# levenshtein
Calculate the Levenshtein Distance (LD) between two strings.

            The LD is the minimum numbers of edits (insert, delete, or
            substitute) to transform one string into another.
            The code calculates the LD and the minimum cost path (MCP)
            through the LD matrix.  The MCP dictates the step-by-step
            edits to make the transformation.  The code also shows the
            transformation of the source string into the target.
			
Same Output:

    Demonstrate computation of Levenshtein Distance (LD) between two words.
    Determine the minimum number of edits to transform source word into target word.
    For example, how many substitutions, insertions, or deletions are required to
    turn 'house' into 'home'?  (Answer: 2), or Democrat into Republican (Answer: 8).
    
    The default cost for all edit operations is 1.
    
    Debug:  0 = return only the LD
            1 = return LD plus distance, minimum path, and operations matrices
            2 = return all intermediate matrices and computations (i.e., lots of output
    
    Other fun examples:
      abc       -> xyz  LD: 3
      kitten    -> sitting  LD: 3
      intention -> execution  LD: 5
      manahaton -> manhattan  LD 3
      00101010  -> 110110  LD: 3
    
    Enter first word (source) [lawn]: republican
    Enter second word (target) [flaw]: democtrat
    Enter level of output (0, 1, 2) [1]:
    
    ***** FINAL RESULTS *****
    
    Final Distance Matrix:
       #  d  e  m  o  c  t  r  a  t
    # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    r [1, 1, 2, 3, 4, 5, 6, 6, 7, 8]
    e [2, 2, 1, 2, 3, 4, 5, 6, 7, 8]
    p [3, 3, 2, 2, 3, 4, 5, 6, 7, 8]
    u [4, 4, 3, 3, 3, 4, 5, 6, 7, 8]
    b [5, 5, 4, 4, 4, 4, 5, 6, 7, 8]
    l [6, 6, 5, 5, 5, 5, 5, 6, 7, 8]
    i [7, 7, 6, 6, 6, 6, 6, 6, 7, 8]
    c [8, 8, 7, 7, 7, 6, 7, 7, 7, 8]
    a [9, 9, 8, 8, 8, 7, 7, 8, 7, 8]
    n [10, 10, 9, 9, 9, 8, 8, 8, 8, 8]
    
    
    Minimum Path Matrix:
       #  d  e  m  o  c  t  r  a  t
    # [0,  ,  ,  ,  ,  ,  ,  ,  ,  ]
    r [ , 1,  ,  ,  ,  ,  ,  ,  ,  ]
    e [ ,  , 1,  ,  ,  ,  ,  ,  ,  ]
    p [ ,  , 2,  ,  ,  ,  ,  ,  ,  ]
    u [ ,  ,  , 3,  ,  ,  ,  ,  ,  ]
    b [ ,  ,  ,  , 4,  ,  ,  ,  ,  ]
    l [ ,  ,  ,  ,  , 5,  ,  ,  ,  ]
    i [ ,  ,  ,  ,  ,  , 6,  ,  ,  ]
    c [ ,  ,  ,  ,  ,  ,  , 7,  ,  ]
    a [ ,  ,  ,  ,  ,  ,  ,  , 7,  ]
    n [ ,  ,  ,  ,  ,  ,  ,  ,  , 8]
    
    
    Final Operations Matrix:
       #  d  e  m  o  c  t  r  a  t
    # [0,  ,  ,  ,  ,  ,  ,  ,  ,  ]
    r [ , S,  ,  ,  ,  ,  ,  ,  ,  ]
    e [ ,  , S,  ,  ,  ,  ,  ,  ,  ]
    p [ ,  , D,  ,  ,  ,  ,  ,  ,  ]
    u [ ,  ,  , S,  ,  ,  ,  ,  ,  ]
    b [ ,  ,  ,  , S,  ,  ,  ,  ,  ]
    l [ ,  ,  ,  ,  , S,  ,  ,  ,  ]
    i [ ,  ,  ,  ,  ,  , S,  ,  ,  ]
    c [ ,  ,  ,  ,  ,  ,  , S,  ,  ]
    a [ ,  ,  ,  ,  ,  ,  ,  , S,  ]
    n [ ,  ,  ,  ,  ,  ,  ,  ,  , S]
    
    
    Sequential Edits:
    republican
    depublican <- substitute 'd' pos: 0
    depublican <- substitute 'e' pos: 1
    deublican <- delete 'p' pos: 2
    demblican <- substitute 'm' pos: 2
    demolican <- substitute 'o' pos: 3
    democican <- substitute 'c' pos: 4
    democtcan <- substitute 't' pos: 5
    democtran <- substitute 'r' pos: 6
    democtran <- substitute 'a' pos: 7
    democtrat <- substitute 't' pos: 8
    
    Levenshtein Distance (LD) between 'republican' and 'democtrat' is: 8
    Levenshtein similarity ratio is: 0.3157894736842105
