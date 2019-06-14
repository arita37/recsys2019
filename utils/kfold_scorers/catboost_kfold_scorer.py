from recommenders.catboost_rank import CatboostRanker
from recommenders.kfold_scorer import KFoldScorer
from utils.dataset import DatasetCatboost
from utils.menu import mode_selection
from utils.menu import cluster_selection

if __name__ == "__main__":
    mode = mode_selection()
    cluster = cluster_selection()
    dataset = DatasetCatboost(mode, cluster)

    init_params = {
        'mode': mode,
        'cluster': cluster,
        'learning_rate': 0.25,
        'iterations': 100,
        'max_depth': 11,
        'reg_lambda': 7.23,
        'colsample_bylevel': 1,
        'one_hot_max_size': 46,
    }

    fit_params = {}

    kfscorer = KFoldScorer(model_class=CatboostRanker, init_params=init_params, k=5)
    kfscorer.fit_predict(dataset, fit_params=fit_params)
