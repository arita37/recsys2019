from tqdm.auto import tqdm

def find(df):
    """ This assumes that the df is ordered by user_id, session_id, timestamp, step """
    indices = []
    cur_ses = ''
    cur_user = ''
    temp_df = df[df.action_type == 'clickout item'][['user_id', 'session_id', 'action_type']]
    #temp_df = temp_df.sort_index()
    for idx in tqdm(temp_df.index.values[::-1]):
        ruid = temp_df.at[idx, 'user_id']
        rsid = temp_df.at[idx, 'session_id']
        if (ruid != cur_user or rsid != cur_ses):
            indices.append(idx)
            cur_user = ruid
            cur_ses = rsid
    return indices[::-1]