import gym
import numpy as np
import time
env = gym.make('CartPole-v0')
pvariance = 0.1 # variance of initial parameters
ppvariance = 0.02 # variance of perturbations
nhiddens = 5 # number of hidden neurons
population_size = 25


ninputs = env.observation_space.shape[0]
if (isinstance(env.action_space, gym.spaces.box.Box)):
    noutputs = env.action_space.shape[0]
else:
    noutputs = env.action_space.n

W1 = np.random.randn(nhiddens,ninputs) * pvariance # first layer
W2 = np.random.randn(noutputs, nhiddens) * pvariance # second layer
B1 = np.zeros(shape=(nhiddens, 1)) # bias first layer
B2 = np.zeros(shape=(noutputs, 1)) # bias second layer
theta = np.concatenate((W1.flatten(), W2.flatten(), B1.flatten(),B2.flatten()))
param_pop = np.random.randn(population_size, len(theta)) * pvariance


for g in range(1,20):
    score =0
    s=[]
    obs = []
    for i_episode in range(population_size):
        observation = env.reset()
        for _ in range(200):
            w1 = param_pop[i_episode][0:20].reshape(W1.shape)
            b1 = param_pop[i_episode][30:35].reshape(B1.shape)
            w2 = param_pop[i_episode][20:30].reshape(W2.shape)
            b2 = param_pop[i_episode][35:37].reshape(B2.shape)

            observation.resize(ninputs,1)
            Z1 = np.dot(w1, observation) + b1
            A1 = np.tanh(Z1)
            Z2 = np.dot(w2, A1) + b2
            A2 = np.tanh(Z2)
            if (isinstance(env.action_space, gym.spaces.box.Box)):
                action = A2
            else:
                action = np.argmax(A2)
            time.sleep(0.01)
            env.render()
            observation, reward, done, info = env.step(action)
            if(reward==1):
                score +=1
            if done: 
                break

        # env.close()
        s.append(score) 
        obs.append(observation) 

    print("score for generation", g ," :",s)
    idx = np.argsort(s)
    for j in range(int(population_size/2)):
        param_pop[idx[j]]=param_pop[idx[j+(population_size//2)]]+ np.random.normal(0.1)*ppvariance

env.close()






