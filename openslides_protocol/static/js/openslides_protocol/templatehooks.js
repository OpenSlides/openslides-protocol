(function () {

'use strict';

angular.module('OpenSlidesApp.openslides_protocol.templatehooks', ['OpenSlidesApp.openslides_protocol'])

.run([
    'templateHooks',
    'ngDialog',
    'ObjectProtocolDialog',
    'ObjectProtocol',
    function (templateHooks, ngDialog, ObjectProtocolDialog, ObjectProtocol) {
        // Agenda
        templateHooks.registerHook({
            Id: 'agendaListAdditionalContentColumn',
            templateUrl: 'static/templates/openslides_protocol/agenda-hook.html',
            scope: {
                openProtocolDialog: function (item) {
                    ngDialog.open(ObjectProtocolDialog.getDialog(item.getContentObject(), true));
                },
                hasProtocol: function (item) {
                    return _.some(ObjectProtocol.getAll(), function (protocol) {
                        return protocol.content_object.collection === item.content_object.collection &&
                            protocol.content_object.id === item.content_object.id;
                    });
                },
                getPlainProtocolText: function (item) {
                    var protocol = _.find(ObjectProtocol.getAll(), function (protocol) {
                        return protocol.content_object.collection === item.content_object.collection &&
                            protocol.content_object.id === item.content_object.id;
                    });
                    return protocol ? $(protocol.protocol).text() : '';
                },
            },
        });
        var getScope = function () {
            return {
                openProtocolDialog: function (obj) {
                    ngDialog.open(ObjectProtocolDialog.getDialog(obj, true));
                },
                hasProtocol: function (obj) {
                    var resourceName = obj.getResourceName();
                    return _.some(ObjectProtocol.getAll(), function (protocol) {
                        return protocol.content_object.collection === resourceName &&
                            protocol.content_object.id === obj.id;
                    });
                },
                getProtocol: function (obj) {
                    var resourceName = obj.getResourceName();
                    return _.find(ObjectProtocol.getAll(), function (protocol) {
                        return protocol.content_object.collection === resourceName &&
                            protocol.content_object.id === obj.id;
                    }).protocol;
                },
                getPlainProtocolText: function (obj) {
                    return $(this.getProtocol(obj)).text();
                },
            };
        };
        // Topic detail
        templateHooks.registerHook({
            Id: 'topicDetailViewDetailContainer',
            templateUrl: 'static/templates/openslides_protocol/topic-detail-hook.html',
            scope: getScope(),
        });
        // Motion list
        templateHooks.registerHook({
            Id: 'motionListAdditionalContentColumn',
            templateUrl: 'static/templates/openslides_protocol/motion-list-hook.html',
            scope: getScope(),
        });
        // Motion detail
        templateHooks.registerHook({
            Id: 'motionDetailViewDetailContainer',
            templateUrl: 'static/templates/openslides_protocol/motion-detail-hook.html',
            scope: getScope(),
        });
        // Assignment list
        templateHooks.registerHook({
            Id: 'assignmentListAdditionalContentColumn',
            templateUrl: 'static/templates/openslides_protocol/assignment-list-hook.html',
            scope: getScope(),
        });
        // Assignment detail
        templateHooks.registerHook({
            Id: 'assignmentDetailViewDetailContainer',
            templateUrl: 'static/templates/openslides_protocol/assignment-detail-hook.html',
            scope: getScope(),
        });
    }
]);

}());
