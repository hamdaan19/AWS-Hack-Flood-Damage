from keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.applications import Xception
from keras.models import Model

def get_xception_model()
    X = Xception(
        include_top=False,
        weights="imagenet",
        input_shape=(128, 128, 3)
    )

    x = Flatten()(X.output)
    X_out = Dense(2, activation='softmax')(x)
    model = Model(inputs=X.input, outputs=X_out)
    
    return model