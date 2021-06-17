import get_verb_data
from kovol_verbs import PredictedKovolVerb

data = get_verb_data.get_data_from_csv()

for d in data:
    predicted = PredictedKovolVerb(d.remote_past_1s, d.recent_past_1s)
    predicted.print_with_kovol_verb(d)