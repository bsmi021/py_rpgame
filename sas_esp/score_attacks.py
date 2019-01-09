# ~/sas_esp/score_attacks.py

""" This script provides the logic for scoring attack objects using Scikit-Learn Linear regression, it assumes
    the location of the model file is in the /data/models directory of the host for the ESP Server.

    The model file for this script for dev purposes is stored in the ~/sas_esp/data/models directory as
    p_attack_lr_v1.sav, this file should be copied to the host for the ESP server into the /data/models directory
    or you will need to change the path in the below script

    Note the /sas_esp/data/models directory structure was created to make testing easier as it mocks the structure
    for the demo, again you can change this on your own implementation.
    """

from pickle import load

import numpy as np

model_file = '/data/models/p_attack_lr_v1.sav'
# model_file_path = os.path.join('data', os.path.join('models', model_file))

loaded_model = load(open(model_file, 'rb'))


def predict_attack_amt(attack_id, att_attack_amt, player_critical_chance, att_base_attack_amt,
                       player_min_damage, player_max_damage, att_blocked, att_critical, att_dodged, att_missed):
    "Output: attack_id, att_attack_amt, predicted"

    X = np.array([player_critical_chance, att_base_attack_amt,
                  player_min_damage, player_max_damage, att_blocked, att_critical, att_dodged, att_missed])
    predicted = loaded_model.predict(X[np.newaxis, :])
    predicted = int(predicted[0][0])

    return (attack_id, att_attack_amt, predicted)


# ###### Tests
model_test = predict_attack_amt(1, 41, 0.29, 41, 18, 49, 0, 0, 0, 0)
print(model_test)
