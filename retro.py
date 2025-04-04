import numpy as np
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
def derivee_sigmoid(x):
    return x * (1 - x)

#def relu(x):
 #   return np.maximum(0, x)
#def derivee_relu(x):
 #   return (x > 0).astype(float)

class simplemlp:
    def __init__(self, nb_neurones_entree, couches_cachees, nb_neurones_sortie, taux_apprentissage=0.01):
                self.taux_apprentissage = taux_apprentissage
                self.couches = [nb_neurones_entree] + couches_cachees + [nb_neurones_sortie]
                self.poids = []
                self.biais = []
                for i in range(len(self.couches) - 1):
                    self.poids.append(np.random.randn(self.couches[i], self.couches[i+1]) * 0.01)
                    self.biais.append(np.zeros((1, self.couches[i+1])))     
                    
    def propagation_avant(self, X):
        activations = [X]
        valeurs_Z = []
        for i in range(len(self.poids)):
            Z = np.dot(activations[-1], self.poids[i]) + self.biais[i]
            valeurs_Z.append(Z)
            if i < len(self.poids) - 1:
                A = sigmoid(Z)  # Activation ReLU pour les couches cachées
            else:
                A = sigmoid(Z)  # Activation sigmoïde pour la couche de sortie
            activations.append(A)
            
             
        return activations, valeurs_Z
    
    
    def retropropagation(self, X, Y):
        activations, valeurs_Z = self.propagation_avant(X)
        dW = [0] * len(self.poids)
        dB = [0] * len(self.biais)
        dA = activations[-1] - Y  # Erreur de la sortie
        m = Y.shape[0]  # Nombre d'exemples 
        
        
           #  calculer les gradients des Wet de B pour chaque couche   
        for i in reversed(range(len(self.poids))):
           
            dZ = dA * derivee_sigmoid(valeurs_Z[i])  #calculer la deriveer pour  tout les couvhes cachees
        
            dW[i] = np.dot(activations[i].T, dZ) / m  # Gradient des valeur de W
            dB[i] = np.sum(dZ, axis=0, keepdims=True) / m  # Gradient  de la valeur de B
            dA = np.dot(dZ, self.poids[i].T)  # Propagation de l'erreur vers l'arrière      
        
        
    # mise a jour des valeur de W et B 
        for i in range(len(self.poids)):
            self.poids[i] -= self.taux_apprentissage * dW[i]
            self.biais[i] -= self.taux_apprentissage * dB[i]
            
# l'entrainement de mlp
    def entrainer(self, X, Y, epochs=1000):
        for epoch in range(epochs):
            self.retropropagation(X, Y)
            if epoch % 100 == 0:
                activations, _ = self.propagation_avant(X)
                erreur = np.mean((Y - activations[-1])**2)
                #print(f"Epoch {epoch}, Erreur: {erreur:.5f}")
        return erreur        

#exmple
X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y_train = np.array([[0], [1], [1], [0]])


mlp = simplemlp(nb_neurones_entree=2, couches_cachees=[4,2], nb_neurones_sortie=1, taux_apprentissage=0.05)
Resultat = mlp.entrainer(X_train, Y_train, epochs=1000)
print("errore de entrenments :", Resultat)

activations, _ = mlp.propagation_avant(X_train)
print("Sortie apres entrainement:\n", activations[-1])
   
