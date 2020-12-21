import h5py

if __name__ == '__main__':

    path = '../data/msd_summary_file.h5'
    line_length = 100
    item_to_print = 10230

    with h5py.File(path, 'r') as f:
        metadata = f['metadata']['songs']
        print('Metadata fields\n')
        for field in metadata.dtype.fields:
            print(field, ":", metadata[item_to_print][field])

        print('-' * line_length)
        analysis = f['analysis']['songs']
        print('Analysis fields\n')
        for field in analysis.dtype.fields:
            print(field, ":", analysis[item_to_print][field])

        print('-' * line_length)
        musicbrainz = f['musicbrainz']['songs']
        print('Musicbrainz fields\n')
        for field in musicbrainz.dtype.fields:
            print(field, ":", musicbrainz[item_to_print][field])