# coding=cp1251
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$', 'turbodiesel.core.main.main_page'),
                       (r'^(\d*)/$', 'turbodiesel.core.views.dashboard'),
                       (r'^entity/(\d*)/(.*)$', 'turbodiesel.core.views.control'),
                       (r'^(\d*)/(\d*)/$', 'turbodiesel.core.views.dashboard_extend'),
                       (r'^(\d*)/common/attach$', 'turbodiesel.core.views.attach'),
                       (r'^(\d*)/create/(\d*)$', 'turbodiesel.core.views.create_page'),
                       (r'^(\d*)/gantt/$', 'turbodiesel.core.views.gantt'),
                       (r'^(\d*)/(.*)/$', 'turbodiesel.core.views.tab'),
                       (r'^(\d*)/save_environment$', 'turbodiesel.core.portal.save_environment'),
                       (r'^(\d*)/load_environment/(\d*)$', 'turbodiesel.core.portal.load_environment'),
                       # ###########################################################################################
                       (r'^entity_filters/(\d*)/(.*)$', 'turbodiesel.core.views.control'),
                       (r'^custom_edit/$', 'turbodiesel.core.views.fiction_delete'),
                       (r'^delete_entity_value/(\d*)/$', 'turbodiesel.core.views.delete_entity_value'),
                       (r'^save_environment/(.*)$', 'turbodiesel.core.portal.save_environment'),
                       (r'^load_environment/(.*)$', 'turbodiesel.core.portal.load_environment'),
                       (r'^save_template/(.*)$', 'turbodiesel.core.portal.save_template'),
                       (r'^custom_save_filter/$', 'turbodiesel.core.portal.save_custom_filter'),  #Сохранение фильтров
                       (r'^apply_filter_from_jqgrid/$', 'turbodiesel.core.portal.apply_filter_from_jqgrid'),
                       #Применение фильтров для импорта в jqgrid
                       (r'^apply_filter_from_xls/$', 'turbodiesel.core.portal.apply_filter_from_xls'),
                       #Применение фильтров для импорта в xls
                       (r'^apply_a_saved_filter/(\d*)/$', 'turbodiesel.core.portal.apply_a_saved_filter'),
                       #Применение сохраненных фильтров для импорта в jqgrid
                       (r'^request_filter_list$', 'turbodiesel.core.portal.get_filter_list'),
                       ############################################################################################
                       (r'^download_delivery/(.*)$', 'turbodiesel.core.views.download_delivery'),
                       (r'^download_product/(.*)$', 'turbodiesel.core.views.download_product'),
                       ############################################################################################
                       (r'^request_calendar/(.*)/$', 'turbodiesel.core.views.request_calendar'),
                       (r'^request_entity_properties/(\d*)$', 'turbodiesel.core.views.request_properties'),
                       (r'^request_entity_value_table/(\d*)/(\d*)/(.*)$',
                        'turbodiesel.core.views.request_table_content'),
                       (r'^request_entity_select/(\d*)/(\d*)/$', 'turbodiesel.core.views.request_select_content'),
                       (r'^request_entity_comments/(\d*)/$', 'turbodiesel.core.views.request_comments'),
                       (r'^request_entity_history/(\d*)$', 'turbodiesel.core.views.request_history'),
                       (r'^request_entity_attachments/(\d*)/$', 'turbodiesel.core.views.request_attachments'),
                       (r'^request_gantt_data/$', 'turbodiesel.core.views.request_gantt_data'),
                       (r'^request_details/(\d*)/$', 'turbodiesel.core.views.request_detail'),
                       (r'^request_entity_list/(\d*)/(-?\d+)/$', 'turbodiesel.core.views.get_entity_table'),
                       (r'^request_entity_control/(\d*)/(.*)/(.*)/$',
                        'turbodiesel.core.views.get_properties_from_entity_control'),
                       (r'^request_usecase/(\d*)/$', 'turbodiesel.core.views.request_usecase'),
                       ############################################################################################
                       (r'^create_entity', 'turbodiesel.core.create.create_json'),
                       (r'^update_entity', 'turbodiesel.core.update.update_json'),
                       (r'^view_entity/(\d*)/$', 'turbodiesel.core.update.update_json'),
)