from keras.layers import Input, Lambda, Dense, Flatten
from tensorflow.keras.applications import Xception
from keras.models import Model

def get_xception_model(split_size=(128,128), in_c=3):
    X = Xception(
        include_top=False,
        weights="imagenet",
        input_shape=split_size+(in_c,),
    )

    x = Flatten()(X.output)
    X_out = Dense(2, activation='softmax')(x)
    model = Model(inputs=X.input, outputs=X_out)
    
    return model