from chemcharts.core.container.fingerprint import FingerprintGenerator


def add_fingerprints(data_set_obj):
    # define function to add fingerprints to data_set
    fp_gen = FingerprintGenerator(data_set_obj.smiles_obj.smiles_list)
    data_set_obj.add_fingerprint(fp_gen.generate_fingerprints())
    data_set_obj.add_fingerprint(fp_gen.generate_fingerprints_morgan())
    data_set_obj.add_fingerprint(fp_gen.generate_fingerprints_maccs())
