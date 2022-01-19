from tensorflow import keras

def make_predictions(image):
    my_model = keras.models.load_model("vgg_classification_model")
    image_np = np.array(image)
    prediction = my_model.predict(x=image_np)
    output = np.argmax(prediction, axis=1)
    
    return output