import pickle
import os
import sys
import preprocessing
import models
import aws


root_dir = os.getcwd()
data_dir = os.path.abspath(root_dir + "/data/")
prog_path = data_dir + "/ml_prog.pickle"


def load_progress(pickle_path):
    if (os.path.isfile(pickle_path)) is True:
        pickle_to_import = open(pickle_path, "rb")
        return pickle.load(pickle_to_import)
    else:
        return None


def save_progress(phase_num, pickle_path):
    prog = {"Progress": phase_num}
    pickle_to_export = open(pickle_path, "wb")
    pickle.dump(prog, pickle_to_export)
    pickle_to_export.close()


def mine_phase_three_clustering():
    # save_progress(5, mine_prog_path)
    # mine_final_phase()
    pass


def mine_final_phase():
    print("You have finished running the data pipeline. Results are available at: data/results/")


def manip_images(model_paths):
    preprocessing.process_kaggle(model_paths.all_solutions, model_paths.clean_solutions)
    preprocessing.remove_others(model_paths.train_image_path, model_paths.clean_solutions)
    preprocessing.crop_all(model_paths.train_image_path)
    preprocessing.create_valids(model_paths.train_image_path, model_paths.valid_image_path, model_paths.clean_solutions,
                                model_paths.clean_train_solutions, model_paths.valid_solutions)
    preprocessing.update_solutions(model_paths.clean_train_solutions, model_paths.augmented_train_solutions)
    preprocessing.augment_images(model_paths.train_image_path, model_paths.clean_train_solutions)
    preprocessing.move_augments(model_paths.train_image_path)


def detect_boxes():
    aws.detect_boxes()


if __name__ == '__main__':
    model_paths = models.initialize_default_paths()
    system_arguments = ' '.join(sys.argv[1:])

    if system_arguments == "aws":
        detect_boxes()

    if system_arguments == "Manip Data":
        manip_images(model_paths)

    elif system_arguments == "Train Model":
        models.train_model(model_paths)

    elif system_arguments == "Train Transfer Model":
        models.train_model(model_paths, transfer=True)

    elif system_arguments == "Predict":
        models.calculate_predictions(model_paths.valid_solutions, model_paths.valid_image_path, model_paths.valid_true, model_paths.valid_preds, model_paths.checkpoint_overall_path)
        models.eval_metrics(model_paths.valid_true, model_paths.valid_preds, model_paths.valid_conf_matrix, model_paths.valid_other_metrics)

    elif system_arguments == "Predict Test":
        models.calculate_predictions(model_paths.test_solutions, model_paths.test_image_path, model_paths.test_true, model_paths.test_preds, model_paths.checkpoint_overall_path)
        models.eval_metrics(model_paths.test_true, model_paths.test_preds, model_paths.test_conf_matrix, model_paths.test_other_metrics)


    # elif system_arguments == "ML":
    #     progress = load_progress(ml_prog_path)
    #     if progress is None:
    #         ml_phase_one_data_retrieval()
    #     else:
    #         num = progress['Progress']
    #         switcher = {
    #             1: phase_one_data_retrieval,
    #             2: phase_two_data_cleaning,
    #             3: phase_three_further_data,
    #             4: phase_four_logs,
    #             5: phase_five_get_sdfs,
    #             7: final_phase
    #         }
    #
    #         current_phase = switcher.get(num, lambda: "Corrupt pickle.")
    #         current_phase()
