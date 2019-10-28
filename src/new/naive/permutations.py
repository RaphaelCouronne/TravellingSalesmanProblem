

# def Liste_Permutees(n):
#     """ retourne les permutations"""
#     verbose = False
#     if verbose:
#         print("--> entre dans permut n={0}".format(n))
#     if n == 2:
#         if verbose:
#             print("<-- sortie de permut n={0}, p={1}".format(n, [[0]]))
#         return [[0]]
#     else:
#         Liste_Temp = []
#         prec = Liste_Permutees(n - 1)
#         for L in prec:  # on le fait par récursivité !!!
#             for k in range(n - 2):
#                 Liste_L = L.copy()  # pour le pas modifier la liste L
#                 Liste_L.insert(k, n - 2)    # on insère en place k l'entier n
#                 Liste_Temp.append(Liste_L)  # on met en mémoire
#             Liste_Temp.append(L + [n - 2])  # on rajoute la liste où n est en dernière position
#         if verbose:
#             print("<-- sortie de permut n={0}, p={1}".format(n, Liste_Temp))
#         return Liste_Temp
#
