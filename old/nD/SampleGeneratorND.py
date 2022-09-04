from re import M
from statistics import mean
from tkinter import Variable
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-poster')
import matplotlib.animation as animation
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
import math
import random

pi = math.pi
e = math.e
def JointSampleGenerator(): # x is distributed uniformmly and y follows a normal distribution whose mean is dependent on x
    x = np.random.uniform(0,1,500)
    JointSample = []
    for i in range(0,len(x)):
        y = np.float64((np.random.normal(2 * x[i] + 1, 2 * x[i] + 1, 1)))
        z = np.float64((np.random.normal(abs(x[i] + y), abs(x[i] + y), 1)))
        JointSample.append([x[i],y,z])
    return np.array(JointSample)

def IndependentCouplingGenerator(jointSamples, numsamples):
    dim = len(jointSamples[0])
    Samples = []
    for i in range(dim):
        r = random.choices(range(0,len(jointSamples)), k=numsamples)
        Samples.append(jointSamples[r,i])
    return np.array(np.transpose(Samples))


def RejectionSampling(Formula):
    TargetPDF = Formula
    Sample = []
    PlotPoint = []
    while len(Sample) < 500:
        SampleCandidate = [np.float64(np.random.uniform(0,1,1)), np.float64(np.random.uniform(-10,10,1))] 
        CandidateDistance = np.random.uniform(0,5,1) # This is equivalent to randomly choosing a point in this space: 0 < x < 1, -10 < y < 10 0 < z < 5
        if CandidateDistance <= TargetPDF(SampleCandidate):
            Sample.append(SampleCandidate) # Accept the point if it falls under the surface which represents the probability density function
            PlotPoint.append(SampleCandidate + [CandidateDistance])
    PlotPoint = np.array(PlotPoint)
    return np.array(Sample)

def main():
    SampleJoint  = np.loadtxt("implementing-flows/3D_moon.csv", delimiter=",")
    SampleIndependent = IndependentCouplingGenerator(SampleJoint, 2500)
    
    fig = plt.figure(figsize=(4,4))
    ax = fig.add_subplot(1, 2, 1, projection='3d')
    plt.title("Independent Coupling")
    ax.scatter3D(*zip(*SampleIndependent), color = 'r', alpha = 0.2)
    ax.set_xlim3d(0,8)
    ax.set_ylim3d(0,8)
    ax.set_zlim3d(0,8)

    ax = fig.add_subplot(1, 2, 2, projection='3d')
    plt.title("Joint Distribution")
    ax.scatter3D(*zip(*SampleJoint), color = 'r', alpha = 0.2)
    ax.set_xlim3d(0,8)
    ax.set_ylim3d(0,8)
    ax.set_zlim3d(0,8)
    plt.show()