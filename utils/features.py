from aws_lambda_powertools.utilities.feature_flags import AppConfigStore, FeatureFlags

store = AppConfigStore(application="EcommerceApp", environment="prod", name="flags")
feature_flags = FeatureFlags(store=store, cache_interval=300)
