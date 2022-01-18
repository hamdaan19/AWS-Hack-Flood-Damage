from tensorflow import keras
from tensorflow.keras import layers

class Unet_xception():
    def __init__(self, img_size, in_channels, classes):
        self.img_size = img_size
        self.in_channels = in_channels
        self.classes = classes
        
        inputs = keras.Input(shape=self.img_size + (self.in_channels,))
        
        ### First half of the network: downsampling inputs ###
        
        # Entry Block 
        x = layers.Conv2D(32, kernel_size=3, strides=2, padding="same")(inputs)
        x = layers.BatchNormalization()(x)
        x = layers.Activation("relu")(x)
        
        self.saved_residue = x
        
        for filters in [64, 128, 256]:
            x = self.sampling_down(filters, x)
            
        ### Second half of the network: upsampling inputs ###   
        
        for filters in [256, 128, 64, 32]:
            x = self.sampling_up(filters, x)
            
        # Adding final output (classification) layer 
        outputs = layers.Conv2D(self.classes, kernel_size=3, activation="softmax", padding="same")(x)
        
        self.model = keras.Model(inputs=inputs, outputs=outputs)
        
        return None
            
            
    def sampling_down(self, f, x):
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(f, kernel_size=3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        
        x = layers.Activation("relu")(x)
        x = layers.SeparableConv2D(f, kernel_size=3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        
        
        x = layers.MaxPooling2D(pool_size=3, strides=2, padding="same")(x)
        
        residue = layers.Conv2D(f, kernel_size=1, strides=2, padding="same")(
            self.saved_residue
        )
        x = layers.add([x, residue]) # Adding back residue
        self.saved_residue = x       # Setting aside next residue
        
        return x
    
    
    def sampling_up(self, f, x):
        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(f, kernel_size=3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        
        x = layers.Activation("relu")(x)
        x = layers.Conv2DTranspose(f, kernel_size=3, padding="same")(x)
        x = layers.BatchNormalization()(x)
        
        x = layers.UpSampling2D(size=2)(x)
        
        residue = layers.UpSampling2D(size=2)(self.saved_residue)
        residue = layers.Conv2D(f, kernel_size=1, padding="same")(residue)
        x = layers.add([x, residue]) # Adding back residue
        self.saved_residue = x       # Setting aside next residue 
        
        return x
        
