from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'^$', 'gamewebstore.views.home', name='home'),
    url(r'^about/$', 'gamewebstore.views.about', name='about'),
    url(r'^accounts/udc/$', 'gamewebstore.views.userDataCollection', name='userDataCollection'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^developers/$', 'gamewebstore.views.developerHome', name='developerHome'),
    url(r'^developers/(?P<dev_id>\d+)/$', 'gamewebstore.views.developerCompany', name='developerCompany'),
    url(r'^developers/(?P<dev_id>\d+)/game/(?P<game_id>\d+)/$', 'gamewebstore.views.developerGame', name='developerGame'),
    url(r'^developers/add/$', 'gamewebstore.views.developerCompanyAdd', name='developerCompanyAdd'),
    url(r'^developers/(?P<dev_id>\d+)/delete/$', 'gamewebstore.views.developerCompanyDelete', name='developerCompanyDelete'),
    url(r'^developers/(?P<dev_id>\d+)/game/add/$', 'gamewebstore.views.developerGameAdd', name='developerGameAdd'),
    url(r'^developers/(?P<dev_id>\d+)/game/(?P<game_id>\d+)/edit/$', 'gamewebstore.views.developerGameEdit', name='developerGameEdit'),
    url(r'^developers/(?P<dev_id>\d+)/game/(?P<game_id>\d+)/toggleActive/$', 'gamewebstore.views.developerGameToggleActive', name='developerGameToggleActive'),
    url(r'^developers/(?P<dev_id>\d+)/newcategory/$', 'gamewebstore.views.developerCategoryAdd', name='developerCategoryAdd'),

    url(r'^marketplace/$', 'gamewebstore.views.marketplaceHome', name='marketplaceHome'),
    url(r'^marketplace/category/(?P<category_id>\d+)/$', 'gamewebstore.views.marketplaceCategoryListing', name='marketplaceCategoryListing'),
    url(r'^marketplace/game/(?P<game_id>\d+)/$', 'gamewebstore.views.marketplaceGameEntry', name='marketplaceGameEntry'),
    url(r'^marketplace/company/(?P<dev_id>\d+)/$', 'gamewebstore.views.marketplaceCompanyGamesListing', name='marketplaceCompanyGamesListing'),
    url(r'^marketplace/game/(?P<game_id>\d+)/buy/$', 'gamewebstore.views.marketplaceGamePurchase', name='marketplaceGamePurchase'),
    url(r'^marketplace/game/(?P<game_id>\d+)/buy/thankyou/$', 'gamewebstore.views.marketplaceGamePurchaseThankYou', name='marketplaceGamePurchaseThankYou'),

    url(r'^transactions/confirm$', 'gamewebstore.views.transactionsConfirm', name='transactionsConfirm'),
    url(r'^transactions/cancel$', 'gamewebstore.views.transactionsCancel', name='transactionsCancel'),
    url(r'^transactions/error$', 'gamewebstore.views.transactionsError', name='transactionsError'),

    url(r'^library/$', 'gamewebstore.views.libraryHome', name='libraryHome'),

    url(r'^play/(?P<game_id>\d+)/$', 'gamewebstore.views.playGame', name='playGame'),
    url(r'^api/(?P<game_id>\d+)/data/load/$', 'gamewebstore.views.playApiLoadSavedData', name='playApiLoadSavedData'),
    url(r'^api/(?P<game_id>\d+)/data/save/$', 'gamewebstore.views.playApiSaveData', name='playApiSaveData'),
    url(r'^api/(?P<game_id>\d+)/score/save/$', 'gamewebstore.views.playApiSaveScore', name='playApiSaveScore'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
