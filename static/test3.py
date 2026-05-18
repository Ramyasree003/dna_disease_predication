import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical

# Load data
df = pd.read_csv("static/dataset/dataset.csv")

# Map implication to categorical labels
df['Implication_Label'] = LabelEncoder().fit_transform(df['Implication'])

# One-hot encode categorical input features
X = pd.get_dummies(df[['Gene Variant / Mutation Identified',
                       'Type of DNA Change',
                       'Associated Disease / Risk']])

y = to_categorical(df['Implication_Label'])

# Reshape for LSTM: (samples, timesteps, features)
X_lstm = np.array(X).reshape((X.shape[0], 1, X.shape[1]))

# Split
X_train, X_test, y_train, y_test = train_test_split(X_lstm, y, test_size=0.2, random_state=42)

# LSTM model
model = Sequential()
model.add(LSTM(64, input_shape=(1, X.shape[1])))
model.add(Dense(y.shape[1], activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

# Train
model.fit(X_train, y_train, epochs=20, batch_size=8, validation_split=0.2)

# Evaluate
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy:.2f}")
