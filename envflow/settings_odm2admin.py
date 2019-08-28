""" SENSOR DASHBOARD CONFIGURATION """
SENSOR_DASHBOARD = {
    "time_series_days": 30,
    "featureactionids": [1699, 1784, 1782, 1701],
}
""" END SENSOR DASHBOARD CONFIGURATION"""

""" MAP CONFIGURATION """
MAP_CONFIG = {
    "lat": 0,
    "lon": 0,
    "zoom": 2,
    "cluster_feature_types": ['Profile', 'Specimen', 'Excavation', 'Field area'],
    "time_series_months": 1,
    "display_titles": True,
    "MapBox": {
      "access_token": 'mapbox accessToken'
    },
    "result_value_processing_levels_to_display": [1, 2, 3],
    "feature_types": ['Site', 'Profile', 'Specimen', 'Excavation', 'Field area', 'Weather station', 'Observation well',
                      'Stream gage', 'Transect']
}
""" END MAP CONFIGURATION """

""" SAMPLING FEATURE TYPE LEGEND MAPPING """
LEGEND_MAP = {
        'Excavation': dict(feature_type="Excavation", icon="fa-spoon", color="darkred",
                           style_class="awesome-marker-icon-darkred"),
        'Field area': dict(feature_type="Field area", icon="fa-map-o", color="darkblue",
                           style_class="awesome-marker-icon-darkblue"),
        'Weather station': dict(feature_type="Weather station", icon="fa-cloud", color="darkblue",
                                style_class="awesome-marker-icon-darkblue"),
        'Ecological land classification': dict(feature_type="Ecological land classification",
                                               icon="fa-bar-chart", color="darkpurple",
                                               style_class="awesome-marker-icon-darkpurple"),
        'Observation well': dict(feature_type="Observation well", icon="fa-eye", color="orange",
                                 style_class="awesome-marker-icon-orange"),
        'Site': dict(feature_type="Site", icon="fa-dot-circle-o", color="green",
                     style_class="awesome-marker-icon-green"),
        'Stream gage': dict(feature_type="Stream gage", icon="fa-tint", color="blue",
                            style_class="awesome-marker-icon-blue"),
        'Transect': dict(feature_type="Transect", icon="fa-area-chart", color="cadetblue",
                         style_class="awesome-marker-icon-cadetblue"),
        'Profile': dict(feature_type="Profile", icon="fa-database", color="purple",
                        style_class="awesome-marker-icon-purple"),
        'Specimen': dict(feature_type="Specimen", icon="fa-flask", color="cadetblue",
                         style_class="awesome-marker-icon-cadetblue")
    }
""" END SAMPLING FEATURE TYPE LEGEND MAPPING """

""" DATA DISCLAIMER CONFIGURATION """
DATA_DISCLAIMER = {
    "text": "Add a link discribing where your data come from",
    "linktext": "The name of my site",
    "link": "http://mysiteswegpage.page/",
}
""" END DATA DISCLAIMER CONFIGURATION """

SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',)