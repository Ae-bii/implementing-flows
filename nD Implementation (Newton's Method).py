import numpy as np
import random
import math
import numdifftools as nd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


random.seed(0)
np.random.seed(0)

e = math.e
pi = math.pi

def distance(z1, z2):
    sum = 0
    for i in range(0,len(z1)-1):
        sum += (z1[i] - z2[i]) ** 2
    return math.sqrt(sum)

def F_0(z):
    r = distance(z, center_1)
    alpha = 0.75 # Consistent with the density (As this gets larger, less samples are moved close to 0)
    return r * math.erf(r/alpha) + (alpha/math.sqrt(pi)) * math.pow(e, -(r/alpha) ** 2)

def F_1(z):
    r = distance(z, center_2)
    alpha = 0.75
    return alpha + r - alpha * math.log(abs(alpha + r))


def BetaNewton(): # Newton's method (Experimental)
    xSummationGradient_1 = 0
    ySummationGradient_1 = 0
    xSummationGradient_2 = 0
    ySummationGradient_2 = 0
    for i in range(0, len(MixtureSample)):
        xSummationGradient_1 += F_0(MixtureSample[i])
        xSummationGradient_2 += F_1(MixtureSample[i])
    for j in range(0, len(StandardNormal)):
        ySummationGradient_1 += F_0(StandardNormal[j])
        ySummationGradient_2 += F_1(StandardNormal[j])
    G_1 = (1/len(MixtureSample)) * xSummationGradient_1 - (1/len(StandardNormal)) * ySummationGradient_1
    G_2 = (1/len(MixtureSample)) * xSummationGradient_2 - (1/len(StandardNormal)) * ySummationGradient_2
    G = np.array([G_1, G_2])
    yHessian_11 = 0
    yHessian_12 = 0
    yHessian_21 = 0
    yHessian_22 = 0
    for l in range(0, len(StandardNormal)):
        yHessian_11 += np.dot(nd.Gradient(F_0)([StandardNormal[l]]), nd.Gradient(F_0)(StandardNormal[l]))
        yHessian_12 += np.dot(nd.Gradient(F_0)([StandardNormal[l]]), nd.Gradient(F_1)(StandardNormal[l]))
        yHessian_21 += np.dot(nd.Gradient(F_1)([StandardNormal[l]]), nd.Gradient(F_0)(StandardNormal[l]))
        yHessian_22 += np.dot(nd.Gradient(F_1)([StandardNormal[l]]), nd.Gradient(F_1)(StandardNormal[l]))
    H_11 = (1/len(StandardNormal)) * yHessian_11
    H_12 = (1/len(StandardNormal)) * yHessian_12
    H_21 = (1/len(StandardNormal)) * yHessian_21
    H_22 = (1/len(StandardNormal)) * yHessian_22
    H = np.array([[H_11,H_12],
                 [H_21,H_22]])
    HInverseNeg = (-1) * np.linalg.inv(H)
    Beta = np.matmul(HInverseNeg, G)
    LearningRate = 0.01 # Not sure how to choose this value
    ParameterList = [1, LearningRate/np.linalg.norm(Beta)]
    return Beta * min(ParameterList) # min(ParameterList) can be understood as similar to the "Proportion" in gradient descent

def u(x, Beta):
    return np.dot(x, x)/2 + Beta[0] * F_0(x) + Beta[1] * F_1(x)

def uConjugate(y, Beta):
    ConvexCandidate = []
    for i in range(0, len(MixtureSample)):
        ConvexCandidate.append(np.dot(MixtureSample[i], y) - u(MixtureSample[i], Beta))
    return max(ConvexCandidate)

def D(Beta):
    xSummation = 0
    ySummation = 0
    for i in range(0, len(MixtureSample)):
        xSummation += u(MixtureSample[i], Beta)
    for j in range(0, len(StandardNormal)):
        ySummation += uConjugate(StandardNormal[j], Beta)
    LL = 1/len(MixtureSample) * xSummation + 1 / \
        len(StandardNormal) * ySummation
    
    return LL



def SamplesUpdate(OldMixtureSample):
    NewMixtureSample = []
    for i in range(0, len(OldMixtureSample)):
        cur = []
        for j in range(dim):
            cur.append(OldMixtureSample[i][j] + Beta[0] * nd.Gradient(F_0)(OldMixtureSample[i])[j] + Beta[1] * nd.Gradient(F_1)(OldMixtureSample[i])[j])
        NewMixtureSample.append(np.array(cur))
    NewMixtureSample = np.array(NewMixtureSample)
    return NewMixtureSample


def MixtureSampleGenerator():
    mean1 = [1, -1, 1]
    mean2 = [-1, 1, -2]
    mean3 = [-1, 2, -1]
    cov = np.array([0.5, 0.5, 0.5])
    cov1 = np.diag(cov**dim)
    cov2 = np.diag(cov**dim)
    cov3 = np.diag(cov**dim)
    x = np.random.multivariate_normal(mean1, cov1, 200)
    y = np.random.multivariate_normal(mean2, cov2, 200)
    z = np.random.multivariate_normal(mean3, cov3, 200)
    MixtureSample = []
    for i in range(200):
        RandomSelector = random.random()
        if RandomSelector > 0.7:
            MixtureSample.append(x[i])
        elif RandomSelector < 0.3:
            MixtureSample.append(z[i])
        else:
            MixtureSample.append(y[i])
    MixtureSample = np.array(MixtureSample)
    return MixtureSample

def StandardNormalGenerator():
    Sample = []
    x = np.random.standard_normal(200)
    y = np.random.standard_normal(200)
    z = np.random.standard_normal(200)
    for i in range(200):
        Sample.append(np.array([x[i], y[i], z[i]]))
    return Sample


#------------------------------------------------------------------ TESTING (change to heatmap, add animtation)------------------------------------------------------------
dim = 3

MixtureSample = MixtureSampleGenerator()
StandardNormal = StandardNormalGenerator()
CenterGeneratorList = MixtureSample + StandardNormal

DValue = 0
Iteration = 0 
while True:
    Iteration += 1
    TooClose = 1
    while TooClose == 1:
        center_1 = CenterGeneratorList[random.randint(0, len(CenterGeneratorList) - 1)]
        center_2 = CenterGeneratorList[random.randint(0, len(CenterGeneratorList) - 1)]
        if distance(center_1, center_2) >= 0.75:
            TooClose = 0
    Beta = BetaNewton()
    OldD = DValue
    DValue = D(Beta)
    print(DValue)
    MixtureSample = SamplesUpdate(MixtureSample)
    if abs(DValue - OldD) < 0.001 or Iteration >20:
        break
