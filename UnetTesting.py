import os

from keras.models import load_model

from UnetTraining import (dice_coef, dice_coef_loss, pickle_load, get_subject_dirs, get_subject_id, read_subject_folder,
                          crop_data, pickle_dump, np)


def test_model(model):
    for testing_dir in get_testing_dirs():
        test_data = crop_data(read_subject_folder(testing_dir))
        prediction = predict(model, test_data)
        pickle_dump(prediction, "prediction.pkl")
        break


def get_testing_dirs():
    subject_dirs = get_subject_dirs()
    testing_ids = get_test_ids()
    testing_dirs = []
    for subject_dir in subject_dirs:
        subject_id = get_subject_id(subject_dir)
        if subject_id in testing_ids:
            testing_dirs.append(subject_dir)
    return testing_dirs


def get_prediction_labels(prediction, threshold=0.5):
    n_samples = prediction.shape[0]
    label_arrays = []
    for sample_number in range(n_samples):
        label_data = np.argmax(prediction[sample_number], axis=0) + 1
        label_data[np.max(prediction) > threshold] = 0
        label_arrays.append(label_data)
    return label_arrays


def get_test_ids():
    return pickle_load("testing_ids.pkl")


def predict(model, data):
    x_data = data[:3]
    return model.predict(np.array([x_data]))


def main():
    model_file = os.path.abspath("3d_unet_model.h5")
    model = load_model(model_file, custom_objects={'dice_coef_loss': dice_coef_loss, 'dice_coef': dice_coef})
    test_model(model)


if __name__ == "__main__":
    main()
