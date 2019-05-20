import data
from extract_features.first_impression_price import FirstImpressionPrice
from extract_features.label_classification import LabelClassification
from extract_features.last_action_before_clickout import LastActionBeforeClickout
from extract_features.last_action_first_impression import LastActionFirstImpression
from extract_features.last_action_involving_first_impression import LastActionInvolvingFirstImpressions
from extract_features.mean_price_clickout import MeanPriceClickout
from extract_features.num_impressions_in_clickout import NumImpressionsInClickout
from extract_features.num_interactions_with_first_impression import NumInteractionsWithFirstImpression
from extract_features.num_interactions_with_first_impression_in_history import \
    NumInteractionsWithFirstImpressionInHistory
from extract_features.price_position_info_interactions import PricePositionInfoInteractedReferences
from extract_features.session_device import SessionDevice
from extract_features.session_length import SessionLength
from extract_features.session_sort_order_when_clickout import SessionSortOrderWhenClickout
from extract_features.time_from_last_action_before_clk import TimeFromLastActionBeforeClk
from utils.check_folder import check_folder


def merge_features_classifier(mode, cluster, features_array, starting_feature):
    df = starting_feature(mode=mode, cluster=cluster).read_feature()
    for f in features_array:
        feature = f(mode=mode, cluster=cluster)
        df = feature.join_to(df, one_hot=True)
        print("Merged with feature:" + feature.name)
        print("New df shape: {}".format(df.shape))

    test_df = data.test_df(mode, cluster)
    test_df = test_df[(test_df.action_type == "clickout item") & (test_df.reference.isnull())]
    sessions = set(test_df.session_id)
    train_df = df[~df.session_id.isin(sessions)]
    test_df = df[df.session_id.isin(sessions)]
    return train_df, test_df

def create_dataset(mode, cluster):
    # training
    features_array = [SessionDevice, SessionSortOrderWhenClickout, MeanPriceClickout,
                      PricePositionInfoInteractedReferences,
                      SessionLength, TimeFromLastActionBeforeClk, LastActionBeforeClickout,
                      NumInteractionsWithFirstImpression, FirstImpressionPrice,
                      LastActionFirstImpression,
                      LastActionInvolvingFirstImpressions,
                      NumInteractionsWithFirstImpression, NumImpressionsInClickout]

    train_df, test_df = merge_features_classifier(mode, cluster, features_array, LabelClassification)
    check_folder('dataset/preprocessed/{}/{}/xgboost_classifier/'.format(cluster, mode))

    train_df.to_csv('dataset/preprocessed/{}/{}/xgboost_classifier/train.csv'.format(cluster, mode), index=False)
    test_df.to_csv('dataset/preprocessed/{}/{}/xgboost_classifier/test.csv'.format(cluster, mode), index=False)

    print("Dataset created!")


if __name__ == "__main__":
    from utils.menu import mode_selection
    mode = mode_selection()
    cluster = 'no_cluster'
    create_dataset(mode, cluster)
