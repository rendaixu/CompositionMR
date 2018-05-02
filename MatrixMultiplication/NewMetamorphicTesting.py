import sys
import itertools
import MatrixMultiplication.MatMrs as matmrs
import MatrixMultiplication.matrixmultiplication as spm
import MatrixMultiplication.TestCases as ts
import math
import Library.Log as logger

def pickup(num, mrs):
    cmr_list = []
    for i in range(num):
        for candidates in itertools.combinations(mrs, i+1):
            cmr_list.append(matmrs.MRComposition(list(candidates)))
    return cmr_list

def AssertMRViolation(ftc_output, ftc_expected_output, message):
    d = 0.00001
    row = len(ftc_expected_output)
    col = len(ftc_expected_output[0])
    if not (row == len(ftc_output) and col == len(ftc_output[0])):
        return True
    for i in range(row):
        for j in range(col):
            if math.fabs(ftc_output[i][j] - ftc_expected_output[i][j]) >= d:
                return True
    return False

def TestOneMR(mr, testcases, mutanted_versions):
    #print(mr.getMessage())
    killed_mutants= []
    for mutant_index in mutanted_versions:
        #print(mutant_index)
        matmultiple = spm.MatrixMultiple(mutant_index)
        for (otc_A, otc_B) in testcases:
            otc_output = matmultiple.MatMul(otc_A, otc_B)
            (ftc_expected_output, ftc_A, ftc_B,matmultiple.MatMul) = mr.getExpectedFTCOutput(otc_output, otc_A, otc_B,matmultiple.MatMul)
            ftc_output = matmultiple.MatMul(ftc_A, ftc_B)
            violation = AssertMRViolation(ftc_output, ftc_expected_output, mr.getMessage())
            if violation:
                killed_mutants.append(mutant_index)
    return killed_mutants


"""Calculate the mutation score of a MR and a set of test cases"""
def mutation_score(killed_mutants, mutants):
    return float(len(killed_mutants)) / float(len(mutants))


def getSMRList(name_list):
    smr_list = []
    for mr_name in name_list:
        smr_list.append(matmrs.MRFactor(mr_name))
    return smr_list

""" Assess the efficiency of compounded of num of MRs."""
def TestAllCMRs(num):
    mrs = getSMRList([ "MR1","MR2","MR3", "MR4", "MR5", "MR6","MR7", "MR8", "MR9"])
    #mrs = getSMRList([ "MR1"])
    mutants = ["MU_9_SparseMatMul", "MU_2_SparseMatMul", "MU_3_SparseMatMul",
               "MU_4_SparseMatMul", "MU_5_SparseMatMul", "MU_6_SparseMatMul",
               "MU_7_SparseMatMul", "MU_8_SparseMatMul"] # this faults can lead to the crash of the program. The crash could be caused by my mistake.
    mutants = ["MU_1_SparseMatMul","MU_2_SparseMatMul", "MU_3_SparseMatMul",
               "MU_4_SparseMatMul", "MU_5_SparseMatMul"] # this is the original version of the paper.
    test_cases = ts.TestCases().getTestCases()
    test_cases = ts.TestCases().getSpecialTestCases()
    for mutant in mutants:
        cmr_list = pickup(num, mrs)
        try:
            for cmr in cmr_list:
                killed_mutants =TestOneMR(cmr, test_cases, [mutant])
                print("{}:{}".format(cmr.getMessage(),list(set(killed_mutants))))
        except Exception as e:
            print("\t\t{} could lead to crash of {}".format(mutant, e))
            continue

def Test1():
    TestAllCMRs(2)

if __name__ == "__main__":

    Test1()
