(function () {

'use strict';

angular.module('OpenSlidesApp.openslides_protocol', [
    'OpenSlidesApp.core.site',
    'OpenSlidesApp.openslides_protocol.templates',
])

.config([
    'OpenSlidesPluginsProvider',
    function(OpenSlidesPluginsProvider) {
        OpenSlidesPluginsProvider.registerPlugin({
            name: 'openslides_protocol',
            display_name: 'Protocol',
            languages: ['de']
        });
    }
])

.factory('ItemProtocol', [
    'DS',
    'gettext',
    'operator',
    function (DS, gettext, operator) {
        var name = 'openslides_protocol/item-protocol';
        return DS.defineResource({
            name: name,
            relations: {
                belongsTo: {
                    'agenda/item': {
                        localField: 'item',
                        localKey: 'item_id',
                    }
                }
            },
        });
    }
])

.run(['ItemProtocol', function (ItemProtocol) {}]);

}());
